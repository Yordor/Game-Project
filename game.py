import pygame
from dataclasses import dataclass
from collections import deque

# -----------------------------
# CONFIG ปรับได้
# -----------------------------
WIDTH, HEIGHT = 520, 760
FLOORS = 10
COLS = 3
ROOM_W, ROOM_H = 140, 110
FLOOR_GAP = 150
SIDE_MARGIN = 40
COL_GAP = 30

PLAYER_SPEED = 250.0
CAM_FOLLOW = 0.1

BG = (18, 20, 28)
ROOM_COLOR = (70, 110, 160)
ROOM_CENTER = (110, 170, 220)
ROOM_TARGET = (255, 190, 90)
PLAYER_COLOR = (255, 236, 90) #เดะเปลียนเป็นตัวละครทีหลังตอนนี้เอาจุดโง่ๆไปก่อน55
TEXT = (235, 235, 235)
LINK_COLOR = (46, 60, 90)

pygame.init()
FONT = pygame.font.SysFont("consolas", 18)
BIG = pygame.font.SysFont("consolas", 24)

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
    links = {}
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

    for f in range(FLOORS):
        for c in range(COLS):
            node = NodeId(f, c)
            neigh = []
            if c - 1 >= 0:
                neigh.append(NodeId(f, c - 1))
            if c + 1 < COLS:
                neigh.append(NodeId(f, c + 1))
            if c == 1:
                if f + 1 < FLOORS:
                    neigh.append(NodeId(f + 1, c))
                if f - 1 >= 0:
                    neigh.append(NodeId(f - 1, c))
            links[node] = neigh

    return rooms, links

def center_of(rect: pygame.Rect):
    return pygame.Vector2(rect.centerx, rect.centery)

def shortest_path(links, start: NodeId, goal: NodeId):
    if start == goal:
        return [start]
    q = deque([start])
    prev = {start: None}
    while q:
        u = q.popleft()
        for v in links[u]:
            if v not in prev:
                prev[v] = u
                q.append(v)
                if v == goal:
                    path = [v]
                    while prev[path[-1]] is not None:
                        path.append(prev[path[-1]])
                    path.reverse()
                    return path
    return []

def draw_connections(screen, rooms, links, cam_y):
    for node, neighs in links.items():
        p1 = center_of(rooms[node].rect)
        for v in neighs:
            if v.floor < node.floor:
                continue
            p2 = center_of(rooms[v].rect)
            pygame.draw.line(screen, LINK_COLOR, (p1.x, p1.y + cam_y), (p2.x, p2.y + cam_y), 3)
