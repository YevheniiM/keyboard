from BE.advanced_layout.KeyboardCheckHint import KeyboardCheckHint
from BE.library import keyboard


def setupHint(hints):
    keyboardCheckHint = KeyboardCheckHint(hints)
    keyboardCheckHint.window_show()
    keyboard.hook_key("down", keyboardCheckHint.activate_next_Button, suppress=True)
    keyboard.hook_key("up", keyboardCheckHint.activate_prev_Button, suppress=True)
    keyboard.hook_key("enter", keyboardCheckHint.set_active, suppress=True)
    keyboard.wait("esc", suppress=True)
    return keyboardCheckHint.get_active_index()
