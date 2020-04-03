
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

class SemiCharRNN(nn.Module):
    
    def __init__(self, dataset_params, n_hidden=650, n_layers=2,
                               drop_prob=0.5, grad_clip = 5):
        super().__init__()
        self.dataset_params = dataset_params
        self.drop_prob = drop_prob
        self.n_layers = n_layers
        self.n_hidden = n_hidden
        
        
        self.rnn = nn.LSTM(3*len(self.dataset_params["chars"]), n_hidden, n_layers, 
                            dropout=drop_prob, batch_first=True)
        
        self.dropout = nn.Dropout(drop_prob)
        
        self.fc = nn.Linear(n_hidden, len(self.dataset_params["words"]))
        
      
    
    def forward(self, x, hidden):
                
        r_output, hidden = self.rnn(x, hidden)
        
        out = self.dropout(r_output)
        
        out = out.contiguous().view(-1, self.n_hidden)
        out = F.log_softmax(self.fc(out))
        
        return out, hidden
    