import re
import string
import time

from BE.AI.client import run

import nltk

from BE.advanced_layout.KeyboardHintController import setupHint
from BE.library import keyboard
from BE.library.keyboard import STOP_CHARACTERS

nltk.download('punkt')


def send_to_network(sentence):
    corrected = run(sentence)
    print(str(corrected)[2:-1])
    return str(corrected)[2:-1]


class SupporterCorrection:
    def __init__(self, hint):
        self.current_string = ''
        self.hint = hint

    def start_listen(self):
        characters = keyboard.get_typed_characters(SupporterCorrection._generate_events())
        while True:
            self.current_string += next(characters)
            self.check_current_string()

    def check_current_string(self):
        if self.current_string[-1] in STOP_CHARACTERS:
            self._process_string()
            self.current_string = ''

    def _process_string(self):
        words = re.findall(r'\w+', self.current_string)
        words_with_punct = re.findall(r"[\w']+|[.,!?;]", self.current_string)

        corrected_sentence = send_to_network(' '.join(words))
        corrected_words = corrected_sentence.split(' ')

        assert len(corrected_words) == len(words)

        to_correct = []
        for i in range(len(corrected_words)):
            if corrected_words[i] != words[i]:
                to_correct.append(corrected_words[i])

        # ЗЕНИК, ТУТ ТВОЯ ФУНКЦІЯ З ВІКОНЦЕМ
        chosen = setupHint(self.hint, to_correct)

        chosen_real_indexes = []
        for i in chosen:
            if len(to_correct) > i:
                chosen_real_indexes.append(corrected_words.index(to_correct[i]))

        final = ''

        for i in range(len(words_with_punct)):
            whitespace = ' ' if i != 0 else ''
            if words_with_punct[i] in string.punctuation:
                final += words_with_punct[i]
            else:
                word_index = words.index(words_with_punct[i])

                if word_index in chosen_real_indexes:
                    final += whitespace + corrected_words[word_index]
                else:
                    final += whitespace + words[word_index]

        self._replace_with_final(final)

        print(final)

    def _replace_with_final(self, final):
        for _ in self.current_string:
            keyboard.send('backspace')
            time.sleep(0.01)
        for i in final:
            keyboard.write(i)
            time.sleep(0.01)

    @staticmethod
    def _generate_events():
        while True:
            yield keyboard.read_event()
