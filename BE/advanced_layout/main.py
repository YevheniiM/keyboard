from KeyboardController import KeyboardController
import json
import sys
from PyQt5.QtWidgets import *

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
    app.exec_()
