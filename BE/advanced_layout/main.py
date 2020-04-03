import threading

from BE.advanced_layout.KeyboardController import KeyboardController
import json
import sys
from PyQt5.QtWidgets import *
from BE.advanced_layout.KeyboardHintController import setupHint
from BE.advanced_layout.KeyboardCheckHint import KeyboardCheckHint
from PyQt5.QtCore import QThread

from BE.advanced_layout.KeyboardHintController import setupHint
from BE.advanced_layout.neural_network_support.SupporterCompletion import SupporterCompletion
from BE.advanced_layout.neural_network_support.SupporterCorrection import SupporterCorrection
from BE.library import keyboard


class SupporterThread(QThread):
    def __init__(self, keyboardCheckHint):
        QThread.__init__(self)
        self.keyboardCheckHint = keyboardCheckHint

    def __del__(self):
        self.wait()

    def run(self):
        setupHint(self.keyboardCheckHint)


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
    

    support_correction = True
    support_completion = False

    supporter = None
    if support_correction:
        supporter = SupporterCorrection()
    if support_completion:
        supporter = SupporterCompletion()


        def process():
            supporter.chosen = True
            supporter._process_word()


        keyboard.add_hotkey('ctrl+shift', process)

    print("starting...")

    ///////////////////
    my_thread = threading.Thread(target=setupHint, args=(["11111", "22222", "33333"],))
    my_thread.start()
    keyboardCheckHint = KeyboardCheckHint(["111111111", "22222222222222", "33333333333"])
    myThread = SupporterThread(keyboardCheckHint)
    myThread.start()
    app.exec_()
    supporter = Supporter()
    supporter.start_listen()
    
    app.exec_()

    if supporter is not None:
        supporter.start_listen()
