import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import math
import random
import itertools

NR_COLS = 10
NR_ROWS = 9
TILE_SIZE = 55
WINDOW_WIDTH = NR_COLS * TILE_SIZE
WINDOW_HEIGHT = NR_ROWS * TILE_SIZE
GAME_SPEED = 7

# snake
START_LENGTH = 3
START_HEAD_X = START_LENGTH - 1 # Not px.
START_HEAD_Y = math.floor(NR_ROWS / 2) # Not px.
START_DX = 1
START_DY = 0

COLOR = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'GREY1': (120, 120, 120),
    'GREY2': (70, 70, 70)
}

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

def to_px(tile_unit):
    return tile_unit * TILE_SIZE


class Apple:
    def __init__(self, color=COLOR['RED']):
        self.color = color
        self.new_apple()

    def new_apple(self):
        self.x = to_px(random.randint(0,NR_COLS-1))
        self.y = to_px(random.randint(0,NR_ROWS-1))


class SnakeBit:
    def __init__(self, x, y, head=False):
        self.x = x
        self.y = y
        self.head = head


class Snake:
    def __init__(self, head_x, head_y, dx, dy, length):
        self.head_x = head_x
        self.head_y = head_y
        self.dx = dx
        self.dy = dy
        self.start_length = length
        self.snakebits = []
        self.spawn()

    def spawn(self):
        self.dx = START_DX
        self.dy = START_DY

        self.snakebits.append(SnakeBit(to_px(START_HEAD_X), to_px(START_HEAD_Y), head=True))
        for x_pos in range(START_HEAD_X - 1, -1, -1):
            self.snakebits.append(SnakeBit(to_px(x_pos), to_px(START_HEAD_Y)))

    # Move by removing the tail and adding a new bit in front of the head
    def move(self, should_grow):
        if not should_grow:
            del self.snakebits[-1]

        self.snakebits[0].head = False # previoius head is no longer head
        new_x = self.snakebits[0].x + to_px(self.dx)
        new_y = self.snakebits[0].y + to_px(self.dy)
        self.snakebits.insert(0, SnakeBit(new_x, new_y, head=True))
        self.head_x = new_x
        self.head_y = new_y


class Game:
    def __init__(self):
        self.snake = Snake(to_px(START_HEAD_X), to_px(START_HEAD_Y), START_DX, START_DY, to_px(START_LENGTH))
        self.apple = Apple()
        self.score = 0
        self.high_score = 0
        self.game_over = False

    def game_loop(self):
        while not self.game_over:
            self.update_direction()

            apple_eaten = self.is_apple_eaten()
            if (apple_eaten):
                self.apple.new_apple()
                self.score += 1

            self.snake.move(apple_eaten)

            if (self.did_loose()):
                self.score = 0
                self.snake.snakebits.clear()
                self.snake.spawn()

            self.high_score = self.score if self.score > self.high_score else self.high_score

            self.render()
            pygame.display.update()
            clock.tick(GAME_SPEED)

        pygame.quit()
        quit()

    def update_direction(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.snake.dx != 1:
                        self.snake.dx = -1
                        self.snake.dy = 0
                elif event.key == pygame.K_UP:
                    if self.snake.dy != 1:
                        self.snake.dx = 0
                        self.snake.dy = -1
                elif event.key == pygame.K_RIGHT:
                    if self.snake.dx != -1:
                        self.snake.dx = 1
                        self.snake.dy = 0
                elif event.key == pygame.K_DOWN:
                    if self.snake.dy != -1:
                        self.snake.dx = 0
                        self.snake.dy = 1


    def is_apple_eaten(self):
        head_x, head_y = self.snake.snakebits[0].x, self.snake.snakebits[0].y
        return head_x == self.apple.x and head_y == self.apple.y

    def did_loose(self):
        if self.is_tail_eaten():
            return True
        elif self.did_hit_border():
            return True
        else:
            return False

    def is_tail_eaten(self):
        head_x, head_y = self.snake.snakebits[0].x, self.snake.snakebits[0].y
        for i in range(4, len(self.snake.snakebits)):
            if head_x == self.snake.snakebits[i].x and head_y == self.snake.snakebits[i].y:
                return True
        return False

    def did_hit_border(self):
        head_x, head_y = self.snake.snakebits[0].x, self.snake.snakebits[0].y
        if (head_x < 0) or (head_x >= WINDOW_WIDTH): return True
        if (head_y < 0) or (head_y >= WINDOW_HEIGHT): return True
        return False

    def render(self):
        # background (alternating tile colors)
        bg_colors = itertools.cycle((COLOR['GREY1'], COLOR['GREY2']))
        for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
            for x in range(0, WINDOW_WIDTH, TILE_SIZE):
                rect = (x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(window, next(bg_colors), rect)
            next(bg_colors)

        # apple
        pygame.draw.rect(window, self.apple.color, [
                        self.apple.x, self.apple.y, TILE_SIZE, TILE_SIZE])

        # snake
        for snakebit in self.snake.snakebits:
            pygame.draw.rect(window, COLOR['BLUE'] if snakebit.head else COLOR['GREEN'],
                [snakebit.x, snakebit.y, TILE_SIZE, TILE_SIZE])

        # score
        font = pygame.font.SysFont('Monaco', 42)

        score_img = font.render("Score: " + str(self.score), True, COLOR['WHITE'])
        high_score_img = font.render(
            "High Score: " + str(self.high_score), True, COLOR['WHITE'])

        (msg_width, _) = font.size("High Score: " + str(self.high_score))
        window.blit(score_img, [0, 0])
        window.blit(high_score_img, [WINDOW_WIDTH - msg_width, 0])


if __name__ == "__main__":
    game = Game()
    game.game_loop()
