import math
from random import choice
from random import randint as rnd
import gameconstants as gc
import bullet as blt
import pygame


class Target:

    def __init__(self, screen: pygame.Surface, shoot_type=""):
        self.time = 0
        self.delay = 0
        self.long_delay = 0
        self.screen = screen
        self.shoot_type = shoot_type
        self.new_target()
        self.init_shoot()
        self.id = ''
        self.is_frozen = False
        self.freezetime = 0

    def new_target(self):
        self.x = rnd(500, 750)
        self.y = rnd(300, 600)
        self.r = rnd(7, 50)
        self.color = gc.RED
        self.live = 1
        self.vy = (self.y - 300) * rnd(1, 5) * 0.01 / 2
        self.points = 1

    def hit(self):
        self.live -= 1
        gc.total_score += self.points
        if self.live == 0 and self in gc.enemies_array:
            gc.enemies_now[self.id] -= 1
            gc.enemies_array.remove(self)

    def draw(self):
        if self.is_frozen:
            pygame.draw.circle(
                self.screen,
                gc.CYAN,
                (self.x, self.y),
                self.r*1.2,
                15
            )
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        return True

    def init_shoot(self):
        match self.shoot_type:
            case "":
                self.shot_color = self.color
            case "normal":
                self.shot_color = gc.WHITE
                self.delay = max(100 - 5 * gc.LEVEL, 30)
            case "homing":
                self.shot_color = gc.YELLOW
                self.delay = max(200 - 10 * gc.LEVEL, 100)
            case "ricochet":
                self.shot_color = gc.RED
                self.long_delay = 150
                self.delay = 15
            case "random_spray":
                self.shot_color = gc.MAGENTA
                self.delay = max(170 - 10*gc.LEVEL, 140)

    def draw_shoot(self):
        if not self.shoot_type:
            pass
        pygame.draw.circle(
            self.screen,
            self.shot_color,
            (self.x, self.y),
            self.r // 5 * 4,
            self.r // 2
        )

    def shoot(self, tank):
        match self.shoot_type:
            case "":
                pass
            case "normal":
                blt.normal_shoot(self, tank)
            case "homing":
                blt.homing_shoot(self, tank)
            case "ricochet":
                blt.ricochet_shoot(self, tank)
            case "random_spray":
                blt.random_shoot(self, tank)
            case "bombardier":
                blt.bomb_shoot(self, tank)

    def unfreeze(self):
        if self.is_frozen:
            if self.freezetime >= 180:
                self.is_frozen = False
                self.freezetime = 0
            self.freezetime += 1
