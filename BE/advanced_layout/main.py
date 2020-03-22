from KeyboardController import KeyboardController
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid number of parameters")
        exit(-1)
    keyboardController = KeyboardController()
    with open(sys.argv[1], 'r') as f:
        loaded_json = json.load(f)
        keyboardController.process_configuration_file(loaded_json)
    keyboardController.set_layout(1)
    while True:
        continue
