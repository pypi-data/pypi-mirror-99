import os
import datetime
import shutil
import tensorflow as tf
import numpy as np
import pickle
from enum import Enum
from time import time
from azureml.studio.core.logger import module_logger, TimeProfile
from azureml.designer.modules.recommendation.dnn.common.entry_param import EntryParam
from azureml.studio.core.error import UserError, InvalidDirectoryError
from azureml.studio.internal.error import InvalidModelDirectoryError
from azureml.designer.modules.recommendation.dnn.common.feature_builder import FeatureBuilder
from azureml.designer.modules.recommendation.dnn.common.tf_feature_columns import CategoricalVocabListFeatureColumn, \
    NumericFeatureColumn, CrossedFeatureColumn, EmbeddingFeatureColumn, parse_basic_features
from azureml.designer.modules.recommendation.dnn.common.constants import RANDOM_SEED, MODEL_SAVE_FILE
from azureml.designer.modules.recommendation.dnn.common.dataset import FeatureDataset
from azureml.studio.core.io.model_directory import ModelDirectory
from azureml.designer.core.model.core_model import CoreModel
from azureml.designer.modules.recommendation.dnn.wide_and_deep.common.input_function_builder import InputFunctionBuilder
from azureml.designer.modules.recommendation.dnn.common.distributed_utils import distributed_env
from azureml.designer.modules.recommendation.dnn.wide_and_deep.common.log_hook import LogHook


class ActivationFnSelection(Enum):
    ReLU = 'ReLU'
    Sigmoid = 'Sigmoid'
    Tanh = 'Tanh'
    Linear = 'Linear'
    LeakyReLU = 'LeakyReLU'


class OptimizerSelection(Enum):
    Adagrad = 'Adagrad'
    Adam = 'Adam'
    Ftrl = 'Ftrl'
    RMSProp = 'RMSProp'
    SGD = 'SGD'
    Adadelta = 'Adadelta'


class NanLossDuringTrainingError(UserError):
    def __init__(self):
        msg = "Training stopped with NanLossDuringTrainingError. " \
              "Please try other optimizers, smaller batch size and/or smaller learning rate."
        super().__init__(msg)


class ResourceExhaustedError(UserError):
    def __init__(self):
        msg = "Resource has been exhausted. Please upgrade compute size or use a smaller network or batch size."
        super().__init__(msg)


class WideNDeepModelHyperParams:
    def __init__(self,
                 epochs,
                 batch_size,
                 wide_optimizer,
                 wide_lr,
                 deep_optimizer,
                 deep_lr,
                 hidden_units,
                 activation_fn,
                 dropout,
                 batch_norm,
                 crossed_dim,
                 user_dim,
                 item_dim,
                 embed_dim):
        self.epochs = epochs
        self.batch_size = batch_size
        self.wide_optimizer = wide_optimizer
        self.wide_lr = wide_lr
        self.deep_optimizer = deep_optimizer
        self.deep_lr = deep_lr
        self.hidden_units = hidden_units
        self.activation_fn = activation_fn
        self.dropout = dropout
        self.batch_norm = batch_norm
        self.crossed_dim = crossed_dim
        self.user_dim = user_dim
        self.item_dim = item_dim
        self.embed_dim = embed_dim

    def __str__(self):
        hyper_param_info = f"Epochs: {self.epochs}\n" \
            f"Batch size: {self.batch_size}\n" \
            f"Wide optimizer: {self.wide_optimizer}\n" \
            f"Wide learning rate: {self.wide_lr}\n" \
            f"Deep optimizer: {self.deep_optimizer}\n" \
            f"Deep learning rate: {self.deep_lr}\n" \
            f"Hidden units: {self.hidden_units}\n" \
            f"Activation function: {self.activation_fn}\n" \
            f"Dropout: {self.dropout}\n" \
            f"Batch norm: {self.batch_norm}\n" \
            f"Crossed dimension: {self.crossed_dim}\n" \
            f"User embedding dimension: {self.user_dim}\n" \
            f"Item embedding dimension: {self.item_dim}\n" \
            f"Categorical feature embedding dimension: {self.embed_dim}"

        return hyper_param_info

    @property
    def gpu_support(self):
        gpu_support_optimizers = [OptimizerSelection.Adam, OptimizerSelection.RMSProp, OptimizerSelection.SGD]

        return self.deep_optimizer in gpu_support_optimizers and self.wide_optimizer in gpu_support_optimizers


