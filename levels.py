import math
import gameconstants as gc
import balls
import pygame
from random import choice
from random import sample
from pygame import Rect
import bullettypes as bullets
import enemytypes as enemy
import enemies
import gameconstants as gc


def update_dict():
    match gc.LEVEL:
        case 1:
            for i in sample(gc.ENEMIES_ID, 3):
                gc.enemies_dict[i] = 1
        case 2:
            gc.enemies_dict = gc.EMPTY_DICT
        case 3:
            gc.enemies_dict = gc.EMPTY_DICT
        case 4:
            gc.enemies_dict = gc.EMPTY_DICT
        case 5:
            gc.enemies_dict = gc.EMPTY_DICT
            for i in range(5):
                rand = choice(gc.ENEMIES_ID)
                gc.enemies_dict[rand] += 1
        case 6:
            gc.enemies_dict = gc.EMPTY_DICT
            for i in range(5):
                rand = choice(gc.ENEMIES_ID)
                gc.enemies_dict[rand] += 1
        case 7:
            gc.enemies_dict = gc.EMPTY_DICT
            gc.enemies_dict["oscillating"] = 6
        case _:
            gc.enemies_dict = gc.EMPTY_DICT
            for i in range(7):
                rand = choice(gc.ENEMIES_ID)
                gc.enemies_dict[rand] += 1


def changelevel():
    if gc.LEVEL > 7 and gc.total_score - gc.level_score >= gc.LVL_list[7]:
        gc.LEVEL += 1
        gc.level_score = gc.total_score
        update_dict()
        return True
    if gc.LEVEL < 7 and gc.total_score - gc.level_score >= gc.LVL_list[gc.LEVEL-1]:
        gc.LEVEL += 1
        gc.level_score = gc.total_score
        update_dict()
        return True
    return False


def spawn(enemytype, screen, shoottype=""):
    match enemytype:
        case "standart":
            target = enemy.Standart_target(screen, shoottype)
            target.id = "standart"
            gc.enemies_now["standart"] += 1
            gc.enemies_array.append(target)
        case "heavy":
            target = enemy.Heavy_target(screen, shoottype)
            target.id = "heavy"
            gc.enemies_now["heavy"] += 1
            gc.enemies_array.append(target)
        case "oscillating":
            target = enemy.Oscillating_target(screen, shoottype)
            target.id = "oscillating"
            gc.enemies_now["oscillating"] += 1
            gc.enemies_array.append(target)
        case "teleportation":
            target = enemy.Teleportation_target(screen, shoottype)
            target.id = "teleportation"
            gc.enemies_now["teleportation"] += 1
            gc.enemies_array.append(target)
        case "gravity":
            target = enemy.Gravity_target(screen, shoottype)
            target.id = "gravity"
            gc.enemies_now["gravity"] += 1
            gc.enemies_array.append(target)
        case "bombardier":
            target = enemy.Bombardier(screen, shoottype)
            target.id = "bombardier"
            gc.enemies_now["bombardier"] += 1
            gc.enemies_array.clear()
            gc.enemies_array.append(target)
    return target


def spawn_enemies(screen):
    if gc.LEVEL == 7 and gc.enemies_now['bombardier'] == 0:
        spawn("bombardier", screen)
    if gc.LEVEL == 2 and gc.enemies_now['oscillating'] == 0:
        for i in sample(gc.STANDART_DECK, 4):
            target = spawn("oscillating", screen, "normal")
            target.new_target(i)
    if gc.LEVEL == 3 and gc.enemies_now['teleportation'] == 0:
        for i in range(4):
            spawn("teleportation", screen, "ricochet")
    if gc.LEVEL == 4 and gc.enemies_now['heavy'] == 0:
        for i in range(5):
            spawn("heavy", screen, "random_spray")
    if gc.time >= gc.delay:
        for i in range(max(gc.enemies_dict.values())):
            for key in gc.enemies_now:
                if gc.enemies_now[key] < gc.enemies_dict[key]:
                    if gc.LEVEL == 7:
                        spawn(key, screen, "random_spray")
                    else:
                        spawn(key, screen, choice(gc.SHOT_DECK))
        gc.time = 0
    gc.time += 1
