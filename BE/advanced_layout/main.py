from BE.advanced_layout.KeyboardController import KeyboardController
import json
import sys
from PyQt5.QtWidgets import *
from BE.advanced_layout.KeyboardHintController import setupHint
from BE.advanced_layout.KeyboardCheckHint import KeyboardCheckHint
from PyQt5.QtCore import QThread

from BE.advanced_layout.PredictionHint import PredictionHint
from BE.advanced_layout.neural_network_support.SupporterCompletion import SupporterCompletion
from BE.advanced_layout.neural_network_support.SupporterCorrection import SupporterCorrection
from BE.library import keyboard


class SupporterThread(QThread):
    def __init__(self, keyboardCheckHint, pred_hint, neuro=None):
        QThread.__init__(self)
        self.keyboardCheckHint = keyboardCheckHint
        self.pred_hint = pred_hint
        self.neuro = neuro

    def __del__(self):
        self.wait()

    def run(self):
        if self.neuro == "correction":
            support_correction = True
            support_completion = False
        elif self.neuro == "completion":
            print("COMPLETION")
            support_correction = False
            support_completion = True

        supporter = None
        if support_correction:
            supporter = SupporterCorrection(self.keyboardCheckHint)
        if support_completion:
            supporter = SupporterCompletion(self.pred_hint)

            def process():
                supporter.chosen = True
                supporter._process_word()

            keyboard.add_hotkey('ctrl+shift', process)

        if supporter is not None:
            print('starting in a new thread...')
            supporter.start_listen()


if __name__ == "__main__":
    app = QApplication([])

    keyboardController = KeyboardController()
    NEURO = ''
    with open(r"D:\Study\AI_Competition\keyboard\BE\advanced_layout\helpers\config.json", 'r') as f:
        loaded_json = json.load(f)
        keyboardController.process_configuration_file(loaded_json)

        ai = loaded_json['layouts'][0]['ai']
        if ai['correction']:
            NEURO = 'correction'
        elif ai['completion']:
            NEURO = 'completion'

    if not NEURO:
        print('setting')
        keyboardController.set_layout(0)
    else:
        keyboardCheckHint1 = KeyboardCheckHint(["111111111"])
        keyboardCheckHint1.window_hide()
        keyboardCheckHint2 = KeyboardCheckHint(["111111111", "22222222222222"])
        keyboardCheckHint2.window_hide()
        keyboardCheckHint3 = KeyboardCheckHint(["111111111", "22222222222222", "33333333333"])
        keyboardCheckHint3.window_hide()
        keyboardCheckHint4 = KeyboardCheckHint(["111111111", "22222222222222", "33333333333", "22222222222222"])
        keyboardCheckHint4.window_hide()
        keyboardCheckHint5 = KeyboardCheckHint(
            ["111111111", "22222222222222", "33333333333", "22222222222222", "33333333333"])
        keyboardCheckHint5.window_hide()

        predictionHint = PredictionHint("")
        predictionHint.window_hide()

        myThread = SupporterThread(
            [keyboardCheckHint1, keyboardCheckHint2, keyboardCheckHint3, keyboardCheckHint4, keyboardCheckHint5],
            predictionHint,
            neuro=NEURO)
        myThread.start()

    app.exec_()
