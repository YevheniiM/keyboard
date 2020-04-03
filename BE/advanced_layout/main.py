from BE.advanced_layout.KeyboardController import KeyboardController
import json
import sys
from PyQt5.QtWidgets import *
from BE.advanced_layout.KeyboardHintController import setupHint
from BE.advanced_layout.KeyboardCheckHint import KeyboardCheckHint
from PyQt5.QtCore import QThread


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
    keyboardCheckHint = KeyboardCheckHint(["hello", "hi there", "lan davai"])
    myThread = SupporterThread(keyboardCheckHint)
    myThread.start()
    app.exec_()

