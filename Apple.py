import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT, SQUARE_SIZE


class Apple:
    def __init__(self, color):
        self.color = color
        self.new_coordinates()

    def new_coordinates(self):
        self.x = round(random.randrange(
            0, WINDOW_WIDTH - SQUARE_SIZE) / SQUARE_SIZE) * SQUARE_SIZE
        self.y = round(random.randrange(
            0, WINDOW_HEIGHT - SQUARE_SIZE) / SQUARE_SIZE) * SQUARE_SIZE
