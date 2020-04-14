
from model.semichar_rnn import SemiCharRNN
from model.seq2seq import AttentionAutoencoder
from torch import nn
from model.losses import masked_ce_loss

def get_model(model_name, dataset_params, n_hidden, n_layers, drop_prob, grad_clip, attn_model, dim, vs):
  if model_name == "semichar_rnn":
    net = SemiCharRNN(dataset_params, n_hidden, n_layers, drop_prob, grad_clip)
  elif model_name == "seq2seq+attention":
    net = AttentionAutoencoder(dim, n_hidden, vs, n_layers, attn_model)
  else:
    raise ValueError(f"Architecture with such name ({model_name}) is nt defined")
  return net

def get_loss(loss):
  if loss == "CE":
    return nn.CrossEntropyLoss()
  if loss == "MaskedCE":
    return masked_ce_loss()