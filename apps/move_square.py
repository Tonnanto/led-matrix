import numpy as np

from apps.app import App
from displays.color import Colors
from displays.display import Display
from events.event import EventProvider, Event


class MoveSquare(App):

    def __init__(self, event_provider: EventProvider, display: Display):
        super().__init__(event_provider, display)
        self.needs_redraw = True
        self.square_pos = [0, 0]
        self.board_height = self.display.height
        self.board_width = self.display.width

    def tick(self):
        super().tick()

        if self.needs_redraw:
            color_matrix = np.zeros((self.display.height, self.display.width, 3))
            color_matrix[self.square_pos[1]][self.square_pos[0]] = Colors.RED

            self.display.draw(np.array(color_matrix))
            self.needs_redraw = False

    def on_event(self, event: Event):
        super().on_event(event)
        if event == Event.UP:
            self.square_pos[1] = (self.square_pos[1] - 1) % self.board_height
        if event == Event.DOWN:
            self.square_pos[1] = (self.square_pos[1] + 1) % self.board_height
        if event == Event.RIGHT:
            self.square_pos[0] = (self.square_pos[0] + 1) % self.board_width
        if event == Event.LEFT:
            self.square_pos[0] = (self.square_pos[0] - 1) % self.board_width

        self.needs_redraw = True
