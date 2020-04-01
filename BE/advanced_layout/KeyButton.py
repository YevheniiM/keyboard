import time
import keyboard


class KeyButton:
    def __init__(self, key, keys, delay):
        self.key = key
        self.keys = keys
        self.delay = delay
        self.start_time = -1
        self.current_key = 0

    def hook_multiple_press(self, event):
        if self.start_time == -1:
            self.start_time = time.time()
        elif event.event_type == 'down' and (time.time() - self.start_time) < self.delay:
            keyboard.send('backspace')
        elif event.event_type == 'up' and (time.time() - self.start_time) > self.delay:
            keyboard.send(self.keys[0])
            self.start_time = time.time()
            self.current_key = 1
        elif event.event_type == 'up' and (time.time() - self.start_time) < self.delay:
            keyboard.send(self.keys[self.current_key % len(self.keys)])
            self.current_key += 1
            self.start_time = time.time()

    def hook_long_press(self, event):
        if self.start_time == -1:
            self.start_time = time.time()
            keyboard.send(self.keys[self.current_key % len(self.keys)])
            self.current_key += 1
        elif event.event_type == 'down' and (time.time() - self.start_time) > self.delay:
            keyboard.send('backspace')
            keyboard.send(self.keys[self.current_key % len(self.keys)])
            self.start_time = time.time()
            self.current_key += 1
        elif event.event_type == 'up':
            self.start_time = -1
            self.current_key = 0
