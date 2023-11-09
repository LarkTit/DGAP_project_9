import math
import gameconstants as gc
import balls
import pygame
from pygame import Rect


class Tank:
    def __init__(self, screen):
        self.screen = screen

        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.width = 11
        self.color = gc.GREY

        self.v = 10
        self.length = 30
        self.height = 15
        self.x = 100
        self.y = gc.BORDERS.bottom - self.height
        self.body = Rect(self.x - self.length, self.y - self.height, self.length*2, self.height*2)
        self.head = Rect(self.x - 12, self.y - 2*self.height, 24, 24)

    def move(self):
        if pygame.key.get_pressed()[pygame.K_d]:
            self.body.move_ip((self.v, 0))
            self.head.move_ip((self.v, 0))
            self.x += self.v
        if pygame.key.get_pressed()[pygame.K_a]:
            self.body.move_ip((-self.v, 0))
            self.head.move_ip((-self.v, 0))
            self.x -= self.v

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        gc.bullet += 1
        new_ball = balls.Ball(self.screen, self.x, self.y - 20)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        gc.balls_array.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        if event:
            self.an = math.atan2((event.pos[1] - self.y + 20), (event.pos[0] - self.x))
        if self.f2_on:
            self.color = gc.RED
        else:
            self.color = gc.GREY

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y - 20),
            (self.x + 15*math.cos(self.an) + math.cos(self.an)*self.f2_power,
             self.y - 20 + 15*math.sin(self.an) + math.sin(self.an)*self.f2_power),
            self.width
        )
        pygame.draw.rect(self.screen, gc.RED, self.body)
        pygame.draw.rect(self.screen, gc.RED, self.head)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = gc.RED
        else:
            self.color = gc.GREY
