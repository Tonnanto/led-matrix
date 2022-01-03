import numpy as np


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __iter__(self):
        pass

    def draw(self, color_matrix: np.array):
        pass

    def start(self):
        pass

    def stop(self):
        pass

