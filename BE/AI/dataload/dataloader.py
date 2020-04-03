import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
import nlpaug.augmenter.char as nac
import fasttext
import spacy
import gensim
from gensim.models.wrappers import FastText
from torch.utils import data
import string

from bpemb import BPEmb



class SemicharDataset(data.Dataset):
    def __init__(self, root_path, seq_length, predefined=False):
        
        """Initialize the dataset"""
        if not predefined:
            self.chars = None
            self.root_path = root_path
            self.seq_length = seq_length
            self.tokenized_data = self.tokenize(root_path)
            self.tokenized_data = self.tokenized_data[:len(self.tokenized_data) - len(self.tokenized_data) % self.seq_length]
            self.data = np.array(self.tokenized_data).reshape(-1, seq_length)


            self.int2char = dict(enumerate(self.chars))
            self.char2int = {ch: ii for ii, ch in self.int2char.items()}

            self.words = tuple(set(self.tokenized_data))
            self.int2word = dict(enumerate(self.words))
            self.word2int = {ch: ii for ii, ch in self.int2word.items()}
            self.augmentator = nac.KeyboardAug(aug_char_min=0, aug_char_p=0.4, aug_word_p=0.4, aug_word_min=0,
                                    aug_word_max= int(0.7*self.seq_length), special_char=False, tokenizer = lambda x: x.split(), reverse_tokenizer = lambda x: x)
            
        else: 
            self.int2char = predefined["int2char"]
            self.char2int = predefined["char2int"]

            self.words = predefined["words"]
            self.int2word = predefined["int2word"]
            self.word2int = predefined["word2int"]
            self.chars = predefined["chars"]

    def tokenize(self, root_path):
        with open(root_path, 'r') as f:
            text = f.read()
            self.chars = tuple(set(text))

        spacy_nlp = spacy.load('en_core_web_sm')
        spacy_nlp.max_length = 2 * len(text)

        x = spacy_nlp(text, disable=['parser', 'tagger', 'ner'])
        splitted = [token.text for token in x if
                    not (token.text.isspace() or (token.text[0].isdigit() and token.text[-1].isdigit()) or (token.text[0] in string.punctuation and token.text[-1] in string.punctuation))]
        return splitted

    def one_hot_encode(self, arr, n_labels):
        one_hot = np.zeros((arr.size, n_labels), dtype=np.float32)

        # Fill the appropriate elements with ones
        one_hot[np.arange(one_hot.shape[0]), arr.flatten()] = 1.

        # Finally reshape it to get back to the original array
        one_hot = one_hot.reshape((*arr.shape, n_labels))

        return one_hot

    def middle_embedding(self, word, n_labels):
        return np.sum(self.one_hot_encode(word[1:-1], n_labels), axis=0)

    def augment(self, arr):
        augmented_data = self.augmentator.augment(" ".join(arr.ravel().tolist()))
        return np.array(augmented_data).reshape(arr.shape)

    def get_encodes(self, arr, use_aug=True):
        if use_aug:
            arr = self.augment(arr)
        

        flat_arr = arr.ravel()
        splitted_encoded = np.array(list(map(lambda x: np.array([self.char2int[ch] for ch in x]), flat_arr)))

        first_char = list(map(lambda x: x[0], splitted_encoded))
        last_char = list(map(lambda x: x[-1], splitted_encoded))
        middle = splitted_encoded

        first_char_encoded = self.one_hot_encode(np.array(first_char), len(self.chars))
        last_char_encoded = self.one_hot_encode(np.array(last_char), len(self.chars))

        middle_encoded = np.vstack(list(map(lambda x: self.middle_embedding(x, len(self.chars)), middle)))
        encoded_seq = np.hstack([first_char_encoded, middle_encoded, last_char_encoded]).reshape(
            (*arr.shape, 3 * len(self.chars)))
        return encoded_seq

    def get_int(self, x):
        return self.word2int[x]

    def get_params(self):
      param_dict = dict()

      param_dict["chars"] = self.chars
      param_dict["int2char"] = self.int2char
      param_dict["char2int"] = self.char2int
      param_dict["words"] = self.words
      param_dict["int2word"] = self.int2word
      param_dict["word2int"] = self.word2int

      return param_dict

    def __len__(self):
        return np.shape(self.data)[0]

    def __getitem__(self, index):
        sequence = self.data[index]
        X = self.get_encodes(sequence.copy())
        y = np.vectorize(self.get_int)(sequence)
        return torch.from_numpy(X), torch.from_numpy(y)








