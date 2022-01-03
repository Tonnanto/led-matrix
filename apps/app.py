from displays.display import Display
from events.event import EventListener, EventProvider, Event


class App(EventListener):

    def __init__(self, event_provider: EventProvider, display: Display):
        super().__init__()
        self.display = display
        event_provider.register_listener(self)
        self.running = True

    def __iter__(self):
        while self.running:
            while len(self.events) > 0:
                event = self.events.pop(0)
                self.on_event(event)

            self.tick()
            yield

    def tick(self):
        pass

    def on_event(self, event: Event):
        if event == Event.ESC:
            self.running = False


