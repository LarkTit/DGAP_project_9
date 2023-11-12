import math
from random import choice
from random import randint as rnd
import gameconstants as gc
import levels
import balls
import enemies
import enemytypes as enemy
from tank import Tank

import pygame


pygame.init()
screen = pygame.display.set_mode((gc.WIDTH, gc.HEIGHT))

"""текст"""
pygame.font.init()
text = "SCORE: 0"
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 120)
img = font.render(text, True, gc.BLACK)
fps_text = ""
fps_img = font.render(fps_text, True, gc.BLACK)
level_text = "LEVEL: " + str(gc.LEVEL)
level_img = font.render(level_text, True, gc.BLACK)

heart = pygame.image.load('sprite.bmp').convert_alpha()
heart = pygame.transform.scale(heart, (54, 54))

levels.update_dict()
clock = pygame.time.Clock()
tank = Tank(screen)
finished = False

while not finished:
    screen.fill(gc.WHITE)
    for b in gc.balls_array:
        b.draw()
    for bul in gc.bullets_array:
        bul.draw()
        if bul.color == gc.GREEN:
            bul.draw_explode()

    tank.draw()
    pygame.draw.rect(screen, gc.BLACK, gc.BORDERS, 1)
    for e in gc.enemies_array:
        e.draw()
        e.draw_shoot()
    if tank.is_hit:
        tank.draw_bomb()
    screen.blit(img, (20, 20))
    screen.blit(fps_img, (20, 50))
    screen.blit(level_img, (320, 20))
    for i in range(tank.lives):
        screen.blit(heart, (600 + 56*i, 22))
    pygame.display.update()

    clock.tick(gc.FPS)
    fps_text = "FPS: " + str(int(clock.get_fps()))
    fps_img = small_font.render(fps_text, True, gc.BLACK)
    level_text = "LEVEL: " + str(gc.LEVEL)
    level_img = font.render(level_text, True, gc.BLACK)

    tank.move()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            tank.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            tank.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            tank.targetting(event)

    levels.spawn_enemies(screen)
    levels.changelevel()

    for e in gc.enemies_array:
        e.move()
        e.shoot(tank)

    for bul in gc.bullets_array:
        bul.move()
        if bul.ricochets > 3:
            gc.bullets_array.remove(bul)
        if bul.y > gc.BORDERS.bottom:
            gc.bullets_array.remove(bul)
        if bul.color == gc.GREEN:
            bul.explode()
        tank.hittank(bul)

    if tank.is_hit:
        if tank.lives <= 0:
            gameover_text = big_font.render("GAME OVER", True, gc.BLACK)
            screen.fill(gc.WHITE)
            screen.blit(gameover_text, (130, 240))
            screen.blit(img, (300, 320))

            pygame.display.update()
            pygame.time.delay(4000)
            finished = True
        if tank.time <= 62:
            tank.bomb_r += 4
            tank.clear_bullets()
            tank.bomb_color = (255, tank.bomb_color[1] + 4, tank.bomb_color[2] + 4)
        else:
            tank.is_hit = False
            tank.bomb_r = 0
            tank.time = 0
            tank.bomb_color = gc.RED
        tank.time += 1

    for b in gc.balls_array:
        b.move()
        b.ball_fade()
        for e in gc.enemies_array:
            if b.hittest(e) and e.live:
                e.hit()
                if b in gc.balls_array:
                    gc.balls_array.remove(b)
                text = "SCORE: " + str(gc.total_score)
                img = font.render(text, True, gc.BLACK)

    tank.power_up()


pygame.quit()
