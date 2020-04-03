import time

from BE.advanced_layout.KeyHint import KeyHint

from BE.library import keyboard


class KeyButton:
    def __init__(self, key, keys, delay):
        self.key = key
        self.keys = keys
        self.delay = delay
        self.start_time = -1
        self.current_key = 0
        self.hint = KeyHint(self.keys)
        self.hint.window_hide()
        self.is_fist_time_press = True

    def hook_multiple_press(self, event):
        if self.start_time == -1:
            self.start_time = time.time()
            self.hint.window_show()
            keyboard.send(self.keys[0])
        elif event.event_type == 'down' and (time.time() - self.start_time) < self.delay:
            self.hint.window_show()
        elif event.event_type == 'up' and (time.time() - self.start_time) > self.delay:
            keyboard.send(self.keys[0])
            self.hint.window_hide()
            self.start_time = time.time()
            self.current_key = 1
        elif event.event_type == 'up' and (time.time() - self.start_time) < self.delay:
            keyboard.send('backspace')
            keyboard.send(self.keys[self.current_key % len(self.keys)])
            self.hint.window_hide()
            self.hint.activate_next_Button()
            self.current_key += 1
            self.start_time = time.time()

    def hook_long_press(self, event):
        if self.start_time == -1:
            self.start_time = time.time()
            keyboard.send(self.keys[self.current_key % len(self.keys)])
            self.hint.window_show()
            self.current_key += 1
        elif event.event_type == 'down' and (time.time() - self.start_time) > self.delay:
            keyboard.send('backspace')
            keyboard.send(self.keys[self.current_key % len(self.keys)])
            self.hint.activate_next_Button()
            self.start_time = time.time()
            self.current_key += 1
        elif event.event_type == 'up':
            self.hint.window_hide()
            self.start_time = -1
            self.current_key = 0
