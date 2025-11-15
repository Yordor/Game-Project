import pygame

WIDTH, HEIGHT = 1920, 1080
FPS = 60

FLOORS = 8
COLS = 5
ROOM_W, ROOM_H = 140, 110
FLOOR_GAP = 150
COL_GAP = 30

PLAYER_SPEED = 260
CAM_FOLLOW = 0.1

PLAYER_IMG_PATH = "assets/player.png"

MONSTER_IMG_PATHS = {
    "Normal":   "assets/Enemy_Normal.png",
    "Tank(HP)": "assets/Enemy_Hp.png",
    "Tank(DEF)":"assets/Enemy_Def.png",
    "Attack":   "assets/Enemy_Atk.png",
    "BOSS":     "assets/Enemy_Boss.png"
}

ITEM_IMG_PATHS = {
    "Def Gem":     "assets/Item2.png",
    "Atk Gem":     "assets/Item1.png",
    "Heal Potion": "assets/Item3.png",
}

ROOM_LAYOUT = {
    (0, 0): "Attack",
    (2, 0): "Tank(DEF)",
    (0, 4): "Tank(DEF)",
    (1, 2): "Normal",
    (1, 3): "Tank(HP)",
    (1, 4): "Def Gem",
}

BG = (18, 20, 28)
ROOM_COLOR = (80, 120, 170)
ROOM_BOSS = (190, 60, 60)
TEXT = (235, 235, 235)
ARROW_COLOR = (255, 220, 130)

ROOM_BG_IMAGE = "assets/dun2.png"
BOSS_ROOM_BG_IMAGE = "assets/boss_room1.gif"