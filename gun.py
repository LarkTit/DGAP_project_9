import math
from random import choice
from random import randint as rnd

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
BORDERS = pygame.Rect(0, 0, WIDTH - 10, HEIGHT - 10)
G = 3.3
LEVEL = 1


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.accel = G

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x + self.r >= BORDERS.right:
            self.vx = -self.vx
            self.x = BORDERS.right - self.r
        if self.x - self.r <= BORDERS.left:
            self.vx = -self.vx
            self.x = BORDERS.left + self.r
        if self.y + self.r >= BORDERS.bottom:
            self.y = BORDERS.bottom - self.r
            self.vy = -self.vy*0.8
            self.vx = self.vx*0.9
        if self.y - self.r <= BORDERS.top:
            self.y = BORDERS.top + self.r
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
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x - obj.x)**2 + (self.y - obj.y)**2) < (obj.r + self.r)**2:
            return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.width = 11
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
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
            self.color = RED
        else:
            self.color = GREY

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
            self.color = RED
        else:
            self.color = GREY


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
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 690)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(5, 18)
        color = self.color = YELLOW
        live = self.live = 1
        vy = self.vy = rnd(5, 10) * 1

    def new_target_1(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(720, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(7, 50)
        color = self.color = RED
        live = self.live = 1
        vy = self.vy = (self.y - 300) * rnd(1, 5) * 0.01

    def hit(self, points=1):
        """Попадание шарика в цель."""
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


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

"""текст"""
pygame.font.init()
text = "SCORE: 0"
font = pygame.font.SysFont(None, 48)
img = font.render(text, True, BLACK)


clock = pygame.time.Clock()
gun = Gun(screen)
target_1 = Target(screen)
target_2 = Target(screen)
target_1.new_target_1()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    pygame.draw.rect(screen, BLACK, BORDERS, 1)
    target_1.draw()
    if LEVEL > 1:
        target_2.draw()
    for b in balls:
        b.draw()
    screen.blit(img, (20, 20))
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    if LEVEL == 3:
        target_1.move()
        target_2.move()

    for b in balls:
        b.move()
        if b.hittest(target_1) and target_1.live:
            target_1.live = 0
            target_1.hit()
            target_1.new_target_1()
            balls.clear()
            if target_1.points == 4:
                LEVEL = 2
                target_2.new_target_2()
            if target_1.points + target_2.points == 8:
                LEVEL = 3
            text = "SCORE: " + str(target_1.points + target_2.points)
            img = font.render(text, True, BLACK)
        if b.hittest(target_2) and target_2.live:
            target_2.live = 0
            target_2.hit()
            target_2.new_target_2()
            balls.clear()
            if target_1.points + target_2.points == 8:
                LEVEL = 3
            text = "SCORE: " + str(target_1.points + target_2.points)
            img = font.render(text, True, BLACK)
    gun.power_up()

pygame.quit()
