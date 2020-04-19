from config import *


class Snake:
    dx = 1
    dy = 0
    speed = 1
    snakeBits = []
    color = 0

    def __init__(self, dx, dy, speed, xPos, yPos, length):
        self.dx = dx
        self.dy = dy
        self.speed = speed

        for x in range(xPos, xPos + length, square_size):
            self.snakeBits.append(SnakeBit(x, yPos))

    # Move by removing the tail and adding a new bit in front of the head
    def move(self):
        del self.snakeBits[-1]

        newX = self.snakeBits[0].xPos + self.dx * self.speed
        newY = self.snakeBits[0].yPos + self.dy * self.speed
        self.snakeBits.append(SnakeBit(newX, newY))


class SnakeBit:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
