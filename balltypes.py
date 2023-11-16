import math
from random import choice
import gameconstants as gc
import pygame
from balls import Ball


class FreezeBall(Ball):

    def set_id(self):
        self.id = "freeze"

    def draw(self):
        pygame.draw.circle(
            self.screen,
            gc.CYAN,
            (self.x, self.y),
            self.r
        )

        pygame.draw.circle(
            self.screen,
            gc.BLUE,
            (self.x, self.y),
            self.r * 0.9,
            5
        )

    def hittest(self, obj):
        if ((self.x - obj.x)**2 + (self.y - obj.y)**2) < (obj.r + self.r)**2:
            for e in gc.enemies_array:
                if ((e.x - obj.x)**2 + (e.y - obj.y)**2) < (200)**2:
                    e.is_frozen = True
            return True
        return False


class RicochetBall(Ball):

    def set_id(self):
        self.id = "ricochet"
        self.color = gc.BLACK
        self.fade_color = self.color
        self.red, self.green, self.blue = self.color

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

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
            self.vy = -self.vy*1
            self.vx = self.vx*1
        if self.y - self.r <= gc.BORDERS.top:
            self.y = gc.BORDERS.top + self.r
            self.vy = -self.vy*1
            self.vx = self.vx*1
