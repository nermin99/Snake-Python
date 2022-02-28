import pygame
import random

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

snake = Snake(START_DX, START_DY, COLOR['GREEN'], START_POS_X,
              START_POS_Y, START_LENGTH*SQUARE_SIZE)

apple = Apple(COLOR['RED'])

score, high_score = 0, 0
game_over = False

def game_loop():
    global game_over, score, high_score

    while not game_over:
        update_direction()

        is_tail_eaten()

        should_grow = is_apple_eaten()
        snake.move(should_grow)

        high_score = score if score > high_score else high_score

        render()
        pygame.display.update()
        clock.tick(GAME_SPEED)

    pygame.quit()
    quit()


def update_direction():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global game_over
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if snake.dx != 1:
                    snake.dx = -1
                    snake.dy = 0
            elif event.key == pygame.K_UP:
                if snake.dy != 1:
                    snake.dx = 0
                    snake.dy = -1
            elif event.key == pygame.K_RIGHT:
                if snake.dx != -1:
                    snake.dx = 1
                    snake.dy = 0
            elif event.key == pygame.K_DOWN:
                if snake.dy != -1:
                    snake.dx = 0
                    snake.dy = 1

    # wrap snake on border
    if (snake.snakebits[0].xPos >= WINDOW_WIDTH):
        snake.snakebits[0].xPos = 0
    if (snake.snakebits[0].xPos < 0):
        snake.snakebits[0].xPos = WINDOW_WIDTH - SQUARE_SIZE
    if (snake.snakebits[0].yPos >= WINDOW_HEIGHT):
        snake.snakebits[0].yPos = 0
    if (snake.snakebits[0].yPos < 0):
        snake.snakebits[0].yPos = WINDOW_HEIGHT - SQUARE_SIZE


def is_tail_eaten():
    global score
    for i in range(4, len(snake.snakebits)):
        if snake.x == snake.snakebits[i].xPos and snake.y == snake.snakebits[i].yPos:
            snake.snakebits.clear()
            snake.spawn_tail()
            score = 0
            return True
    return False


def is_apple_eaten():
    global score
    if snake.x == apple.x and snake.y == apple.y:
        apple.new_coordinates()
        score += 1
        return True
    else:
        return False


def render():
    # background
    window.fill(COLOR['BLACK'])

    # apple
    pygame.draw.rect(window, apple.color, [
                     apple.x, apple.y, SQUARE_SIZE, SQUARE_SIZE])

    # snake
    for i in range(0, len(snake.snakebits)):
        pygame.draw.rect(window, snake.color, [
            snake.snakebits[i].xPos, snake.snakebits[i].yPos, SQUARE_SIZE, SQUARE_SIZE])

    # score
    font = pygame.font.SysFont('Monaco', 42)

    score_img = font.render("Score: " + str(score), True, COLOR['WHITE'])
    high_score_img = font.render(
        "High Score: " + str(high_score), True, COLOR['WHITE'])

    (msg_width, _) = font.size("High Score: " + str(high_score))
    window.blit(score_img, [0, 0])
    window.blit(high_score_img, [WINDOW_WIDTH - msg_width, 0])


if __name__ == "__main__":
    game_loop()
