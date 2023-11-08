import math
from random import choice
from random import randint as rnd
import gameconstants as gc
import balls
import enemies

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
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
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
        """Прицеливание. Зависит от положения мыши."""
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


pygame.init()
screen = pygame.display.set_mode((gc.WIDTH, gc.HEIGHT))
bullet = 0
balls_array = []

"""текст"""
pygame.font.init()
text = "SCORE: 0"
font = pygame.font.SysFont(None, 48)
img = font.render(text, True, gc.BLACK)


clock = pygame.time.Clock()
gun = Gun(screen)
target_1 = enemies.Target(screen)
target_2 = enemies.Target(screen)
target_1.new_target_1()
finished = False

while not finished:
    screen.fill(gc.WHITE)
    gun.draw()
    pygame.draw.rect(screen, gc.BLACK, gc.BORDERS, 1)
    target_1.draw()
    if gc.LEVEL > 1:
        target_2.draw()
    for b in balls_array:
        b.draw()
    screen.blit(img, (20, 20))
    pygame.display.update()

    clock.tick(gc.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    if gc.LEVEL == 3:
        target_1.move()
        target_2.move()

    for b in balls_array:
        b.move()
        if b.hittest(target_1) and target_1.live:
            target_1.live = 0
            target_1.hit()
            target_1.new_target_1()
            balls_array.clear()
            if target_1.points == 4:
                LEVEL = 2
                target_2.new_target_2()
            if target_1.points + target_2.points == 8:
                LEVEL = 3
            text = "SCORE: " + str(target_1.points + target_2.points)
            img = font.render(text, True, gc.BLACK)
        if b.hittest(target_2) and target_2.live:
            target_2.live = 0
            target_2.hit()
            target_2.new_target_2()
            balls.clear()
            if target_1.points + target_2.points == 8:
                LEVEL = 3
            text = "SCORE: " + str(target_1.points + target_2.points)
            img = font.render(text, True, gc.BLACK)
    gun.power_up()

pygame.quit()
