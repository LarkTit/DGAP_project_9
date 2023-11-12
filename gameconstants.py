from pygame import Rect

FPS = 60
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 201, 31)
GREEN = (0, 255, 0)
MAGENTA = (255, 3, 184)
CYAN = (0, 255, 204)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
BROWN = (150, 75, 0)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
WIDTH = 800
HEIGHT = 600
G = 0.7
LEVEL = 1
BORDERS = Rect(0, 0, WIDTH - 10, HEIGHT - 10)

STANDART_DECK = [i for i in range(50, 250, 25)]
EXTENDED_DECK = [i for i in range(50, 500, 25)]
ENEMIES_ID = ["standart", "heavy", "oscillating", "teleportation", "gravity"]
SHOT_DECK = ("normal", "homing", "ricochet", "random_spray")
bullet = 0
balls_array = []
enemies_array = []
bullets_array = []
xpos = 0
ypos = 0
total_score = 0
level_score = 0
LVL_list = [10, 10, 10, 10, 20, 30, 500, 40]
EMPTY_DICT = {"standart": 0,
              "heavy": 0,
              "oscillating": 0,
              "teleportation": 0,
              "gravity": 0,
              "bombardier": 0}
enemies_dict = EMPTY_DICT.copy()
enemies_now = {"standart": 0,
               "heavy": 0,
               "oscillating": 0,
               "teleportation": 0,
               "gravity": 0,
               "bombardier": 0}
time = 0
delay = 360
