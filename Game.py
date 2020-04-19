import pygame
from pygame.locals import *
import random

from Snake import Snake
from Apple import Apple
from config import *

pygame.init()


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

snake = Snake(START_DX, START_DY, COLOR['GREEN'], START_POS_X,
              START_POS_Y, START_LENGTH*SQUARE_SIZE)

apple = Apple(COLOR['RED'])


game_over = False


def game_loop():
    global game_over

    while not game_over:
        update_direction()

        should_grow = apple_eaten()

        snake.move(should_grow)

        if should_grow:
            apple.new_coordinates()

        game_over = tail_eaten()

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
    if (snake.snakebits[0].xPos > WINDOW_WIDTH):
        snake.snakebits[0].xPos = 0
    if (snake.snakebits[0].xPos < 0):
        snake.snakebits[0].xPos = WINDOW_WIDTH - SQUARE_SIZE
    if (snake.snakebits[0].yPos > WINDOW_HEIGHT):
        snake.snakebits[0].yPos = 0
    if (snake.snakebits[0].yPos < 0):
        snake.snakebits[0].yPos = WINDOW_HEIGHT - SQUARE_SIZE


def apple_eaten():
    return snake.x == apple.x and snake.y == apple.y


def tail_eaten():
    for i in range(4, len(snake.snakebits)):
        if snake.x == snake.snakebits[i].xPos and snake.y == snake.snakebits[i].yPos:
            return True
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


if __name__ == "__main__":
    game_loop()
