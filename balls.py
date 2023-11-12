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
        self.fade_color = self.color
        self.red, self.green, self.blue = self.color
        self.live = 30
        self.accel = gc.G
        self.time = 0

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
            self.vy = -self.vy*0.7
            self.vx = self.vx*0.8
        if self.y - self.r <= gc.BORDERS.top:
            self.y = gc.BORDERS.top + self.r
            self.vy = -self.vy*0.7
            self.vx = self.vx*0.8
        self.vy -= self.accel

    def ball_fade(self):
        if self.time >= 110 and self.time < 150:
            self.fade_color = (self.fade_color[0] + (255 - self.red) / 40,
                               self.fade_color[1] + (255 - self.green) / 40,
                               self.fade_color[2] + (255 - self.blue) / 40)
            self.color = tuple(map(int, self.fade_color))
        if self.time >= 150:
            if self in gc.balls_array:
                gc.balls_array.remove(self)
        self.time += 1

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
