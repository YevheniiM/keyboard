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
from dataload.dataloader import AutoCompleteDataset

train_on_gpu = torch.cuda.is_available()
spacy_nlp = spacy.load('en_core_web_sm')


class Completor:
    def __init__(self, dataset_params, net, classes=5):
        self.net = net
        self.dataset_params = dataset_params
        self.dataset = AutoCompleteDataset(None, None, self.dataset_params)
        self.hidden = None
        self.backup_hidden = None
        self.last_word = ""
        self.classes = classes

    def add_letter(self, letter):
        if letter.isspace():
            self.last_word = ""
            self.hidden = self.backup_hidden
        else:
            self.last_word += letter
        return self.predict()

    def predict(self):
        x = np.array([self.last_word])
        inputs, dummy_target = self.dataset.get_encodes(x, False)
        inputs = torch.from_numpy(inputs.reshape(1, 1, -1))

        if (train_on_gpu):
            inputs = inputs.cuda()

        out, self.backup_hidden = self.net(inputs, self.hidden)
        # self.hidden = tuple([each.detach_() for each in self.hidden])

        if (train_on_gpu):
            out = out.cpu()  # move to cpu
        pred_classes = torch.topk(out, k=self.classes)[1].numpy().reshape(-1)

        return [self.dataset_params['int2word'][ind] for ind in pred_classes]


if __name__ == "__main__":
    PATH = "model/pretrained/best_test_autocomplete_model.net"
    dev = (torch.device('cpu') if not train_on_gpu else torch.device("cuda"))
    d = torch.load(PATH, map_location=dev)
    st_dict = d['model']
    params = d['dataset_params']
    params["embed"] = "data/big_vectors.bin"  # костиль (для кожної мережі додавати свій embed)

    model = SemiCharRNN(params, n_hidden=d['n_hidden'], n_layers=d['n_layers'])
    model.load_state_dict(st_dict)
    model.eval()

    if (train_on_gpu):
        model.cuda()
    else:
        model.cpu()

    cor = Completor(params, model, classes=5)

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
                    conn.sendto(str.encode(cor.add_letter(data.decode())), addr)