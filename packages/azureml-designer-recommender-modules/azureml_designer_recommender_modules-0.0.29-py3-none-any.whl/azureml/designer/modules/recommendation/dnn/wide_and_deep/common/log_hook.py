import numpy as np
import tensorflow as tf
from azureml.core.run import Run


class LogHook(tf.estimator.SessionRunHook):
    LOSS_TABLE_NAME = "Loss"

    def __init__(self, total_steps, log_steps):
        self.log_every_n_steps = np.ceil(total_steps / log_steps)
        self.steps = 0
        self.run = Run.get_context()
        self.cum_loss = 0.0

    def after_run(self, run_context, run_values):
        self.steps += 1
        self.cum_loss += run_values.results[1]

        if self.steps % self.log_every_n_steps == 0:
            avg_loss = self.cum_loss / self.log_every_n_steps
            self.run.log_row(self.LOSS_TABLE_NAME, **{"Global step": self.steps, "Loss": avg_loss})
            self.cum_loss = 0.0

    def before_run(self, run_context):
        return run_context.original_args

    def end(self, session):
        self.run.flush()
