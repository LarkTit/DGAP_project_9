import math
from random import choice
from random import randint as rnd
import gameconstants as gc
import balls
import enemies
from tank import Tank

import pygame


pygame.init()
screen = pygame.display.set_mode((gc.WIDTH, gc.HEIGHT))

"""текст"""
pygame.font.init()
text = "SCORE: 0"
font = pygame.font.SysFont(None, 48)
img = font.render(text, True, gc.BLACK)


clock = pygame.time.Clock()
tank = Tank(screen)
target_1 = enemies.Target(screen)
target_2 = enemies.Target(screen)
target_1.new_target_1()
finished = False

while not finished:
    screen.fill(gc.WHITE)
    tank.draw()
    pygame.draw.rect(screen, gc.BLACK, gc.BORDERS, 1)
    target_1.draw()
    if gc.LEVEL > 1:
        target_2.draw()
    for b in gc.balls_array:
        b.draw()
    screen.blit(img, (20, 20))
    pygame.display.update()

    clock.tick(gc.FPS)
    tank.move()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            tank.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            tank.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            tank.targetting(event)

    if gc.LEVEL == 3:
        target_1.move()
        target_2.move()
    for b in gc.balls_array:
        b.move()
        if b.hittest(target_1) and target_1.live:
            target_1.live = 0
            target_1.hit()
            target_1.new_target_1()
            gc.balls_array.clear()
            if target_1.points == 4:
                LEVEL = 2
                target_2.new_target_2()
            if target_1.points + target_2.points == 8:
                LEVEL = 3
            text = "SCORE: " + str(target_1.points + target_2.points)
            img = font.render(text, True, gc.BLACK)
        if b.hittest(target_2) and target_2.live:
            target_2.live = 0
            target_2.hit()
            target_2.new_target_2()
            gc.balls_array.clear()
            if target_1.points + target_2.points == 8:
                LEVEL = 3
            text = "SCORE: " + str(target_1.points + target_2.points)
            img = font.render(text, True, gc.BLACK)
    tank.power_up()


pygame.quit()
