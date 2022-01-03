import numpy as np
import pygame
from displays.display import Display


class PyGameDisplay(Display):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.color_matrix = self.create_initial_color_matrix()
        self.prev_color_matrix = np.copy(self.color_matrix)
        self.pixel_size = 20
        self.running = True

        self.window = pygame.display.set_mode((width * self.pixel_size, height * self.pixel_size), pygame.DOUBLEBUF)

    def __iter__(self):
        while True:
            for y in range(self.height):
                if not np.array_equal(self.color_matrix[y], self.prev_color_matrix[y]):
                    for x in range(self.width):
                        if not np.array_equal(self.color_matrix[y][x], self.prev_color_matrix[y][x]):
                            color = self.color_matrix[y][x]
                            pygame.draw.rect(self.window, color,
                                             pygame.Rect(x * self.pixel_size, y * self.pixel_size,
                                                         self.pixel_size,
                                                         self.pixel_size))

            pygame.display.update()
            self.prev_color_matrix = np.copy(self.color_matrix)
            yield

    def create_initial_color_matrix(self) -> np.array:
        return np.zeros((self.height, self.width, 3))

    def draw(self, color_matrix: np.array):
        assert len(color_matrix) == self.height
        assert len(color_matrix[0]) == self.width

        self.prev_color_matrix = np.copy(self.color_matrix)
        self.color_matrix = color_matrix

    def stop(self):
        pygame.quit()
