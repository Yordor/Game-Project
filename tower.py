import pygame

from config import (
    WIDTH, HEIGHT,
    FLOORS, COLS, ROOM_W, ROOM_H, FLOOR_GAP, COL_GAP,
    ROOM_LAYOUT,
    MONSTER_IMG_PATHS, ITEM_IMG_PATHS,
    ROOM_COLOR, ROOM_BOSS, ARROW_COLOR,
    ROOM_BG_IMAGE, BOSS_ROOM_BG_IMAGE
)
from monster import Monster, MONSTER_STATS
from item import ITEM_STATS
def stair_col_for(cols: int) -> int:
    #หาตรงกลางของcol
    return (cols // 2) if (cols % 2 == 1) else (cols // 2) - 1


def center_of(rect: pygame.Rect) -> pygame.Vector2:
    return pygame.Vector2(rect.centerx, rect.centery)


def load_monster_images():
    images = {}
    for name, path in MONSTER_IMG_PATHS.items():
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (70, 70))
            images[name] = img
        except:
            images[name] = None
    return images


def load_item_images():
    images = {}
    for name, path in ITEM_IMG_PATHS.items():
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (50, 50))
            images[name] = img
        except:
            images[name] = None
    return images

def load_room_backgrounds():
    bg_normal = pygame.image.load(ROOM_BG_IMAGE).convert()
    bg_normal = pygame.transform.scale(bg_normal, (ROOM_W, ROOM_H))

    bg_boss_raw = pygame.image.load(BOSS_ROOM_BG_IMAGE).convert()
    bg_boss = pygame.transform.scale(bg_boss_raw, (ROOM_W * 5, ROOM_H * 3)) 

    return bg_normal, bg_boss

def build_tower():
    rooms = {}
    links = {}
    monsters = {}
    items = {}

    total_w = COLS * ROOM_W + (COLS - 1) * COL_GAP
    start_x = (WIDTH - total_w) // 2
    cols_x = [start_x + i * (ROOM_W + COL_GAP) for i in range(COLS)]
    stair = stair_col_for(COLS)

    # สร้างห้องธรรมดา
    for f in range(FLOORS - 1):
        y = HEIGHT - 120 - f * FLOOR_GAP
        for c in range(COLS):
            rooms[(f, c)] = pygame.Rect(cols_x[c], y, ROOM_W, ROOM_H)
            name = ROOM_LAYOUT.get((f, c))

            if name is None:
                continue

            if name in MONSTER_STATS:
                monsters[(f, c)] = Monster(name)
            elif name in ITEM_STATS:
                items[(f, c)] = name

    # ห้องบอสชั้นบนสุด
    top = FLOORS - 1
    boss_h = ROOM_H * 2
    base_y = HEIGHT - 120 - top * FLOOR_GAP
    boss_y = base_y - (boss_h - ROOM_H)
    total_w = COLS * ROOM_W + (COLS - 1) * COL_GAP
    start_x = (WIDTH - total_w) // 2

    rooms[(top, stair)] = pygame.Rect(start_x, boss_y, total_w, boss_h)
    monsters[(top, stair)] = Monster("BOSS")
    BOSS_ID = (top, stair)

    # ทางเดิน
    for f in range(FLOORS - 1):
        for c in range(COLS):
            neigh = []
            if c - 1 >= 0:
                neigh.append((f, c - 1))
            if c + 1 < COLS:
                neigh.append((f, c + 1))
            if f + 1 < FLOORS - 1:
                neigh.append((f + 1, c))
            if f - 1 >= 0:
                neigh.append((f - 1, c))
            links[(f, c)] = neigh

    # ลิงก์ระหว่างชั้นบนสุดกับห้องบอส
    for c in range(COLS):
        links[(FLOORS - 2, c)].append(BOSS_ID)
    links[BOSS_ID] = [(FLOORS - 2, c) for c in range(COLS)]

    return rooms, links, monsters, items, BOSS_ID, stair


def is_neighbor(links, a, b):
    return b in links.get(a, [])


def draw_direction_arrows(screen, room_rect: pygame.Rect, neighbors, cam_y):
    rr = room_rect.copy()
    rr.y += cam_y

    dirs = set()
    f, c = neighbors['self']
    for nf, nc in neighbors['list']:
        if nf == f and nc == c - 1:
            dirs.add('L')
        if nf == f and nc == c + 1:
            dirs.add('R')
        if nf == f + 1 and nc == c:
            dirs.add('U')
        if nf == f - 1 and nc == c:
            dirs.add('D')

    s = 14
    cx, cy = rr.centerx, rr.centery
    padding = 16

    def tri(points):
        pygame.draw.polygon(screen, ARROW_COLOR, points)

    if 'L' in dirs:
        x = rr.left + padding
        tri([(x, cy), (x + s, cy - s // 2), (x + s, cy + s // 2)])
    if 'R' in dirs:
        x = rr.right - padding
        tri([(x, cy), (x - s, cy - s // 2), (x - s, cy + s // 2)])
    if 'U' in dirs:
        y = rr.top + padding
        tri([(cx, y), (cx - s // 2, y + s), (cx + s // 2, y + s)])
    if 'D' in dirs:
        y = rr.bottom - padding
        tri([(cx, y), (cx - s // 2, y - s), (cx + s // 2, y - s)])


def draw_rooms_and_entities(screen, rooms, monsters, items,
                            BOSS_ID, cam_y, monster_images, item_images,
                            room_bg, boss_bg, font):
    #ห้องมอน + ไอเท็ม
    for key, rect in rooms.items():
        rr = rect.copy()
        rr.y += cam_y

        if key == BOSS_ID:
            bg_x = rr.centerx - boss_bg.get_width() // 2
            bg_y = rr.y + (rr.height - boss_bg.get_height())
            screen.blit(boss_bg, (bg_x, bg_y))
        else:
            screen.blit(room_bg, (rr.x, rr.y))

        if key == BOSS_ID:
            label = font.render("BOSS", True, (255, 255, 255))
            screen.blit(label,
                        (rr.centerx - label.get_width() // 2, rr.y + 8))

        mon_here = monsters.get(key)
        if mon_here:
            img = monster_images.get(mon_here.name)
            if img:
                mx = rr.centerx - img.get_width() // 2
                my = rr.centery - img.get_height() // 2
                screen.blit(img, (mx, my))
        elif key in items:
            item_name = items[key]
            img = item_images.get(item_name)
            if img:
                mx = rr.centerx - img.get_width() // 2
                my = rr.centery - img.get_height() //2
                screen.blit(img, (mx, my))