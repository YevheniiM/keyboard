from transformers import AutoModelWithLMHead, AutoTokenizer
import torch
import time

from BE.AI.client import run
from BE.library.keyboard import STOP_CHARACTERS

tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = AutoModelWithLMHead.from_pretrained("roberta-base")

import nltk

nltk.download('punkt')

from BE.library import keyboard


def send_to_network(char):
    corrected = run(char)
    return str(corrected)[2:-1]


class SupporterCompletion:
    def __init__(self, hint):
        self.sentence = ''
        self.chosen = False
        self.hint = hint
        send_to_network(' ')

    @staticmethod
    def _generate_events():
        while True:
            yield keyboard.read_event()

    def start_listen(self):
        characters = keyboard.get_typed_characters(SupporterCompletion._generate_events())
        while True:
            self.current_character = next(characters)
            self.sentence += self.current_character
            self._process_word()

    def _process_word(self):
        print(self.current_character)
        print('---------------')
        suggestion = send_to_network(self.current_character)
        print(suggestion)

        if self.current_character in STOP_CHARACTERS:
            self.sentence = ''
        #     # destroy window
        else:
            self.hint.change_text_hint(suggestion)
            self.hint.window_show()

            if self.chosen:
                for _ in self.sentence.split()[-1]:
                    keyboard.send('backspace')
                    time.sleep(0.01)
                    print('backspace pressed')

                for c in self.sentence + " " + suggestion:
                    keyboard.write(c)
                    time.sleep(0.01)

                self.chosen = False