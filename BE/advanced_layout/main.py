from BE.advanced_layout.KeyboardController import KeyboardController
import json
import sys

# from BE.advanced_layout.neural_network_support.SupporterCompletion import SupporterCompletion
from BE.advanced_layout.neural_network_support.SupporterCompletion import SupporterCompletion
from BE.advanced_layout.neural_network_support.SupporterCorrection import SupporterCorrection
from BE.library import keyboard

if __name__ == "__main__":
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

    if supporter is not None:
        print('starting...')
        supporter.start_listen()
