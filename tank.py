import math
import gameconstants as gc
import balls
import pygame
from random import choice
from pygame import Rect


class Tank:
    def __init__(self, screen):
        self.screen = screen

        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.width = 11
        self.color = gc.GREY
        self.body_color = gc.RED

        self.lives = 3
        self.is_hit = False
        self.bomb_r = 20
        self.bomb_color = gc.RED
        self.time = 0

        self.v = 5
        self.length = 30
        self.height = 15
        self.x = 100
        self.y = gc.BORDERS.bottom - self.height
        self.body = Rect(self.x - self.length, self.y - self.height, self.length*2, self.height*2)
        self.head = Rect(self.x - 12, self.y - 2*self.height, 24, 24)

    def move(self):
        if pygame.key.get_pressed()[pygame.K_d] and self.x != gc.BORDERS.right - self.length:
            self.body.move_ip((self.v, 0))
            self.head.move_ip((self.v, 0))
            self.x += self.v
        if pygame.key.get_pressed()[pygame.K_a] and self.x != self.length:
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
        new_ball.vx = self.f2_power * math.cos(self.an) / 2
        new_ball.vy = - self.f2_power * math.sin(self.an) / 2
        gc.balls_array.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        if event:
            gc.xpos = event.pos[0]
            gc.ypos = event.pos[1]
        if self.f2_on:
            self.color = gc.RED
        else:
            self.color = gc.GREY

    def draw(self):
        self.an = math.atan2((gc.ypos - self.y + 20), (gc.xpos - self.x))
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y - 20),
            (self.x + 15*math.cos(self.an) + math.cos(self.an)*self.f2_power,
             self.y - 20 + 15*math.sin(self.an) + math.sin(self.an)*self.f2_power),
            self.width
        )
        pygame.draw.rect(self.screen, self.body_color, self.body)
        pygame.draw.rect(self.screen, self.body_color, self.head)

    def draw_bomb(self):
        pygame.draw.circle(
            self.screen,
            self.bomb_color,
            (self.x, self.y + 5),
            self.bomb_r,
            15
        )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = gc.RED
        else:
            self.color = gc.GREY

    def hittank(self, bullet):
        if bullet.color == gc.GREEN:
            if not self.is_hit and bullet.bomb_r <= 90 and ((self.x - bullet.x)**2 + (self.y + 5 - bullet.y)**2) < (bullet.bomb_r + self.length - 4)**2:
                self.lives -= 1
                self.is_hit = True
                return True
        if not self.is_hit and ((self.x - bullet.x)**2 + (self.y + 5 - bullet.y)**2) < (bullet.r + self.length - 4)**2:
            self.lives -= 1
            self.is_hit = True
            return True
        return False

    def clear_bullets(self):
        for b in gc.bullets_array:
            if b in gc.bullets_array and ((self.x - b.x)**2 + (self.y + 5 - b.y)**2) < (b.r + self.bomb_r)**2:
                gc.bullets_array.remove(b)
