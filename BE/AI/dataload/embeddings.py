import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
import nlpaug.augmenter.char as nac
import fasttext
import spacy
import gensim
from gensim.models.wrappers import FastText



# def one_hot_embedding(word, n_labels):
#     return np.sum(one_hot_encode(word[1:-1], n_labels), axis=0)
#
#
# def get_encodes(arr, use_aug=False):
#     if use_aug:
#         aug_rr = nac.KeyboardAug(aug_char_min=0, aug_char_max=None, aug_char_p=0.4, aug_word_p=0.4, aug_word_min=0,
#                                  aug_word_max=arr.size // 3, special_char=False)
#         augmented_data = aug_rr.augment(" ".join(arr.ravel().tolist())).split()
#         arr = np.array(augmented_data).reshape(arr.shape)
#
#     flat_arr = arr.ravel()
#     splitted_encoded = np.array(list(map(lambda x: np.array([char2int[ch] for ch in x]), flat_arr)))
#
#     first_char = list(map(lambda x: x[0], splitted_encoded))
#     last_char = list(map(lambda x: x[-1], splitted_encoded))
#     middle = list(map(lambda x: x, splitted_encoded))
#
#     first_char_encoded = one_hot_encode(np.array(first_char), len(chars))
#     last_char_encoded = one_hot_encode(np.array(last_char), len(chars))
#
#     middle_encoded = np.vstack(list(map(lambda x: one_hot_embedding(x, len(chars)), middle)))
#     encoded_seq = np.hstack([first_char_encoded, middle_encoded, last_char_encoded]).reshape(
#         (*arr.shape, 3 * len(chars)))
#     return encoded_seq
#
#
# def get_int(x):
#     return word2int[x]

