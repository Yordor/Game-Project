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
    "Slime":   "assets/Enemy_Normal.png",
    "Ghost": "assets/Enemy_Hp.png",
    "Spider":"assets/Enemy_Def.png",
    "Bat":   "assets/Enemy_Atk.png",
    "BOSS":     "assets/Enemy_Boss.png"
}

ITEM_IMG_PATHS = {
    "Def Gem":     "assets/Item2.png",
    "Atk Gem":     "assets/Item1.png",
    "Heal Potion": "assets/Item3.png",
}

ROOM_LAYOUT = {
    (0, 0): "Bat",(0, 1): "Slime",(0, 3): "Slime",(0, 4): "Ghost",
    (1, 0): "Bat",(1, 1): "Ghost",(1, 2): "Slime",(1, 3): "Ghost",(1, 4): "Spider",
    (2, 0): "Def Gem",(2, 1): "Bat",(2, 2): "Atk Gem",(2, 3): "Ghost",(2, 4): "Atk Gem",
    (3, 0): "Spider",(3, 1): "Ghost",(3, 2): "Heal Potion",(3, 3): "Slime",(3, 4): "Ghost",
    (4, 0): "Ghost",(4, 1): "Def Gem",(4, 2): "Spider",(4, 3): "Spider",(4, 4): "Def Gem",
    (5, 0): "Atk Gem",(5, 1): "Ghost",(5, 2): "Atk Gem",(5, 3): "Bat",(5, 4): "Heal Potion",
    (6, 0): "Slime",(6, 1): "Def Gem",(6, 2): "Ghost",(6, 3): "Spider",(6, 4): "Bat",
}
BG = (18, 20, 28)
ROOM_COLOR = (80, 120, 170)
ROOM_BOSS = (190, 60, 60)
TEXT = (235, 235, 235)
ARROW_COLOR = (255, 220, 130)

ROOM_BG_IMAGE = "assets/dun2.png"

BOSS_ROOM_BG_IMAGE = "assets/boss_room1.gif"

