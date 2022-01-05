import time
from enum import Enum
from random import randrange

import numpy
import numpy as np

from apps.app import App
from displays.color import Colors
from displays.display import Display
from events.event import EventProvider, Event
from PIL import Image, ImageDraw, ImageFont


class SnakeDirection(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class SnakeApp(App):

    def __init__(self, event_provider: EventProvider, display: Display):
        super().__init__(event_provider, display)
        self.score = 0
        self.snake_direction = SnakeDirection.RIGHT
        self.snake_pos = [(0, 0)]
        self.snake_color = Colors.GREEN
        self.snake_head_color = np.array((0, 120, 120))
        self.snake_delay = 0.1
        self.timestamp = time.time()
        self.food_pos = None
        self.food_color = Colors.RED
        self.game_over = False  # True
        # self.pending_moves = []

    def tick(self):

        if self.game_over:
            self.game_over_sequence()

        elif time.time() - self.timestamp > self.snake_delay:
            self.move()
            self.draw_snake()

            if self.food_pos is None:
                self.spawn_food()

            self.timestamp = time.time()

    def draw_snake(self):
        color_matrix = np.zeros((self.display.height, self.display.width, 3))
        for pos in self.snake_pos:
            color_matrix[pos[1]][pos[0]] = self.snake_color

        if self.food_pos is not None:
            color_matrix[self.food_pos[1]][self.food_pos[0]] = self.food_color

        self.display.draw(np.array(color_matrix))

    def move(self):
        assert len(self.snake_pos) > 0

        x = None
        y = None

        direction = self.snake_direction
        # if len(self.pending_moves) > 0:
        #     direction = self.direction_from_event(self.pending_moves.pop())

        if direction == SnakeDirection.RIGHT:
            x = self.snake_pos[0][0] + 1
            y = self.snake_pos[0][1]
        if direction == SnakeDirection.LEFT:
            x = self.snake_pos[0][0] - 1
            y = self.snake_pos[0][1]
        if direction == SnakeDirection.UP:
            x = self.snake_pos[0][0]
            y = self.snake_pos[0][1] - 1
        if direction == SnakeDirection.DOWN:
            x = self.snake_pos[0][0]
            y = self.snake_pos[0][1] + 1

        x %= self.display.width
        y %= self.display.height
        new_pos = (x, y)

        self.snake_pos.insert(0, new_pos)

        if new_pos == self.food_pos:
            # eat food
            self.food_pos = None
            self.score += 1

        elif new_pos in self.snake_pos[1:]:
            print(new_pos)
            print(self.snake_pos)
            # eat self -> game over
            self.game_over = True

        else:
            # continue
            del self.snake_pos[-1]

    def on_event(self, event: Event):
        super().on_event(event)
        # if len(self.pending_moves) > 0:
        #     self.pending_moves.append(event)
        #     return

        self.change_direction(event)

    def change_direction(self, event: Event):
        if event == Event.UP and self.snake_direction is not SnakeDirection.DOWN:
            self.snake_direction = SnakeDirection.UP
        if event == Event.DOWN and self.snake_direction is not SnakeDirection.UP:
            self.snake_direction = SnakeDirection.DOWN
        if event == Event.RIGHT and self.snake_direction is not SnakeDirection.LEFT:
            self.snake_direction = SnakeDirection.RIGHT
        if event == Event.LEFT and self.snake_direction is not SnakeDirection.RIGHT:
            self.snake_direction = SnakeDirection.LEFT

    def spawn_food(self):
        assert self.food_pos is None
        x = randrange(self.display.width)
        y = randrange(self.display.height)

        if (x, y) in self.snake_pos:
            self.spawn_food()
            return

        self.food_pos = (x, y)

    def game_over_sequence(self):
        text = f'Score: {self.score}'
        # img = Image.new('RGB', (self.display.width, self.display.height))

        font = ImageFont.truetype("arialbd.ttf", 14)

        w, h = font.getsize(text)
        h *= 2
        image = Image.new('L', (w, h), 1)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font)
        # draw.text((32, 8), 'Game', font=font)
        # draw.text((32, 24), 'Over!', font=font)

        arr = np.asarray(image)
        arr = np.where(arr, 0, 1)
        arr = arr[(arr != 0).any(axis=1)]

        # print(arr)
        result = np.where(arr, 1, 0)
        # print('\n'.join([''.join(row) for row in result]))

        # d = ImageDraw.Draw(img)
        # d.text((32, 8), 'Game', (255, 0, 0), align='center', anchor='mm', font=font, stroke_width=0)
        # d.text((32, 24), 'Over!', (255, 0, 0), align='center', anchor='mm', font=font)
        # px = image.load()

        display_matrix = np.zeros((self.display.height, self.display.width))
        color_matrix = np.zeros((self.display.height, self.display.width, 3))

        display_matrix[0:result.shape[0], 0:result.shape[1]] = result

        for y in range(self.display.height):
            for x in range(self.display.width):
                color_matrix[y][x] = (255, 0, 0) if display_matrix[y][x] else (0, 0, 0)

        self.display.draw(np.array(color_matrix))
