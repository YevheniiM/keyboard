# from __future__ import print_function
import torch
import torch.optim as optim
from torch.utils import data
import numpy as np
import yaml
import logging
from model.model_utils import get_model, get_loss
from dataload.dataloader import seq2seqDataset, SemicharDataset
from metric_counter import MetricCounter
import os
from torch import nn

class Trainer(object):
    def __init__(self, config):
        self.config = config
        self.dataset = self._get_dataset(config["dataroot"], config["seq_length"])
        dlen = len(self.dataset)
        splitlen = [int(0.8*dlen), int(0.1*dlen), 0]
        splitlen[2] = dlen - sum(splitlen)
        
        self.train_dataset, self.val_dataset, self.test_dataset = data.random_split(self.dataset, splitlen)

        self.experiment_name = f"{config['experiment_desc']}_{config['model']['model_n']}"
        self.metric_counter = MetricCounter(self.experiment_name, self.config["print_every"])

    def test(self):
      PATH = f'model/pretrained/best_{self.config["experiment_desc"]}.pth'
      self.model.load_state_dict(torch.load(PATH)['model'])
      self.model.eval()
      self._validate(-1, True)

    def train(self):

        self._init_params()
        self.model.cuda()
        
        for epoch in range(0, self.epochs):
            if self.config['model']['model_n'] == "semichar_rnn":
                self._run_epoch(epoch)
                self._validate(epoch)
            if self.config['model']['model_n'] == "seq2seq+attention":
                self._run_epoch_seq2seq(epoch)
                self._validate_seq2seq(epoch)
            
            if self.metric_counter.update_best_model():
                torch.save({
                    'model': self.model.state_dict(),
                    'optimizer': self.optimizer.state_dict(),
                    'dataset_params': self.dataset.get_params(),
                    'n_hidden': self.config['model']['n_hidden'],
                    'n_layers': self.config['model']['n_layers']
                }, f'model/pretrained/best_{self.config["experiment_desc"]}.pth')

            print(self.metric_counter.loss_message())
            logging.debug(
                f"Experiment Name: {self.config['experiment_desc']}, Epoch: {epoch}, Loss: {self.metric_counter.loss_message()}")
    
    def _run_epoch_seq2seq(self, epoch):
        self.metric_counter.clear()
        
        counter = 0 
        for lenX, X, leny, y, y1hot in self.loader_train:
            h = None
            lenX, perm_idx = lenX.sort(0, descending=True)
            X = X[perm_idx]
            y = y[perm_idx]
            leny = leny[perm_idx]
            y1hot = y1hot[perm_idx]

            X, y = X.float().cuda(), y.float().cuda()
            lenX, leny = lenX.cuda(), leny.cuda()
            y1hot = y1hot.cuda()


            self.optimizer.zero_grad()
            out = self.model(h, lenX, X, leny, y)
            tar = y1hot[:, :out.size(1)]
            tar = tar.contiguous().view(tar.nelement())
            cur = out.contiguous().view(tar.nelement(), -1)
            loss = self.loss_fn(cur, tar)

            loss.backward()

            acc = self.calc_acc(cur, tar)
            nn.utils.clip_grad_norm_(self.model.parameters(), self.config['clip'])
            self.optimizer.step()

            self.metric_counter.add_losses(loss)
            self.metric_counter.add_acc(acc)
            if not counter % self.config['print_every']:
                print(f"Epoch: {epoch}; Train Step: {counter}: {self.metric_counter.loss_message()}")
          
          
            counter += 1

        
        self.metric_counter.write_to_tensorboard(epoch)
            
    def _validate_seq2seq(self, epoch):
        self.metric_counter.clear()

        counter = 0 
        self.model.eval()
        loader = self.loader_val
        for lenX, X, leny, y, y1hot in loader:
            h = None
            lenX, perm_idx = lenX.sort(0, descending=True)
            X = X[perm_idx]
            y = y[perm_idx]
            leny = leny[perm_idx]
            y1hot = y1hot[perm_idx]

            X, y = X.float().cuda(), y.float().cuda()
            lenX, leny = lenX.cuda(), leny.cuda()
            y1hot = y1hot.cuda()

            out = self.model(h, lenX, X, leny, y)
            tar = y1hot[:, :out.size(1)]
            tar = tar.contiguous().view(tar.nelement())
            cur = out.contiguous().view(tar.nelement(), -1)
            loss = self.loss_fn(cur, tar)

            acc = self.calc_acc(cur, tar)

            self.metric_counter.add_losses(loss)
            self.metric_counter.add_acc(acc)
            if not counter % self.config['print_every']:
                print(f"Epoch: {epoch}; Valid Step: {counter}: {self.metric_counter.loss_message()}")
          
          
            counter += 1

        
        self.metric_counter.write_to_tensorboard(epoch, validation=True)
        print(self.metric_counter.loss_message())
        
        self.model.train()
            


            


    def _run_epoch(self, epoch):
        
        self.metric_counter.clear()
        h = None
        counter = 0 
        for X, y in self.loader_train:
            X, y = X.cuda(), y.cuda()

            self.optimizer.zero_grad()
            if h is not None:
              h = tuple([x[:, :X.size(0)].contiguous() for x in h])
            output, h = self.model(X, h)
            
            loss = self.loss_fn(output, y.view(y.nelement()).long())
            loss.backward()
            

            h = tuple([i.detach_() for i in h])
            acc = self.calc_acc(output, y.view(y.nelement()))

            nn.utils.clip_grad_norm_(self.model.parameters(), self.config['clip'])
            self.optimizer.step()

            self.metric_counter.add_losses(loss)
            self.metric_counter.add_acc(acc)
            if not counter % self.config['print_every']:
              print(f"Epoch: {epoch}; Train Step: {counter}: {self.metric_counter.loss_message()}")
          
          
            counter += 1

        
        self.metric_counter.write_to_tensorboard(epoch)
        
        
    
            
    def _validate(self, epoch, test=False):
        h = None
        self.model.eval()
        self.metric_counter.clear()
        counter = 0
        loader = (self.loader_test if test else self.loader_val)

        for X, y in loader:
            X, y = X.cuda(), y.cuda()
            if h is not None:
                h = tuple([x[:, :X.size(0)].contiguous() for x in h])
            output, h = self.model(X, h)

            loss = self.loss_fn(output, y.view(y.nelement()).long())
            acc = self.calc_acc(output, y.view(y.nelement()))

            self.metric_counter.add_losses(loss)
            self.metric_counter.add_acc(acc)
            if not counter % self.config['print_every']:
              print(f"Epoch: {epoch}; Valid Step: {counter}: {self.metric_counter.loss_message()}")
            counter += 1
        
        if not test:
          self.metric_counter.write_to_tensorboard(epoch, validation=True)
        else:
          print(self.metric_counter.loss_message())
        
        self.model.train()
    
    def calc_acc(self, y_pred, y):
        acc_output = y_pred.cpu().detach().numpy().astype("int32")
        acc =  np.equal(acc_output.argmax(1), y.cpu().numpy())
        return acc.sum()/acc_output.shape[0]

  
    def _get_dataset(self, dataroot, seq_length):
        if self.config['model']['model_n'] == "semichar_rnn":
            return SemicharDataset(dataroot, seq_length)
        if self.config['model']['model_n'] == "seq2seq+attention":
            return seq2seqDataset(dataroot, seq_length, 50, 1000)

    def _get_optim(self, params):
        if self.config['optimizer']['name'] == 'adam':
            optimizer = optim.Adam(params, lr=self.config['optimizer']['lr'])
        elif self.config['optimizer']['name'] == 'sgd':
            optimizer = optim.SGD(params, lr=self.config['optimizer']['lr'])
        else:
            raise ValueError(f"Optimizer {self.config['optimizer']['name']} not recognized.")
        return optimizer
      
    def _init_params(self):

        self.loader_train = data.DataLoader(self.train_dataset,
                                            batch_size=self.config['batch_size'],
                                            shuffle=True)
        self.loader_val = data.DataLoader(self.val_dataset,
                                          batch_size=self.config['batch_size'],
                                          shuffle=False)

        self.loader_test = data.DataLoader(self.test_dataset,
                                          batch_size=self.config['batch_size'],
                                          shuffle=False)
                                          
        self.model = get_model(self.config['model']['model_n'],
                               self.dataset.get_params(),
                               self.config['model']['n_hidden'],
                               self.config['model']['n_layers'],
                               self.config['model']['drop_prob'],
                               self.config['model']['grad_clip'],
                               self.config['model']['attn_model'],
                               self.config['model']['dim'],
                               self.config['model']['vs'])

        self.epochs = self.config['num_epochs']
        self.optimizer = self._get_optim(self.model.parameters())
        self.loss_fn = get_loss(self.config['model']['loss'])

        


if __name__ == '__main__':
    with open('config/params.yaml', 'r') as f:
        config = yaml.load(f)

    trainer = Trainer(config)
    trainer.train()