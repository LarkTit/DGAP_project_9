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
ammo_text = ["0", "0"]

heart = pygame.image.load('sprites\\heart.bmp').convert_alpha()
heart = pygame.transform.scale(heart, (54, 54))

default_on = pygame.image.load('sprites\\default-on.bmp').convert_alpha()
default_on = pygame.transform.scale(default_on, (60, 60))

default_off = pygame.image.load('sprites\\default-off.bmp').convert_alpha()
default_off = pygame.transform.scale(default_off, (60, 60))

freeze_on = pygame.image.load('sprites\\freeze-on.bmp').convert_alpha()
freeze_on = pygame.transform.scale(freeze_on, (60, 60))

freeze_off = pygame.image.load('sprites\\freeze-off.bmp').convert_alpha()
freeze_off = pygame.transform.scale(freeze_off, (60, 60))

ricochet_off = pygame.image.load('sprites\\ricochet-off.bmp').convert_alpha()
ricochet_off = pygame.transform.scale(ricochet_off, (60, 60))

ricochet_on = pygame.image.load('sprites\\ricochet-on.bmp').convert_alpha()
ricochet_on = pygame.transform.scale(ricochet_on, (60, 60))

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
    tank.draw_hitbox()
    if tank.is_hit:
        tank.draw_bomb()

    screen.blit(img, (20, 20))
    screen.blit(fps_img, (20, 50))
    screen.blit(level_img, (320, 20))
    for i in range(2):
        ammo_text = small_font.render(str(tank.ammo[i+1]), True, gc.BLACK)
        screen.blit(ammo_text, (80, 230 + 70*i))
    for i in range(tank.lives):
        screen.blit(heart, (600 + 56*i, 22))
    if tank.shoot_id == "default":
        screen.blit(default_on, (15, 160))
    else:
        screen.blit(default_off, (15, 160))
    if tank.shoot_id == "freeze":
        screen.blit(freeze_on, (15, 230))
    else:
        screen.blit(freeze_off, (15, 230))
    if tank.shoot_id == "ricochet":
        screen.blit(ricochet_on, (15, 300))
    else:
        screen.blit(ricochet_off, (15, 300))
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
        elif event.type == pygame.MOUSEMOTION:
            tank.targetting(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            tank.shoot_num = (tank.shoot_num-1) % 3
            tank.shoot_id = gc.BALLS[tank.shoot_num]
            while tank.ammo[tank.shoot_num] == 0:
                tank.shoot_num = (tank.shoot_num-1) % 3
                tank.shoot_id = gc.BALLS[tank.shoot_num]
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            tank.shoot_num = (tank.shoot_num+1) % 3
            tank.shoot_id = gc.BALLS[tank.shoot_num]
            while tank.ammo[tank.shoot_num] == 0:
                tank.shoot_num = (tank.shoot_num+1) % 3
                tank.shoot_id = gc.BALLS[tank.shoot_num]

    levels.spawn_enemies(screen)
    if levels.changelevel() and gc.LEVEL > 4:
        if gc.LEVEL % 2:
            tank.add_ammo(1, 0)
        else:
            tank.add_ammo(0, 1)
    if levels.changelevel() and gc.LEVEL > 8:
        tank.add_ammo(2, 2)

    for e in gc.enemies_array:
        e.unfreeze()
        if not e.is_frozen:
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
