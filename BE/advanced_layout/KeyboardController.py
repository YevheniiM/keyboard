from ShortcutsControll import add_shortcuts, add_abbreviations, remove_shortcuts_and_abbreviations, \
    add_control_shortcut, add_access_with_hot_key
from RemapController import add_remap_buttons


class KeyboardController:
    def __init__(self, configuration_file=None):
        self.id = 0
        self.layouts = []
        self.last_layout = 0
        self.process_configuration_file(configuration_file)
        self.configuration_file = configuration_file

    def process_configuration_file(self, configuration_file=None):
        if configuration_file is None:
            return
        self.id = configuration_file['id']
        self.layouts.clear()
        for layout in configuration_file['layouts']:
            self.layouts.append(layout)

    def set_layout(self, index):
        try:
            self.__clear_keyboard_configuration()
        except:
            pass
        self.last_layout = index
        self.__install_keyboard_configuration()

    def __clear_keyboard_configuration(self):
        remove_shortcuts_and_abbreviations()

    def __install_keyboard_configuration(self):
        add_remap_buttons(self.layouts[self.last_layout]['keymap'], self.layouts[self.last_layout]['mode'])
        add_shortcuts(self.layouts[self.last_layout]['shortcuts'])
        add_access_with_hot_key(self.layouts[self.last_layout]['access_with_hot_key'])
        add_abbreviations(self.layouts[self.last_layout]['key_strings'])
        add_control_shortcut(self.set_layout, len(self.layouts))
