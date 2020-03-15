import json
from enum import Enum


class HotKey:
    def __init__(self, name, keys):
        """

        :type keys: dict {char, char}
        :type name: str
        """
        self.name = name
        self.keys = keys


class Shortcut:
    def __init__(self, original, remapped):
        """

        :type remapped: str (keys separated with + sign)
        :type original: str (keys separated with + sign)
        """
        self.original = original
        self.remapped = remapped


class KeyString:
    def __init__(self, abbreviation, string):
        """

        :type string: str
        :type abbreviation: str
        """
        self.abbreviation = abbreviation
        self.string = string


class Key:
    def __init__(self, original, remapped):
        """

        :type remapped: list[char]
        :type original: char
        """
        self.original = original
        self.remapped = remapped


class Command:
    def __init__(self, name, command):
        self.name = name
        self.command = command


class Mode:
    class Type(Enum):
        LONG_PRESS = 1
        MULTIPLE_PRESS = 2

    def __init__(self, mode, value):
        """

        :type value: int
        :type mode: Mode.Type
        """
        self.mode = mode
        self.value = value


class Layout:
    def __init__(self, access_with_hot_keys, shortcuts, key_strings, key_map, commands, mode):
        """

        :type mode: Mode
        :type commands: list[command]
        :type key_map: list[Key]
        :type key_strings: list[KeyString]
        :type shortcuts: list[Shortcut]
        :type access_with_hot_keys: list[HotKey]
        """
        self.key_map = key_map
        self.commands = commands
        self.mode = mode
        self.access_with_hot_keys = access_with_hot_keys
        self.shortcuts = shortcuts
        self.key_strings = key_strings


class Configuration:
    FILE_PATH = 'BE/advanced_layout/helpers/configuration.json'

    def __init__(self, layouts):
        """

        :type layouts: list[Layout]
        """
        self.layouts = layouts

    def __read_config(self):
        data = json.load(self.FILE_PATH)

        process_id = data['id']
        layouts_count = len(data['layouts'])

        if layouts_count < 1:
            raise Exception

        for layout in data['layouts']:
            pass
