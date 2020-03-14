import time

from BE.library import keyboard


def generate_events():
    while True:
        yield keyboard.read_event()


strings = keyboard.get_typed_strings(generate_events())
while True:
    print(next(strings))
