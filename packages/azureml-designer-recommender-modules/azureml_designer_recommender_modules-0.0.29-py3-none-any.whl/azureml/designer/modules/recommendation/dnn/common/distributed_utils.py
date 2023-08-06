import os
import json
import random
from azureml.studio.core.logger import common_logger


class DistributedEnv:
    HOST_LIST_ENV = "AZ_BATCH_HOST_LIST"
    PROCESS_PER_NODE_ENV = "AZUREML_PARAMETER_Mpi_Process_Count_Per_Node"
    NODE_COUNT_ENV = "AZUREML_NODE_COUNT"
    TASK_INDEX_ENV = "AZ_BATCHAI_TASK_INDEX"
    TF_CLUSTER_CONFIG_ENV = "TF_CONFIG"

    def __init__(self):
        self.hosts = os.environ.get(self.HOST_LIST_ENV, 'localhost')
        self.process_per_node = int(
            os.environ[self.PROCESS_PER_NODE_ENV]) if self.PROCESS_PER_NODE_ENV in os.environ else None

        self.node_count = int(os.environ[self.NODE_COUNT_ENV]) if self.NODE_COUNT_ENV in os.environ else None
        self.task_index = int(os.environ[self.TASK_INDEX_ENV]) if self.TASK_INDEX_ENV in os.environ else None

    def is_chief(self):
        return self.task_index == 0 or self.task_index is None

    def setup_multi_worker_mirrored_cluster(self, gpu_support=True):
        random.seed(42)

        if self.exist_cluster():
            common_logger.info("Training cluster exists, skip cluster setup.")
            common_logger.info(os.environ[self.TF_CLUSTER_CONFIG_ENV])
            return

        common_logger.info(f"Node List: {self.hosts}, "
                           f"Process Per Node: {self.process_per_node}, "
                           f"Task index: {self.task_index}")

        if any(val is None for val in [self.process_per_node, self.task_index]):
            common_logger.info("Not find cluster setting, train the model standalone")
            return

        # the worker needs to know the explicit port each others use, random choose
        workers = [f'{node}:{random.randint(20000, 40000)}' for node in self.hosts.split(',') for i in
                   range(self.process_per_node)]

        cluster_config = {
            'cluster': {
                'chief': workers[:1],
                'worker': workers[1:]
            },
        }
        if self.task_index == 0:
            cluster_config['task'] = {'type': 'chief', 'index': 0}
        else:
            cluster_config['task'] = {'type': 'worker', 'index': self.task_index - 1}

        os.environ[self.TF_CLUSTER_CONFIG_ENV] = json.dumps(cluster_config)
        if gpu_support:
            os.environ["CUDA_VISIBLE_DEVICES"] = str(self.task_index % self.process_per_node)
        else:
            os.environ["CUDA_VISIBLE_DEVICES"] = '-1'
        common_logger.info(f"Setup training cluster for multi worker mirrored strategy: {cluster_config}")

        return

    @property
    def worker_count(self):
        if self.node_count is None or self.process_per_node is None:
            return None

        return self.node_count * self.process_per_node

    def exist_cluster(self):
        return os.environ.get(self.TF_CLUSTER_CONFIG_ENV, None) is not None


distributed_env = DistributedEnv()
