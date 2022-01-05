import time
from enum import IntEnum
from random import randrange

import numpy as np

from apps.app import App
from displays.color import Colors
from displays.display import Display
from events.event import EventProvider, Event
from PIL import Image, ImageDraw, ImageFont


class SnakeDirection(IntEnum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class SnakeApp(App):

    HIGH_SCORE = 128  # Bot

    def __init__(self, event_provider: EventProvider, display: Display):
        super().__init__(event_provider, display)
        self.score = 0
        self.snake_direction = SnakeDirection.RIGHT
        self.snake_pos = [(0, 0)]
        self.snake_color = Colors.GREEN
        self.snake_head_color = np.array((0, 120, 120))
        self.snake_delay = 0
        self.timestamp = time.time()
        self.food_pos = None
        self.food_color = Colors.RED
        self.game_over = False  # True
        self.pending_moves = []
        self.snake_bot = True

    def tick(self):

        if self.game_over:
            if self.score > SnakeApp.HIGH_SCORE:
                SnakeApp.HIGH_SCORE = self.score
            self.game_over_sequence()
            self.restart()

        elif time.time() - self.timestamp > self.snake_delay:

            if self.food_pos is None:
                self.spawn_food()

            self.change_direction()
            self.move()

            self.draw_snake()

            self.timestamp = time.time()

    def draw_snake(self):
        color_matrix = np.zeros((self.display.height, self.display.width, 3))
        for pos in self.snake_pos:
            color_matrix[pos[1]][pos[0]] = self.snake_color

        if self.food_pos is not None:
            color_matrix[self.food_pos[1]][self.food_pos[0]] = self.food_color

        self.display.draw(np.array(color_matrix))

    def change_direction(self):
        if self.snake_bot:
            self.bot_direction()

        if len(self.pending_moves) > 0:
            self.snake_direction = self.pending_moves.pop()

    def move(self):
        new_pos = self.adjacent_pos(self.snake_direction)

        self.snake_pos.insert(0, new_pos)

        if new_pos == self.food_pos:
            # eat food
            self.food_pos = None
            self.score += 1

        elif new_pos in self.snake_pos[1:]:
            # eat self -> game over
            self.game_over = True

        else:
            # continue
            del self.snake_pos[-1]

    def on_event(self, event: Event):
        super().on_event(event)
        if event == Event.UP and self.snake_direction is not SnakeDirection.DOWN:
            self.pending_moves.append(SnakeDirection.UP)
        if event == Event.DOWN and self.snake_direction is not SnakeDirection.UP:
            self.pending_moves.append(SnakeDirection.DOWN)
        if event == Event.RIGHT and self.snake_direction is not SnakeDirection.LEFT:
            self.pending_moves.append(SnakeDirection.RIGHT)
        if event == Event.LEFT and self.snake_direction is not SnakeDirection.RIGHT:
            self.pending_moves.append(SnakeDirection.LEFT)
        self.pending_moves.append(event)

    def bot_direction(self):
        snake_pos = self.snake_pos[0]
        food_pos = self.food_pos

        new_direction = self.snake_direction

        # if snake_pos[0] is not food_pos[0]:
        if snake_pos[0] - food_pos[0] > 0 and self.snake_direction is not SnakeDirection.RIGHT:
            new_direction = SnakeDirection.LEFT
        elif snake_pos[0] - food_pos[0] < 0 and self.snake_direction is not SnakeDirection.LEFT:
            new_direction = SnakeDirection.RIGHT

        # if snake_pos[1] is not food_pos[1]:
        elif snake_pos[1] - food_pos[1] > 0 and self.snake_direction is not SnakeDirection.DOWN:
            new_direction = SnakeDirection.UP
        elif snake_pos[1] - food_pos[1] < 0 and self.snake_direction is not SnakeDirection.UP:
            new_direction = SnakeDirection.DOWN

        i = 0
        while self.adjacent_pos(new_direction) in self.snake_pos:
            new_direction = ((new_direction + 1) % 4)
            i += 1
            if i >= 4:
                break

        self.pending_moves.append(new_direction)

    # returns the position next to the snake head in the given direction
    def adjacent_pos(self, direction):
        assert len(self.snake_pos) > 0

        x = None
        y = None

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
        return x, y

    def spawn_food(self):
        assert self.food_pos is None
        x = randrange(self.display.width)
        y = randrange(self.display.height)

        if (x, y) in self.snake_pos:
            self.spawn_food()
            return

        self.food_pos = (x, y)

    def restart(self):
        self.score = 0
        self.snake_pos = [(0, 0)]
        self.game_over = False

    def game_over_sequence(self):
        text = f'Score: {self.score}'
        # img = Image.new('RGB', (self.display.width, self.display.height))

        font = ImageFont.truetype("arialbd.ttf", 10)

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
        print(f'Score: {self.score}')
        print(f'High Score: {SnakeApp.HIGH_SCORE}')
        # time.sleep(1)
