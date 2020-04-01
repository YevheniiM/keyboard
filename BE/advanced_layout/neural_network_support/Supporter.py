import re
import string
import time
from typing import Optional

import nltk

nltk.download('punkt')

from BE.library import keyboard
from BE.library.keyboard import STOP_CHARACTERS


def send_to_network(sentence):
    arr = sentence.split(' ')
    new_arr = [i + '_corrected' for i in arr]
    return ' '.join(new_arr)


def choose_what_correct(corrected_words):
    # повертає ті індекси, які треба виправити або None, якщо не треба
    return 1, 3, 5


class Supporter:
    def __init__(self):
        self.current_string = ''

    def start_listen(self):
        characters = keyboard.get_typed_characters(Supporter._generate_events())
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

        # ЗЕНИК, ТУТ ТВОЯ ФУНКЦІЯ З ВІКОНЦЕМ
        to_correct = choose_what_correct(corrected_words)
        final = ''

        for i in range(len(words_with_punct)):
            whitespace = ' ' if i != 0 else ''
            if words_with_punct[i] in string.punctuation:
                final += words_with_punct[i]
            else:
                word_index = words.index(words_with_punct[i])

                if word_index in to_correct:
                    final += whitespace + corrected_words[word_index]
                else:
                    final += whitespace + words[word_index]

        self._replace_with_final(final)

        print(final)

    def _replace_with_final(self, final):
        for i in self.current_string:
            keyboard.send('backspace')
            time.sleep(0.01)
        for i in final:
            keyboard.write(i)
            time.sleep(0.01)

    @staticmethod
    def _generate_events():
        while True:
            yield keyboard.read_event()