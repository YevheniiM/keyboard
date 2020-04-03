import numpy as np
from tensorboardX import SummaryWriter
import logging
from math import inf


class MetricCounter():
  
    def __init__(self, exp_name, print_every):
        self.writer = SummaryWriter(exp_name)
        logging.basicConfig(filename='{}.log'.format(exp_name), level=logging.DEBUG)
        self.loss = []
        self.acc = []
        self.print_every = print_every
        self.best_metric = inf

    def clear(self):
        self.loss = []
        self.acc = []

    def add_losses(self, loss):
        self.loss.append(loss.item())

    def add_acc(self, acc):
        self.acc.append(acc)

    def loss_message(self, full=False):
        k = 0 if full else -self.print_every
        mean_loss = np.mean(self.loss[k:])
        mean_acc = np.mean(self.acc[k:])
        return f'loss={round(mean_loss, 3)}; acc={mean_acc};'

    def write_to_tensorboard(self, epoch_num, validation=False):
        scalar_prefix = 'Validation' if validation else 'Train'
        self.writer.add_scalar(f'{scalar_prefix}_loss', np.mean(self.loss), epoch_num)
        self.writer.add_scalar(f'{scalar_prefix}_acc', np.mean(self.acc), epoch_num)


    def update_best_model(self):
        cur_metric = np.mean(self.loss)
        if self.best_metric > cur_metric:
            self.best_metric = cur_metric
            return True
        return False