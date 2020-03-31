from BE.advanced_layout.KeyboardController import KeyboardController
import json
import sys
import keyboard


def generate_events():
    while True:
        yield keyboard.read_event()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid number of parameters")
        exit(-1)
    keyboardController = KeyboardController()
    with open(sys.argv[1], 'r') as f:
        loaded_json = json.load(f)
        keyboardController.process_configuration_file(loaded_json)
    keyboardController.set_layout(0)
    strings = keyboard.get_typed_strings(generate_events())
    while True:
        print(next(strings))
