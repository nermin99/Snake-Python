import random
import pygame

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SQUARE_SIZE = 20
GAME_SPEED = 13

# snake
START_POS_X = 100
START_POS_Y = 120
START_DX = 1
START_DY = 0
START_LENGTH = 3

COLOR = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255)
}

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

class Apple:
    def __init__(self, color):
        self.color = color
        self.new_coordinates()

    def new_coordinates(self):
        self.x = round(random.randrange(
            0, WINDOW_WIDTH - SQUARE_SIZE) / SQUARE_SIZE) * SQUARE_SIZE
        self.y = round(random.randrange(
            0, WINDOW_HEIGHT - SQUARE_SIZE) / SQUARE_SIZE) * SQUARE_SIZE


class SnakeBit:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos


class Snake:
    def __init__(self, xPos, yPos, dx, dy, length, color):
        self.x = xPos
        self.y = yPos
        self.dx = dx
        self.dy = dy
        self.start_length = length
        self.color = color
        self.snakebits = []
        self.spawn_tail()

    def spawn_tail(self):
        for x in range(self.x, self.x + self.start_length, SQUARE_SIZE):
            self.snakebits.append(SnakeBit(x, self.y))

    # Move by removing the tail and adding a new bit in front of the head
    def move(self, should_grow):
        if not should_grow:
            del self.snakebits[-1]

        newX = self.snakebits[0].xPos + self.dx * SQUARE_SIZE
        newY = self.snakebits[0].yPos + self.dy * SQUARE_SIZE
        self.snakebits.insert(0, SnakeBit(newX, newY))
        self.x = newX
        self.y = newY


class Game:
    def __init__(self):
        self.snake = Snake(START_POS_X, START_POS_Y, START_DX, START_DY,
                    START_LENGTH*SQUARE_SIZE, COLOR['GREEN'])
        self.apple = Apple(COLOR['RED'])
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
                self.apple.new_coordinates()
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
        if (self.snake.snakebits[0].xPos >= WINDOW_WIDTH):
            self.snake.snakebits[0].xPos = 0
        if (self.snake.snakebits[0].xPos < 0):
            self.snake.snakebits[0].xPos = WINDOW_WIDTH - SQUARE_SIZE
        if (self.snake.snakebits[0].yPos >= WINDOW_HEIGHT):
            self.snake.snakebits[0].yPos = 0
        if (self.snake.snakebits[0].yPos < 0):
            self.snake.snakebits[0].yPos = WINDOW_HEIGHT - SQUARE_SIZE

    def is_tail_eaten(self):
        for i in range(4, len(self.snake.snakebits)):
            if self.snake.x == self.snake.snakebits[i].xPos and self.snake.y == self.snake.snakebits[i].yPos:
                return True
        return False

    def is_apple_eaten(self):
        return self.snake.x == self.apple.x and self.snake.y == self.apple.y

    def render(self):
        # background
        window.fill(COLOR['BLACK'])

        # apple
        pygame.draw.rect(window, self.apple.color, [
                        self.apple.x, self.apple.y, SQUARE_SIZE, SQUARE_SIZE])

        # snake
        for i in range(0, len(self.snake.snakebits)):
            pygame.draw.rect(window, self.snake.color, [
                self.snake.snakebits[i].xPos, self.snake.snakebits[i].yPos, SQUARE_SIZE, SQUARE_SIZE])

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
