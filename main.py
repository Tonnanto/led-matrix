from apps.move_square import MoveSquare
from displays.pygame_display import PyGameDisplay

from events.event import KeyboardEventProvider

# Constants
fps = 30

# Variables
running = True

# Components
event_provider = KeyboardEventProvider()
display = PyGameDisplay(64, 32)
app = MoveSquare(event_provider, display)


def mainloop():
    global running
    app_iterator = iter(app)
    display_iterator = iter(display)

    while running:

        try:
            next(app_iterator)
            next(display_iterator)
        except StopIteration:
            running = False

    if not running:
        print("QUITING APP")
        display.stop()


mainloop()
