import os
from math import ceil
import tensorflow as tf
import pandas as pd
from pandas.api.types import is_integer_dtype, is_float_dtype, is_string_dtype
from abc import abstractmethod
from azureml.designer.modules.recommendation.dnn.common.dataset import TransactionDataset
from azureml.designer.modules.recommendation.dnn.common.feature_builder import FeatureBuilder
from azureml.designer.modules.recommendation.dnn.common.constants import RANDOM_SEED
from azureml.designer.modules.recommendation.dnn.common.distributed_utils import distributed_env
from azureml.studio.core.logger import common_logger, TimeProfile
from tempfile import TemporaryDirectory


class InputFunctionBuilder:
    def __init__(self,
                 transactions: TransactionDataset,
                 user_feature_builder: FeatureBuilder,
                 item_feature_builder: FeatureBuilder,
                 batch_size,
                 epochs,
                 random_seed=RANDOM_SEED):
        self.transactions = transactions
        self.batch_size = batch_size
        self.epochs = epochs
        self.random_seed = random_seed

        self._init_features_lookup(user_feature_builder=user_feature_builder, item_feature_builder=item_feature_builder)

    def _init_features_lookup(self, user_feature_builder, item_feature_builder):
        self.user_features_lookup = user_feature_builder.build_feature_lookup(ids=self.transactions.users)
        self.item_features_lookup = item_feature_builder.build_feature_lookup(ids=self.transactions.items)

    @abstractmethod
    def get_input_fn(self):
        pass


class TrainInputFunctionBuilder(InputFunctionBuilder):
    def __init__(self,
                 transactions: TransactionDataset,
                 user_feature_builder: FeatureBuilder,
                 item_feature_builder: FeatureBuilder,
                 batch_size,
                 epochs,
                 shuffle,
                 random_seed=RANDOM_SEED):
        common_logger.debug("Init train input function builder.")
        super().__init__(transactions, user_feature_builder, item_feature_builder, batch_size, epochs, random_seed)
        if shuffle:
            self.transactions.df = self.transactions.df.sample(frac=1.0, random_state=self.random_seed).reset_index(
                drop=True)
        if distributed_env.exist_cluster():
            worker_count = distributed_env.worker_count
            task_index = distributed_env.task_index

            instances_count_per_worker = len(self.transactions.df) // worker_count
            self.transactions.df = \
                self.transactions.df.iloc[
                    task_index * instances_count_per_worker:(task_index + 1) * instances_count_per_worker].reset_index(
                    drop=True)
            common_logger.info(
                f"Split dataset into {worker_count} shards, "
                f"current shard index: {distributed_env.task_index}, "
                f"instances count: {len(self.transactions.df)}")
            common_logger.info(f"Notice that the remaining instances would be dropped.")

        self.work_dir = TemporaryDirectory()

    def get_input_fn(self):
        csv_file = os.path.join(self.work_dir.name, 'input.csv')

        if self.transactions.row_size == 0:
            common_logger.debug("No valid samples found, return none input function.")
            return None

        header = []
        feature_types = []
        for df in [self.user_features_lookup, self.item_features_lookup]:
            for col in df:
                header.append(col)
                if is_float_dtype(df[col]):
                    feature_types.append(tf.float32)
                elif is_integer_dtype(df[col]):
                    feature_types.append(tf.int32)
                elif is_string_dtype(df[col]):
                    # need to set with empty string, or it would be set as missing when loading batck
                    feature_types.append('')
        header.append(self.transactions.rating_col)
        feature_types.append(tf.float32)

        CHUNK_SIZE = 100000
        with TimeProfile(f"Serialize training dataset to csv file: {csv_file}, chunk size: {CHUNK_SIZE}"):
            pd.DataFrame({}, columns=header).to_csv(csv_file, index=False, header=True)

            chunk_count = ceil(self.transactions.row_size / CHUNK_SIZE)
            for i in range(chunk_count):
                chunk_transactions = self.transactions.df.iloc[i:(i + 1) * CHUNK_SIZE, :]
                chunk_users = self.user_features_lookup.loc[chunk_transactions[self.transactions.user_col]].reset_index(
                    drop=True)
                chunk_items = self.item_features_lookup.loc[chunk_transactions[self.transactions.item_col]].reset_index(
                    drop=True)
                chunk_df = pd.concat(
                    [chunk_users, chunk_items, chunk_transactions[self.transactions.rating_col].reset_index(drop=True)],
                    axis=1)
                chunk_df.to_csv(csv_file, index=False, mode='a', header=False)

        return lambda: self._dataset(csv_file, self.batch_size, self.epochs, self.transactions.ratings.name,
                                     feature_types)

    @staticmethod
    def _dataset(csv_file, batch_size, epochs, label_name, feature_types):
        dataset = tf.data.experimental.make_csv_dataset(file_pattern=csv_file, batch_size=batch_size,
                                                        label_name=label_name, num_epochs=epochs, shuffle=False,
                                                        column_defaults=feature_types)

        return dataset


