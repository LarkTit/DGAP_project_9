import math
from gameconstants import gc
import balls
import pygame


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.width = 11
        self.color = gc.GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        global balls_array, bullet
        bullet += 1
        new_ball = balls.Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls_array.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        if event:
            if (event.pos[0]-20) == 0:
                self.an = math.pi/2
            else:
                self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = gc.RED
        else:
            self.color = gc.GREY

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            (0, 450),
            (0 + 2*math.cos(self.an)*self.f2_power, 450 + 2*math.sin(self.an)*self.f2_power),
            self.width
        )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = gc.RED
        else:
            self.color = gc.GREY
