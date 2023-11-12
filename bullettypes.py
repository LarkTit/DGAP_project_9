import math
from random import choice
from random import randint as rnd
import gameconstants as gc
import pygame


class Bullet:

    def __init__(self, screen: pygame.Surface, enemy, tank):
        self.screen = screen
        self.enemy = enemy
        self.tank = tank
        self.new_bullet()
        self.shot_color = gc.BLACK
        self.ricochets = 0

    def new_bullet(self):
        self.x = self.enemy.x
        self.y = self.enemy.y
        self.r = 10
        self.color = gc.RED
        self.vy = 0
        self.vx = 0

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            gc.BLACK,
            (self.x, self.y),
            self.r*0.5
        )


class Normal_bullet(Bullet):

    def new_bullet(self):
        self.x = self.enemy.x
        self.y = self.enemy.y
        self.r = 10
        self.color = gc.RED
        self.an = math.atan2((self.y - self.tank.y), (self.x - self.tank.x))
        self.vx = 0
        self.vy = 0

    def move(self):
        self.x += self.vx
        self.y += self.vy


class Homing_bullet(Bullet):

    def new_bullet(self):
        self.x = self.enemy.x
        self.y = self.enemy.y
        self.r = 10
        self.color = gc.RED
        self.an = math.atan2((self.y - self.tank.y), (self.x - self.tank.x))
        self.an_v = self.an
        self.v = 0
        self.vx = 0
        self.vy = 0
        self.a = 0

    def move(self):
        self.an_v -= (self.an_v-self.an) * self.v / 90
        self.vx = - self.v * math.cos(self.an_v)
        self.vy = - self.v * math.sin(self.an_v)
        self.x += self.vx
        self.y += self.vy
        self.an = math.atan2((self.y - self.tank.y), (self.x - self.tank.x))


class Ricochet_bullet(Bullet):

    def new_bullet(self):
        self.x = self.enemy.x
        self.y = self.enemy.y
        self.r = 10
        self.color = gc.RED
        self.an = math.atan2((self.y - self.tank.y), (self.x - self.tank.x)) + rnd(-10, 10) * 0.005
        self.vx = 0
        self.vy = 0

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.x + self.r >= gc.BORDERS.right:
            self.vx = -self.vx
            self.x = gc.BORDERS.right - self.r
            self.ricochets += 1
        if self.x - self.r <= gc.BORDERS.left:
            self.vx = -self.vx
            self.x = gc.BORDERS.left + self.r
            self.ricochets += 1
        if self.y + self.r >= gc.BORDERS.bottom:
            self.y = gc.BORDERS.bottom - self.r
            self.vy = -self.vy
            self.ricochets += 1
        if self.y - self.r <= gc.BORDERS.top:
            self.y = gc.BORDERS.top + self.r
            self.vy = -self.vy
            self.ricochets += 1


class Random_bullet(Bullet):

    def new_bullet(self):
        self.x = self.enemy.x
        self.y = self.enemy.y
        self.r = 5
        self.color = gc.RED
        self.an = math.atan2((self.y - self.tank.y), (self.x - self.tank.x)) + rnd(-10, 10) * 0.1
        self.vx = 0
        self.vy = 0

    def move(self):
        self.x += self.vx
        self.y += self.vy


class Bomb(Bullet):

    def new_bullet(self):
        self.x = self.enemy.x
        self.y = self.enemy.y
        self.length = self.x - self.tank.x
        self.height = self.tank.y - self.y
        self.r = 20
        self.color = gc.GREEN
        self.int_color = gc.RED
        self.v = 7
        self.accel = 0.3
        self.an = math.atan2((self.v**2 + (abs(self.v**4 - self.accel *
                             (self.accel * self.length**2 + 2*self.v**2*self.height)))**0.5), self.accel*self.length)
        self.vx = - self.v * math.cos(self.an)
        self.vy = self.v * math.sin(self.an)

        self.bomb_r = 0
        self.bomb_color = gc.BLACK
        self.timer = 80
        self.time = 0
        self.is_moving = True
        self.is_drawn = True

    def move(self):
        if self.is_moving:
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
                self.vy = -self.vy*0.6
                self.vx = self.vx*0.7
            self.vy -= self.accel

    def draw(self):
        if self.is_drawn:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )
            pygame.draw.circle(
                self.screen,
                self.int_color,
                (self.x, self.y),
                self.r // 2
            )
            pygame.draw.circle(
                self.screen,
                self.int_color,
                (self.x, self.y),
                self.r + 3,
                4

            )

    def explode(self):
        if not self.time % self.timer:
            if self.int_color == gc.BLACK:
                self.int_color = gc.RED
            else:
                self.int_color = gc.BLACK
            self.timer = max(self.timer - 15, 4)

        if self.time >= 160:
            self.is_moving = False
            self.bomb_r += 4
            self.bomb_color = (self.bomb_color[0] + 7,
                               self.bomb_color[1] + 7, self.bomb_color[2] + 7)
            self.is_drawn = False
        if self.time >= 196:
            if self in gc.bullets_array:
                gc.bullets_array.remove(self)
                self.time = 0
        self.time += 1

    def draw_explode(self):
        pygame.draw.circle(
            self.screen,
            self.bomb_color,
            (self.x, self.y),
            self.bomb_r,
            15
        )