class WideNDeepModel(CoreModel, metaclass=EntryParam):
    MODEL_NAME = "Wide & Deep Recommendation Model"
    _ENTRY_PARAM_LOADER = "entry_param_loader"

    def __init__(self, hyper_params: WideNDeepModelHyperParams, user_feature_builder: FeatureBuilder,
                 item_feature_builder: FeatureBuilder, wide_columns=None, deep_columns=None, random_seed=RANDOM_SEED,
                 rel_checkpoints_dir='checkpoints'):
        self.hyper_params = hyper_params
        self.random_seed = random_seed
        self.rel_checkpoints_dir = rel_checkpoints_dir
        self.user_feature_builder = user_feature_builder
        self.item_feature_builder = item_feature_builder
        self.wide_columns = wide_columns
        self.deep_columns = deep_columns
        self.estimator = None

    def default_columns(self):
        """Define a default wide columns and deep columns scheme.

        The wide columns include, users, items, users and items crossed features.
        The deep columns include, user embeddings, item embeddings, other categorical feature embeddings
        and numeric features.
        """
        user = CategoricalVocabListFeatureColumn(key=self.user_feature_builder.id_key,
                                                 vocab=self.user_feature_builder.id_vocab)
        item = CategoricalVocabListFeatureColumn(key=self.item_feature_builder.id_key,
                                                 vocab=self.item_feature_builder.id_vocab)

        # wide feature columns
        crossed_feature = CrossedFeatureColumn(categorical_features=[user, item],
                                               hash_bucket_size=self.hyper_params.crossed_dim)
        wide_columns = [user, item, crossed_feature]

        # deep feature columns
        user_embed = EmbeddingFeatureColumn(categorical_feature=user, dimension=self.hyper_params.user_dim)
        item_embed = EmbeddingFeatureColumn(categorical_feature=item, dimension=self.hyper_params.item_dim)
        deep_columns = [user_embed, item_embed]

        for key, feature_meta in {**self.user_feature_builder.feature_metas,
                                  **self.item_feature_builder.feature_metas}.items():
            if feature_meta.is_numeric_feature():
                deep_columns.append(NumericFeatureColumn(key=key))
            else:
                cat_feature = CategoricalVocabListFeatureColumn(key=key, vocab=feature_meta.vocab)
                deep_columns.append(
                    EmbeddingFeatureColumn(categorical_feature=cat_feature, dimension=self.hyper_params.embed_dim))

        return wide_columns, deep_columns

    def build_model(self, run_config=None, model_dir=None):
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)
        if run_config is None:
            run_config = tf.estimator.RunConfig(tf_random_seed=self.random_seed,  # fix random seed
                                                save_summary_steps=None,  # disable summary
                                                save_checkpoints_secs=None,  # disable checkpoints
                                                save_checkpoints_steps=None)  # disable checkpoints
        # build feature columns
        wide_columns, deep_columns = self._build_feature_columns()
        # build optimizers
        wide_optimizer = self.build_optimizer(optimizer_name=self.hyper_params.wide_optimizer,
                                              learning_rate=self.hyper_params.wide_lr)
        deep_optimizer = self.build_optimizer(optimizer_name=self.hyper_params.deep_optimizer,
                                              learning_rate=self.hyper_params.deep_lr)
        # build activation function
        activation_fn = self.build_activation_fn(activation_fn_name=self.hyper_params.activation_fn)

        self.estimator = tf.estimator.DNNLinearCombinedRegressor(linear_feature_columns=wide_columns,
                                                                 linear_optimizer=wide_optimizer,
                                                                 dnn_feature_columns=deep_columns,
                                                                 dnn_optimizer=deep_optimizer,
                                                                 dnn_hidden_units=self.hyper_params.hidden_units,
                                                                 dnn_activation_fn=activation_fn,
                                                                 dnn_dropout=self.hyper_params.dropout,
                                                                 batch_norm=self.hyper_params.batch_norm,
                                                                 config=run_config,
                                                                 model_dir=model_dir)

    def train(self, input_function_builder: InputFunctionBuilder):
        # this line is a workaround for issue:
        # https://github.com/tensorflow/tensorflow/issues/46556
        tf.compat.v1.disable_eager_execution()
        instances_count = input_function_builder.transactions.row_size
        # if train model on multiple workers, this is the batch count per worker
        batches_count = np.ceil(instances_count / input_function_builder.batch_size)
        module_logger.info(f"Get {instances_count} training instances, and {batches_count} batches per epoch.")

        if distributed_env.exist_cluster():
            strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()
            module_logger.info(f"Found training cluster, would train model with multi worker mirrored strategy.")
        else:
            strategy = None
            module_logger.info(f"Not found training cluster, would train model standalone.")

        run_config = tf.estimator.RunConfig(tf_random_seed=self.random_seed,
                                            log_step_count_steps=batches_count,  # log loss after each epoch
                                            save_checkpoints_steps=batches_count * self.hyper_params.epochs,
                                            keep_checkpoint_max=1,
                                            train_distribute=strategy)

        module_logger.info(f"Build model:\n{self.hyper_params}")
        self.build_model(run_config=run_config)

        input_fn = input_function_builder.get_input_fn()
        metrics_log_hook = LogHook(total_steps=batches_count * self.hyper_params.epochs, log_steps=200)

        if input_fn is None:
            return
        try:
            with TimeProfile("Training Wide & Deep recommendation model"):
                if distributed_env.exist_cluster():
                    if distributed_env.is_chief():
                        hooks = [metrics_log_hook]
                    else:
                        hooks = None
                    train_spec = tf.estimator.TrainSpec(input_fn=input_fn, hooks=hooks)
                    eval_spec = tf.estimator.EvalSpec(input_fn=lambda: tf.data.Dataset.from_tensor_slices(()),
                                                      steps=None)
                    tf.estimator.train_and_evaluate(estimator=self.estimator, train_spec=train_spec,
                                                    eval_spec=eval_spec)
                else:
                    self.estimator.train(input_fn=input_fn, hooks=[metrics_log_hook])
        except tf.estimator.NanLossDuringTrainingError as e:
            raise NanLossDuringTrainingError() from e
        except tf.errors.ResourceExhaustedError as e:
            raise ResourceExhaustedError() from e

    def predict(self, input_function_builder: InputFunctionBuilder):
        input_fn = input_function_builder.get_input_fn()
        batch_count = int(np.ceil(input_function_builder.transactions.row_size / input_function_builder.batch_size))
        log_every_n_batches = batch_count // 5 if batch_count >= 5 else batch_count
        finished_batch_count = 0
        start_time = time()

        module_logger.info(
            f"Get {input_function_builder.transactions.row_size} test instances, split into {batch_count} batches.")
        module_logger.info(f"Rebuild model:\n {self.hyper_params}")

        if input_fn is None:
            raise StopIteration

        try:
            for predictions in self.estimator.predict(input_fn=input_fn, yield_single_examples=False):
                if finished_batch_count > 0 and finished_batch_count % log_every_n_batches == 0:
                    cost_seconds = time() - start_time
                    remaining_seconds = (
                            cost_seconds / finished_batch_count * (batch_count - finished_batch_count))
                    module_logger.info(f"Finished {finished_batch_count} batch predictions, "
                                       f"cost time: {datetime.timedelta(seconds=cost_seconds)}."
                                       f"Remaining time: {datetime.timedelta(seconds=remaining_seconds)}")
                finished_batch_count += 1

                yield predictions['predictions']
        except tf.errors.ResourceExhaustedError as e:
            raise ResourceExhaustedError() from e

    def update_feature_builders(self, user_features: FeatureDataset, item_features: FeatureDataset):
        with TimeProfile("Update features for users"):
            self.user_feature_builder.update(features=user_features)
        with TimeProfile("Update features for items"):
            self.item_feature_builder.update(features=item_features)

    @staticmethod
    def build_optimizer(optimizer_name: OptimizerSelection, learning_rate):
        """Build the optimizer through optimizer name.

        These optimizers come from TensorFlow library, for an overview, please refer to:
        https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
        """
        optimizers = {OptimizerSelection.Adagrad: tf.optimizers.Adagrad,
                      OptimizerSelection.Adam: tf.optimizers.Adam,
                      OptimizerSelection.Ftrl: tf.optimizers.Ftrl,
                      OptimizerSelection.RMSProp: tf.optimizers.RMSprop,
                      OptimizerSelection.SGD: tf.optimizers.SGD,
                      OptimizerSelection.Adadelta: tf.keras.optimizers.Adadelta}
        optimizer = optimizers.get(optimizer_name, None)
        if optimizer is None:
            raise ValueError(f"Unsupported optimizer {optimizer_name}")

        return optimizer(learning_rate=learning_rate)

    @staticmethod
    def build_activation_fn(activation_fn_name: ActivationFnSelection):
        """
        Build the activation function through activation function name.

        This activation functions come from TensorFlow library, for an overview, please refer to:
        https://www.tensorflow.org/api_docs/python/tf/keras/activations
        """

        activation_fns = {ActivationFnSelection.ReLU: tf.nn.relu,
                          ActivationFnSelection.Sigmoid: tf.keras.activations.sigmoid,
                          ActivationFnSelection.Tanh: tf.keras.activations.tanh,
                          ActivationFnSelection.Linear: tf.keras.activations.linear,
                          ActivationFnSelection.LeakyReLU: tf.nn.leaky_relu}
        activation_fn = activation_fns.get(activation_fn_name, None)
        if activation_fn is None:
            raise ValueError(f"Unsupported activation function {activation_fn_name}")

        return activation_fn

    def _build_feature_columns(self):
        # if not specify wide and deep feature columns, use default scheme
        if self.wide_columns is None and self.deep_columns is None:
            self.wide_columns, self.deep_columns = self.default_columns()
        # check if basic feature columns are in feature builders
        self._check_feature_columns()
        wide_columns = [feature_column.build() for feature_column in self.wide_columns]
        deep_columns = [feature_column.build() for feature_column in self.deep_columns]

        return wide_columns, deep_columns

    def _check_feature_columns(self):
        basic_features = parse_basic_features(feature_columns=[*self.wide_columns, *self.deep_columns])
        module_logger.info(f"Model is expected to be fed with features: {[f.key for f in basic_features]}")
        feature_keys = {*self.user_feature_builder.feature_metas.keys(),
                        *self.item_feature_builder.feature_metas.keys(),
                        self.user_feature_builder.id_key,
                        self.item_feature_builder.id_key}
        for feature in basic_features:
            if feature.key not in feature_keys:
                raise RuntimeError(f"feature {feature.key} not found in feature datasets.")

    def save(self, save_to: str, overwrite_if_exists=True):
        with TimeProfile("Saving Wide & Deep recommendation model"):
            # check if saved model already exists
            checkpoints_save_dir = os.path.join(save_to, self.rel_checkpoints_dir)
            checkpoints_exist = tf.train.latest_checkpoint(checkpoints_save_dir) is not None
            model_save_path = os.path.join(save_to, MODEL_SAVE_FILE)
            model_exist = os.path.exists(model_save_path)

            # if checkpoints and model both exists, and not overwrite, raise error
            if checkpoints_exist and model_exist and not overwrite_if_exists:
                raise ValueError(f"Saved model already exists in the target directory: {save_to}")

            # save tensorflow checkpoints to the target dir
            latest_ckpt_file = self.estimator.latest_checkpoint()
            if latest_ckpt_file is None:
                raise ValueError(f"Cannot find checkpoint file of the estimator.")
            checkpoints_dir = os.path.dirname(latest_ckpt_file)

            # copy checkpoints from current temp dir to save path
            # todo: to remove copy logic as soon as DS supports write save_to path directly
            if os.path.exists(checkpoints_save_dir):
                shutil.rmtree(checkpoints_save_dir)
            shutil.copytree(src=checkpoints_dir, dst=checkpoints_save_dir)

            # save estimator wrapper model
            self.estimator = None
            for feature_column in [*self.wide_columns, *self.deep_columns]:
                feature_column.reset()

            # dump model
            with open(model_save_path, "wb") as f:
                pickle.dump(self, f)

    @classmethod
    def entry_param_loader(cls, load_from):
        if isinstance(load_from, str):
            try:
                model = ModelDirectory.load_instance(load_from_dir=load_from, model_class=cls)
            except InvalidDirectoryError as e:
                raise InvalidModelDirectoryError(arg_name=cls.MODEL_NAME,
                                                 reason='the model may not be generated by '
                                                        'the "Train Wide & Deep Recommender" module') from e
        elif isinstance(load_from, ModelDirectory):
            model = load_from.model
        else:
            raise NotImplementedError(
                f"Cannot load Wide & Deep recommendation model from {load_from} of type {type(load_from)}")

        if not isinstance(model, cls):
            raise InvalidModelDirectoryError(arg_name=cls.MODEL_NAME,
                                             reason='the model may not be generated by '
                                                    'the "Train Wide & Deep Recommender" module')

        return model

    @classmethod
    def load(cls, load_from: str):
        model_save_path = os.path.join(load_from, MODEL_SAVE_FILE)
        try:
            with open(model_save_path, "rb") as f:
                model = pickle.load(f)
        except Exception as e:
            raise InvalidModelDirectoryError(arg_name=cls.MODEL_NAME,
                                             reason='the model may not be generated by '
                                                    'the "Train Wide & Deep Recommender" module') from e

        if isinstance(model, cls):
            checkpoints_dir = os.path.join(load_from, model.rel_checkpoints_dir)
            checkpoints_exist = tf.train.latest_checkpoint(checkpoints_dir) is not None
            if not checkpoints_exist:
                raise ValueError(f"Invalid checkpoints path {checkpoints_dir}, no checkpoints found.")
            model.build_model(model_dir=checkpoints_dir)

        else:
            raise InvalidModelDirectoryError(arg_name=cls.MODEL_NAME,
                                             reason='the model may not be generated by '
                                                    'the "Train Wide & Deep Recommender" module')

        return model
