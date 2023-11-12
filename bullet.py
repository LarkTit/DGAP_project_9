import math
from random import choice
from random import randint as rnd
import bullettypes as bullets
import gameconstants as gc
import pygame


def normal_shoot(enemy, tank):
    if enemy.time >= enemy.delay:
        bullet_0 = bullets.Normal_bullet(enemy.screen, enemy, tank)
        bullet_0.vx = - 7 * math.cos(bullet_0.an)
        bullet_0.vy = - 7 * math.sin(bullet_0.an)
        gc.bullets_array.append(bullet_0)
        enemy.time = 0
    enemy.time += 1


def homing_shoot(enemy, tank):
    if enemy.time >= enemy.delay:
        bullet_0 = bullets.Homing_bullet(enemy.screen, enemy, tank)
        bullet_0.v = 5
        bullet_0.vx = - math.cos(bullet_0.an)
        bullet_0.vy = - math.sin(bullet_0.an)
        gc.bullets_array.append(bullet_0)
        enemy.time = 0
    enemy.time += 1


def ricochet_shoot(enemy, tank):
    if enemy.time >= enemy.long_delay:
        if not enemy.time % enemy.delay:
            bullet_0 = bullets.Ricochet_bullet(enemy.screen, enemy, tank)
            bullet_0.vx = - 10 * math.cos(bullet_0.an)
            bullet_0.vy = 10 * math.sin(bullet_0.an)
            gc.bullets_array.append(bullet_0)
    if enemy.time >= enemy.long_delay + 37:
        enemy.time = 0
    enemy.time += 1


def random_shoot(enemy, tank):
    if enemy.time >= enemy.delay:
        for i in range(5):
            bullet_0 = bullets.Random_bullet(enemy.screen, enemy, tank)
            bullet_0.vx = - 3 * math.cos(bullet_0.an)
            bullet_0.vy = - 3 * math.sin(bullet_0.an)
            gc.bullets_array.append(bullet_0)
            enemy.time = 0
    enemy.time += 1


def bomb_shoot(enemy, tank):
    if enemy.time >= enemy.delay:
        bullet_0 = bullets.Bomb(enemy.screen, enemy, tank)
        gc.bullets_array.append(bullet_0)
        enemy.time = 0
    enemy.time += 1
