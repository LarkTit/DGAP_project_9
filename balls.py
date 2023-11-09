import math
from random import choice
import gameconstants as gc
import pygame


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(gc.GAME_COLORS)
        self.live = 30
        self.accel = gc.G

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
            self.vy = -self.vy*0.8
            self.vx = self.vx*0.9
        if self.y - self.r <= gc.BORDERS.top:
            self.y = gc.BORDERS.top + self.r
            self.vy = -self.vy*0.8
            self.vx = self.vx*0.9
        self.vy -= self.accel

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        if ((self.x - obj.x)**2 + (self.y - obj.y)**2) < (obj.r + self.r)**2:
            return True
        return False
