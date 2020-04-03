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
    def __init__(self, keyboardCheckHint, pred_hint):
        QThread.__init__(self)
        self.keyboardCheckHint = keyboardCheckHint
        self.pred_hint = pred_hint

    def __del__(self):
        self.wait()

    def run(self):
        support_correction = True
        support_completion = False

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
    if len(sys.argv) != 2:
        print("Invalid number of parameters")
        exit(-1)
    keyboardController = KeyboardController()
    with open(sys.argv[1], 'r') as f:
        loaded_json = json.load(f)
        keyboardController.process_configuration_file(loaded_json)

    keyboardController.set_layout(0)
    # keyboardCheckHint1 = KeyboardCheckHint(["111111111"])
    # keyboardCheckHint1.window_hide()
    # keyboardCheckHint2 = KeyboardCheckHint(["111111111", "22222222222222"])
    # keyboardCheckHint2.window_hide()
    # keyboardCheckHint3 = KeyboardCheckHint(["111111111", "22222222222222", "33333333333"])
    # keyboardCheckHint3.window_hide()
    # keyboardCheckHint4 = KeyboardCheckHint(["111111111", "22222222222222", "33333333333", "22222222222222"])
    # keyboardCheckHint4.window_hide()
    # keyboardCheckHint5 = KeyboardCheckHint(["111111111", "22222222222222", "33333333333", "22222222222222", "33333333333"])
    # keyboardCheckHint5.window_hide()
    #
    # predictionHint = PredictionHint("")
    # predictionHint.window_hide()

    # myThread = SupporterThread([keyboardCheckHint1, keyboardCheckHint2, keyboardCheckHint3, keyboardCheckHint4, keyboardCheckHint5], predictionHint)
    # myThread.start()
    app.exec_()
    # supporter = Supporter()
    # supporter.start_listen()
    # support_correction = True
    # support_completion = False
    #
    # supporter = None
    # if support_correction:
    #     supporter = SupporterCorrection()
    # if support_completion:
    #     supporter = SupporterCompletion()
    #     def process():
    #         supporter.chosen = True
    #         supporter._process_word()
    #
    #     keyboard.add_hotkey('ctrl+shift', process)
    # app.exec_()
    # print('starting...')
    # if supporter is not None:
    #     supporter.start_listen()