class seq2seqDataset(data.Dataset):
    def __init__(self, root_path, seq_length, embed_dim, embed_vec_space):
        """Initialize the dataset"""

        self.root_path = root_path
        self.seq_length = seq_length
        self.tokenized_data = self.tokenize(root_path)
        self.embed = BPEmb(lang="en", vs=embed_vec_space, add_pad_emb=True)
        self.pad = 1002
        self.sos = 1001
        self.eos = 1000

        self.augmentator = nac.KeyboardAug(aug_char_min=0, aug_char_p=0.4, aug_word_p=0.5, aug_word_min=0,
                                 aug_word_max=self.seq_length // 5, special_char=False)
        


    def tokenize(self, root_path):
  
        with open(root_path, 'r') as f:
            text = f.read()
        lt = len(text)
        print(lt)

        splitted = []
        start = 0

        while True:

          flag = (1 if self.seq_length >= lt - start else 0)
          if lt <= start:
            break
          cur_text = text[start: start + min(self.seq_length, lt - start)]
          last_chunk_len = None
          try:
            last_chunk_len = (0 if cur_text[-1].isspace() else len(cur_text.split()[-1]))
          except:
            print(cur_text)
            start += self.seq_length
            continue
          start += self.seq_length - last_chunk_len

          if last_chunk_len == len(cur_text.strip()):
            start += self.seq_length
            continue
          st = cur_text[:-last_chunk_len].strip()
          if st == st.swapcase():
            start += self.seq_length
            continue
          splitted.append(st)

          if flag:
            break

        return splitted
    # def one_hot_encode(self, arr, n_labels):
    #     one_hot = np.zeros((arr.size, n_labels), dtype=np.float32)

    #     # Fill the appropriate elements with ones
    #     one_hot[np.arange(one_hot.shape[0]), arr.flatten()] = 1.

    #     # Finally reshape it to get back to the original array
    #     one_hot = one_hot.reshape((*arr.shape, n_labels))

        # return one_hot
    def augment(self, seq):

        augmented_data = self.augmentator.augment(seq)
        return seq

    def get_encodes(self, seq, use_aug=False):
        if use_aug:
            seq = self.augment(seq)
        

        def padded_encode(x):
            
            res = np.full((self.seq_length, self.embed.dim), self.embed['<pad>']) 
            res1hot = np.full((self.seq_length), self.pad, dtype=np.int32)
            enc = self.embed.encode_ids(x)

            res[:len(enc)] = self.embed.vectors[enc]  
            res1hot[:len(enc)] = np.array(enc)
            length = len(enc)
            
            res = np.insert(res, 0, np.full((self.embed.dim), self.sos), 0)  
            
            length += 1
            if use_aug:
              res = np.insert(res, length, np.full((self.embed.dim), self.eos), 0)
              length += 1             

              return length, res
            res1hot = np.insert(res1hot, length, self.eos, 0)
            return length, res, res1hot
  

                  
      

        return padded_encode(seq)
    def get_params(self):
        return None 

    def __len__(self):
        return len(self.tokenized_data)

    def __getitem__(self, index):
        sequence = self.tokenized_data[index]
        
        lengths_x, X = self.get_encodes(sequence, use_aug=True)
        lengths_y, Y, y1hot = self.get_encodes(sequence)
        
        return lengths_x, torch.from_numpy(X), lengths_y, torch.from_numpy(Y), torch.from_numpy(y1hot)


if __name__ == '__main__':
    ds = seq2seqDataset("data/big.txt", 40, 1000, 50)
