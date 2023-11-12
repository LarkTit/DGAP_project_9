import math
from random import choice
from random import randint as rnd
import gameconstants as gc
from enemies import Target
import pygame


class Standart_target(Target):

    def new_target(self, level=0):
        self.x = rnd(75, 725)
        if level == 0:
            level = choice(gc.STANDART_DECK)
        self.y = level
        self.r = rnd(15, 25)
        self.color = gc.GREY
        self.live = 1
        self.points = 1


class Heavy_target(Target):

    def new_target(self, level=0):
        self.x = rnd(75, 725)
        if level == 0:
            level = choice(gc.STANDART_DECK)
        self.y = level
        self.r = 50
        self.color = gc.BLACK
        self.live = 3
        self.points = 1

    def hit(self):
        self.live -= 1
        gc.total_score += self.points
        self.color = (self.color[0]+50, self.color[1]+50, self.color[2]+50,)
        if self.live == 0 and self in gc.enemies_array:
            gc.enemies_now[self.id] -= 1
            gc.enemies_array.remove(self)


class Oscillating_target(Target):

    def new_target(self, level=0):
        self.x = choice((75, 725))
        if level == 0:
            level = choice(gc.STANDART_DECK)
        self.y = level
        self.r = rnd(25, 50)
        self.color = gc.BLUE
        self.live = 1
        self.points = 1
        self.accel_const = rnd(1, 5) / 6
        self.vx = 0

    def move(self):
        self.x += self.vx
        self.ax = (400-self.x) * 0.001 * self.accel_const
        self.vx += self.ax


class Teleportation_target(Target):

    def new_target(self, level=0):
        self.x = rnd(75, 725)
        if level == 0:
            level = choice(gc.EXTENDED_DECK)
        self.y = level
        self.r = rnd(25, 50)
        self.color = gc.CYAN
        self.live = 1
        self.points = 1
        self.tp_time = 0

    def move(self):
        self.tp_time += 1
        if self.tp_time >= 80:
            self.tp_time = 0
            self.x = rnd(75, 725)
            self.y = choice(gc.EXTENDED_DECK)


class Gravity_target(Target):

    def new_target(self, level=-100):
        self.x = rnd(75, 725)
        self.y = level
        self.r = 40
        self.vx = choice((-1, 1)) * rnd(1, 5)
        self.vy = 0
        self.color = gc.BROWN
        self.live = 1
        self.points = 2
        self.accel = rnd(3, 12) / 40

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.x + self.r >= gc.BORDERS.right:
            self.vx = -self.vx
            self.x = gc.BORDERS.right - self.r
        if self.x - self.r <= gc.BORDERS.left:
            self.vx = -self.vx
            self.x = gc.BORDERS.left + self.r
        if self.y + self.r >= gc.BORDERS.bottom:
            self.y = gc.BORDERS.bottom - self.r
            self.vy = -self.vy
            self.vx = self.vx
        if self.y - self.r <= gc.BORDERS.top:
            self.y = gc.BORDERS.top + self.r
            self.vy = -self.vy
            self.vx = self.vx
        self.vy -= self.accel


class Bombardier(Target):

    def new_target(self, level=150):
        self.x = 400
        self.y = level
        self.r = 75
        self.color = (75, 83, 32)
        self.live = 15
        self.points = 3
        self.shoot_type = "bombardier"
        self.shot_color = (128, 107, 42)
        self.delay = 120

    def hit(self):
        self.live -= 1
        gc.total_score += self.points
        self.color = (self.color[0]-5, self.color[1]-5, self.color[2]-2)
        if self.live == 0 and self in gc.enemies_array:
            gc.LEVEL += 1
            gc.enemies_now[self.id] -= 1
            gc.enemies_array.remove(self)
