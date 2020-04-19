import pygame
from pygame.locals import *

from Snake import Snake
from config import *

pygame.init()


window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

snake = Snake(1, 0, 1, 60, 70, 4*square_size)

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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

    snake.move()

    window.fill(black)

    for i in range(0, len(snake.snakeBits)):
        pygame.draw.rect(window, green, [
                         snake.snakeBits[i].xPos, snake.snakeBits[i].yPos, square_size, square_size])

    pygame.draw.rect(window, red, [100, 100, square_size, square_size])

    pygame.display.update()

    clock.tick(30)

pygame.quit()
quit()