class RatingPredictionInputFunctionBuilder(InputFunctionBuilder):
    def __init__(self,
                 transactions: TransactionDataset,
                 user_feature_builder: FeatureBuilder,
                 item_feature_builder: FeatureBuilder,
                 batch_size,
                 random_seed=RANDOM_SEED):
        common_logger.debug("Init rating prediction function builder.")
        super().__init__(transactions, user_feature_builder, item_feature_builder, batch_size, 1, random_seed)

    def get_input_fn(self):
        if self.transactions.row_size == 0:
            common_logger.debug("No valid samples found, return none input function.")
            return None

        user_ids = self.transactions.users
        item_ids = self.transactions.items

        users = self.user_features_lookup.loc[user_ids].reset_index(drop=True)
        items = self.item_features_lookup.loc[item_ids].reset_index(drop=True)
        x_df = pd.concat([users, items], axis=1)

        return tf.compat.v1.estimator.inputs.pandas_input_fn(x=x_df,
                                                             y=None,
                                                             batch_size=self.batch_size,
                                                             num_epochs=self.epochs,
                                                             shuffle=False)


class RecommendationInputFunctionBuilder(InputFunctionBuilder):
    def __init__(self,
                 transactions: TransactionDataset,
                 user_feature_builder: FeatureBuilder,
                 item_feature_builder: FeatureBuilder,
                 batch_size,
                 random_seed=RANDOM_SEED):
        common_logger.debug("Init recommendation input function builder.")
        super().__init__(transactions, user_feature_builder, item_feature_builder, batch_size, 1, random_seed)
        self.user_ids = self.transactions.users.unique()
        self.item_vocab = self.item_features_lookup.index.values

    def _init_features_lookup(self, user_feature_builder, item_feature_builder):
        self.user_features_lookup = user_feature_builder.build_feature_lookup(ids=self.transactions.users)
        self.item_features_lookup = item_feature_builder.build_feature_lookup(ids=item_feature_builder.dynamic_id_vocab)

    def get_input_fn(self):
        if self.transactions.row_size == 0:
            common_logger.debug("No valid samples found, return none input function.")
            return None

        return lambda: self._dataset(self.user_features_lookup, self.item_features_lookup, self.user_ids,
                                     self.batch_size)

    @staticmethod
    def _dataset(user_features_lookup, item_features_lookup, user_ids, batch_size):
        users = user_features_lookup.loc[user_ids]
        users_dataset = tf.data.Dataset.from_tensor_slices(users.to_dict("list"))
        items_dataset = tf.data.Dataset.from_tensor_slices(item_features_lookup.to_dict("list"))

        item_num = len(item_features_lookup)
        users_dataset = users_dataset.interleave(lambda x: tf.data.Dataset.from_tensors(x).repeat(item_num),
                                                 cycle_length=1, block_length=item_num)

        user_num = len(user_ids)
        items_dataset = items_dataset.repeat(user_num)

        dataset = (tf.data.Dataset.zip((users_dataset, items_dataset)).
                   flat_map(lambda user, item: tf.data.Dataset.from_tensors({**user, **item})))
        dataset = dataset.batch(batch_size * item_num).prefetch(tf.data.experimental.AUTOTUNE)

        return dataset
