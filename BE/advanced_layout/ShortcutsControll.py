from BE.library import keyboard


def add_shortcuts(shortcuts):
    for shortcut in shortcuts:
        keyboard.remap_hotkey(shortcut, shortcuts[shortcut])


def add_abbreviations(abbreviations):
    for abbreviation in abbreviations:
        keyboard.add_abbreviation(abbreviation, abbreviations[abbreviation])


def remove_shortcuts_and_abbreviations():
    keyboard.unhook_all_hotkeys()


def add_access_with_hot_key(shortcut_keys):
    for shortcut_key in shortcut_keys:
        for shortcut in shortcut_keys[shortcut_key]:
            keyboard.remap_hotkey(shortcut_key + '+' + shortcut,
                                      shortcut_keys[shortcut_key][shortcut])


def add_control_shortcut(callback, len):
    for i in range(0, len):
        keyboard.add_hotkey('ctrl+{}'.format(i), callback, args=[i])
