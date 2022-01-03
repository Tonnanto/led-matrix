from enum import Enum

from pynput import keyboard


class Event(Enum):
    ESC = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class EventProvider:

    def __init__(self):
        self.listeners = []

    def register_listener(self, listener):
        self.listeners.append(listener)

    def post_event(self, event):
        for listener in self.listeners:
            listener.notify(event)


class EventListener:

    def __init__(self):
        self.events = []

    def notify(self, event):
        self.events.append(event)


class KeyboardEventProvider(EventProvider):

    def __init__(self):
        super().__init__()
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()  # start to listen on a separate thread

    def on_press(self, key):
        if key == keyboard.Key.esc:
            self.post_event(Event.ESC)
            # return False  # stop listener

        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys

        if k in ['up', 'down', 'left', 'right']:
            if k == 'up':
                self.post_event(Event.UP)
            elif k == 'down':
                self.post_event(Event.DOWN)
            elif k == 'left':
                self.post_event(Event.LEFT)
            elif k == 'right':
                self.post_event(Event.RIGHT)
