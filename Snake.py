from config import *


class Snake:
    x = None
    y = None
    dx = None
    dy = None
    color = None
    snakebits = []

    def __init__(self, dx, dy, color, xPos, yPos, length):
        self.dx = dx
        self.dy = dy
        self.x = xPos,
        self.y = yPos,
        self.color = color
        for x in range(xPos, xPos + length, SQUARE_SIZE):
            self.snakebits.append(SnakeBit(x, yPos))

    # Move by removing the tail and adding a new bit in front of the head
    def move(self, apple_eaten):
        if not apple_eaten:
            del self.snakebits[-1]

        newX = self.snakebits[0].xPos + self.dx * SQUARE_SIZE
        newY = self.snakebits[0].yPos + self.dy * SQUARE_SIZE
        self.snakebits.insert(0, SnakeBit(newX, newY))
        self.x = newX
        self.y = newY


class SnakeBit:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
