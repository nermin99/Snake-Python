from config import SQUARE_SIZE


class Snake:
    snakebits = []

    def __init__(self, dx, dy, color, xPos, yPos, length):
        self.x = xPos
        self.y = yPos
        self.dx = dx
        self.dy = dy
        self.color = color
        self.start_length = length

        self.spawn_tail()

    def spawn_tail(self):
        for x in range(self.x, self.x + self.start_length, SQUARE_SIZE):
            self.snakebits.append(SnakeBit(x, self.y))

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
