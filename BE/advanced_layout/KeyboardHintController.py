from BE.library import keyboard


def setupHint(keyboardCheckHints, hints):
    keyboardCheckHint = keyboardCheckHints[len(hints) - 1]
    keyboardCheckHint.set_new_hints(hints)
    keyboardCheckHint.window_show()
    key_down = keyboard.hook_key("down", keyboardCheckHint.activate_next_Button, suppress=True)
    key_up = keyboard.hook_key("up", keyboardCheckHint.activate_prev_Button, suppress=True)
    key_enter = keyboard.hook_key("enter", keyboardCheckHint.set_active, suppress=True)
    keyboard.wait("esc", suppress=True)
    keyboardCheckHint.window_hide()
    keyboard.unhook(key_down)
    keyboard.unhook(key_up)
    keyboard.unhook(key_enter)
    return keyboardCheckHint.get_active_index()
