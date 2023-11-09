import math
from random import choice
from random import randint as rnd
import gameconstants as gc
import pygame


class Target:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = -10
        self.y = -10
        self.r = 0
        self.points = 0
        self.live = 1
        self.vy = 0
        self.ay = 0

    def new_target_2(self):
        self.x = rnd(600, 690)
        self.y = rnd(300, 550)
        self.r = rnd(5, 18)
        self.color = gc.YELLOW
        self.live = 1
        self.vy = rnd(5, 10) * 1

    def new_target_1(self):
        self.x = rnd(720, 780)
        self.y = rnd(300, 550)
        self.r = rnd(7, 50)
        self.color = gc.RED
        self.live = 1
        self.vy = (self.y - 300) * rnd(1, 5) * 0.01

    def hit(self, points=1):
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        self.y += self.vy
        self.ay = (-self.y + 300)*0.001
        self.vy += self.ay
