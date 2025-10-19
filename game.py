import pygame
from dataclasses import dataclass
from collections import deque
WIDTH, HEIGHT = 520, 760
FLOORS = 10   
COLS = 3       
ROOM_W, ROOM_H = 140, 110
FLOOR_GAP = 150     
SIDE_MARGIN = 40    
COL_GAP = 30         
BG = (18, 20, 28)
ROOM_CENTER = (110, 170, 220)
ROOM_TARGET = (255, 190, 90)
pygame.init()

@dataclass(frozen=True)
class NodeId:
    floor: int
    col: int

class Room:
    def __init__(self, node_id: NodeId, rect: pygame.Rect):
        self.id = node_id
        self.rect = rect

def build_tower():
    rooms = {}
    total_w = COLS * ROOM_W + (COLS - 1) * COL_GAP
    start_x = (WIDTH - total_w) // 2
    cols_x = []
    for c in range(COLS):
        x = start_x + c * (ROOM_W + COL_GAP)
        cols_x.append(x)
    for f in range(FLOORS):
        y = HEIGHT - 120 - f * FLOOR_GAP
        for c in range(COLS):
            node = NodeId(f, c)
            rect = pygame.Rect(cols_x[c], y, ROOM_W, ROOM_H)
            room = Room(node, rect)

            rooms[node] = room
