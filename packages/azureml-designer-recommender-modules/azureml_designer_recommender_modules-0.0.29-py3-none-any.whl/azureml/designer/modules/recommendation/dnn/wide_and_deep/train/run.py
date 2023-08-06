from azureml.designer.modules.recommendation.dnn.wide_and_deep.train.train_wide_and_deep_recommender import \
    TrainWideAndDeepRecommenderModule
from azureml.designer.modules.recommendation.dnn.common.entry_utils import build_cli_args
from azureml.studio.internal.error_handler import error_handler
from azureml.designer.modules.recommendation.dnn.common.distributed_utils import distributed_env

error_handler._save_module_statistics = distributed_env.is_chief()


@error_handler
def main():
    kwargs = build_cli_args(TrainWideAndDeepRecommenderModule().run)
    TrainWideAndDeepRecommenderModule().run(**kwargs)


if __name__ == "__main__":
    main()
