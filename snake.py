import math
import random
import itertools
import pygame

NR_COLS = 10
NR_ROWS = 9
TILE_SIZE = 55
WINDOW_WIDTH = NR_COLS * TILE_SIZE
WINDOW_HEIGHT = NR_ROWS * TILE_SIZE
GAME_SPEED = 7

# snake
START_LENGTH = 3
START_X_POS = START_LENGTH - 1
START_Y_POS = math.floor(NR_ROWS / 2)
START_DX = 1
START_DY = 0

COLOR = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN1': (0, 255, 0),
    'GREEN2': (0, 200, 0),
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
    def __init__(self, x, y, color=COLOR['GREEN1'], head=False):
        self.x = x
        self.y = y
        self.color = color
        self.head = head


class Snake:
    def __init__(self, x, y, dx, dy, length):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.start_length = length
        self.snakebits = []
        self.spawn_tail()

    def spawn_tail(self):
        for x in range(self.x, self.x + self.start_length, TILE_SIZE):
            self.snakebits.append(SnakeBit(x, self.y))

    # Move by removing the tail and adding a new bit in front of the head
    def move(self, should_grow):
        if not should_grow:
            del self.snakebits[-1]

        new_x = self.snakebits[0].x + to_px(self.dx)
        new_y = self.snakebits[0].y + to_px(self.dy)
        self.snakebits.insert(0, SnakeBit(new_x, new_y))
        self.x = new_x
        self.y = new_y


class Game:
    def __init__(self):
        self.snake = Snake(to_px(START_X_POS), to_px(START_Y_POS), START_DX, START_DY, to_px(START_LENGTH))
        self.apple = Apple()
        self.score = 0
        self.high_score = 0
        self.game_over = False

    def game_loop(self):
        while not self.game_over:
            self.update_direction()

            if (self.is_tail_eaten()):
                self.snake.snakebits.clear()
                self.snake.spawn_tail()
                self.score = 0

            apple_eaten = self.is_apple_eaten()
            if (apple_eaten):
                self.apple.new_apple()
                self.score += 1

            self.snake.move(apple_eaten)

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

        # wrap snake on border
        if (self.snake.snakebits[0].x >= WINDOW_WIDTH):
            self.snake.snakebits[0].x = 0
        if (self.snake.snakebits[0].x < 0):
            self.snake.snakebits[0].x = WINDOW_WIDTH - TILE_SIZE
        if (self.snake.snakebits[0].y >= WINDOW_HEIGHT):
            self.snake.snakebits[0].y = 0
        if (self.snake.snakebits[0].y < 0):
            self.snake.snakebits[0].y = WINDOW_HEIGHT - TILE_SIZE

    def is_tail_eaten(self):
        for i in range(4, len(self.snake.snakebits)):
            if self.snake.x == self.snake.snakebits[i].x and self.snake.y == self.snake.snakebits[i].y:
                return True
        return False

    def is_apple_eaten(self):
        return self.snake.x == self.apple.x and self.snake.y == self.apple.y

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
        for i in range(0, len(self.snake.snakebits)):
            pygame.draw.rect(window, self.snake.snakebits[i].color, [
                self.snake.snakebits[i].x, self.snake.snakebits[i].y, TILE_SIZE, TILE_SIZE])

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
