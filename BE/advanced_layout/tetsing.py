import time

from BE.library import keyboard


def generate_events():
    while True:
        yield keyboard.read_event()


strings = keyboard.get_typed_strings(generate_events())
while True:
    print(next(strings))

# def get_value(char):
#     keyboard.send('backspace')
#     keyboard.write('b')
#
#
# keyboard.remap_hotkey('ctrl+a', 'q')
# # keyboard.add_hotkey('a', get_value, args=['b'])
# keyboard.wait()
