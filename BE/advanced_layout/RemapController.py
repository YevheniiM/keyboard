from BE.advanced_layout.KeyButton import KeyButton
from BE.library import keyboard


def add_remap_buttons(keymap, mode):
    for key in keymap:
        if mode['type'] == 'simple_press':
            keyboard.remap_key(key, keymap[key])
        else:
            keyButton = KeyButton(key, keymap[key], mode['value'])
            if mode['type'] == 'multiple_press':
                keyboard.hook_key(key, keyButton.hook_multiple_press, True)
            elif mode['type'] == 'long_press':
                keyboard.hook_key(key,  keyButton.hook_long_press, True)
