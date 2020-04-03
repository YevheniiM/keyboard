from transformers import AutoModelWithLMHead, AutoTokenizer
import torch
import time

tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = AutoModelWithLMHead.from_pretrained("roberta-base")

import nltk

nltk.download('punkt')

from BE.library import keyboard
from BE.library.keyboard import STOP_CHARACTERS


def send_to_network(sentence):
    sequence = sentence + tokenizer.mask_token

    input_ = tokenizer.encode(sequence, return_tensors="pt")
    mask_token_index = torch.where(input_ == tokenizer.mask_token_id)[1]

    token_logits = model(input_)[0]
    mask_token_logits = token_logits[0, mask_token_index, :]

    token = torch.topk(mask_token_logits, 1, dim=1).indices[0].tolist()
    if not token:
        return

    return sequence.replace(tokenizer.mask_token, tokenizer.decode([token[0]])).split(' ')[-1]


class SupporterCompletion:
    def __init__(self):
        self.sentence_part = ''
        self.chosen = False

    @staticmethod
    def _generate_events():
        while True:
            yield keyboard.read_event()

    def start_listen(self):
        characters = keyboard.get_typed_characters(SupporterCompletion._generate_events())
        while True:
            self.sentence_part += next(characters)
            self._process_word()

    def _process_word(self):
        if self.sentence_part and self.sentence_part[-1] in STOP_CHARACTERS:
            print('cleaning...')
            self.sentence_part = ''
            # destroy window
        else:
            if self.chosen:
                print('sending: ', self.sentence_part)

                predicted_word = send_to_network(self.sentence_part)
                print('predicted: ', predicted_word)

                for _ in self.sentence_part.split(' ')[-1]:
                    keyboard.send('backspace')
                    time.sleep(0.01)

                keyboard.write(predicted_word)

                index = self.sentence_part.rfind(' ')
                self.sentence_part = self.sentence_part[:index]
                self.sentence_part += predicted_word
                self.chosen = False

