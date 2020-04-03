import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
import nlpaug.augmenter.char as nac
import spacy
import os
import time
import socket
from model.semichar_rnn import SemiCharRNN
from dataload.dataloader import SemicharDataset

train_on_gpu = torch.cuda.is_available()
spacy_nlp = spacy.load('en_core_web_sm')


class Corrector:
  def __init__(self, dataset_params, net):
    self.net = net
    self.dataset_params = dataset_params
    self.dataset = SemicharDataset(None, None, self.dataset_params)
  
  def sample(self, sentence):
    lst_res = []
    z = spacy_nlp(sentence, disable=['parser', 'tagger', 'ner'])
    spl = [token.text for token in z if not (token.text.isspace() or (token.text[0].isdigit() and token.text[-1].isdigit()))]
    h = None

    for word in spl:
        pred, h = self.predict(word, h)
        lst_res.append(self.dataset_params['int2word'][torch.argmax(pred).item()])
    
    return ' '.join(lst_res)

  def predict(self, word, h=None):
      x = np.array([word])
      x = self.dataset.get_encodes(x, False).reshape(1, 1, -1)
      
      inputs = torch.from_numpy(x)

      if(train_on_gpu):
          inputs = inputs.cuda()

      
      out, h = self.net(inputs, h)
      h = tuple([each.detach_() for each in h])

      if(train_on_gpu):
          out = out.cpu() # move to cpu

      return out, h


    


if __name__  == "__main__":
    PATH = "model/pretrained/best_model.net"
    dev = (torch.device('cpu') if not train_on_gpu else torch.device("cuda"))
    d = torch.load(PATH, map_location=dev)
    st_dict = d['model']
    params = d['dataset_params']

    model = SemiCharRNN(params, n_hidden=d['n_hidden'], n_layers=d['n_layers'])
    model.load_state_dict(st_dict)
    model.eval()

    if(train_on_gpu):
        model.cuda()
    else:
        model.cpu()

    cor = Corrector(params, model)


    HOST = '127.0.0.1'
    PORT = 65432
    print("prepared")

#    start = time.time()

#    print(sample(model, "Aoccdrnig to a rscheearch at Cmabrigde Uinervtisy,it deosn't mttaer in waht oredr the ltteers in a wrodare, the olny iprmoetnt tihng is taht the frist and lsatltteer be at the rghit pclae. The rset can be a toatlmses and you can sitll raed it wouthit porbelm. Tihsis bcuseae the huamn mnid deos not raed ervey lteterby istlef, but the wrod as a wlohe."))
#    print(time.time() - start)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendto(str.encode(cor.sample(data.decode())), addr)