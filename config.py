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
    (0, 0): "Attack",(0, 1): "Normal",(0, 3): "Normal",(0, 4): "Tank(HP)",
    (1, 0): "Attack",(1, 1): "Tank(HP)",(1, 2): "Normal",(1, 3): "Tank(HP)",(1, 4): "Tank(DEF)",
    (2, 0): "Def Gem",(2, 1): "Attack",(2, 2): "Atk Gem",(2, 3): "Tank(HP)",(2, 4): "Atk Gem",
    (3, 0): "Tank(DEF)",(3, 1): "Tank(HP)",(3, 2): "Heal Potion",(3, 3): "Normal",(3, 4): "Tank(HP)",
    (4, 0): "Tank(HP)",(4, 1): "Def Gem",(4, 2): "Tank(DEF)",(4, 3): "Tank(DEF)",(4, 4): "Def Gem",
    (5, 0): "Atk Gem",(5, 1): "Tank(HP)",(5, 2): "Atk Gem",(5, 3): "Attack",(5, 4): "Heal Potion",
    (6, 0): "Normal",(6, 1): "Def Gem",(6, 2): "Tank(HP)",(6, 3): "Tank(DEF)",(6, 4): "Attack",
}
BG = (18, 20, 28)
ROOM_COLOR = (80, 120, 170)
ROOM_BOSS = (190, 60, 60)
TEXT = (235, 235, 235)
ARROW_COLOR = (255, 220, 130)

ROOM_BG_IMAGE = "assets/dun2.png"

BOSS_ROOM_BG_IMAGE = "assets/boss_room1.gif"
