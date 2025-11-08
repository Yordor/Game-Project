import pygame

# ---------- CONFIG ----------
WIDTH, HEIGHT = 1920, 1080
FPS = 60

FLOORS = 8
COLS = 4
ROOM_W, ROOM_H = 140, 110
FLOOR_GAP = 150
COL_GAP = 30

PLAYER_SPEED = 260
CAM_FOLLOW = 0.1

PLAYER_IMG_PATH = "player.png"


BG = (18, 20, 28)
ROOM_COLOR = (80, 120, 170)
ROOM_BOSS = (190, 60, 60)
TEXT = (235, 235, 235)
ARROW_COLOR = (255, 220, 130)
ARROW_SIZE = 14
ARROW_PADDING = 56
pygame.init()
FONT = pygame.font.SysFont("consolas", 20)


def stair_col_for(cols: int) -> int:
    return (cols // 2) if (cols % 2 == 1) else (cols // 2) - 1

# ---------- Stats ----------
class Player:
    def __init__(self):
        self.hp = 120
        self.atk = 22
        self.defense = 6

class Monster:
    def __init__(self, name, stats):
        self.name = name
        self.hp = stats["HP"]
        self.atk = stats["ATK"]
        self.defense = stats["DEF"]

MONSTER_STATS = {
    "Normal":   {"HP": 50, "ATK": 10, "DEF": 3},
    "Tank(HP)": {"HP": 90, "ATK": 5,  "DEF": 4},
    "Tank(DEF)":{"HP": 50, "ATK": 5,  "DEF": 20},
    "Attack":   {"HP": 40, "ATK": 50, "DEF": 2},
    "BOSS":     {"HP": 220,"ATK": 40, "DEF": 12}
}

def center_of(rect):
    return pygame.Vector2(rect.centerx, rect.centery)

def load_player_image():
    try:
        img = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
        return pygame.transform.smoothscale(img, (46, 46))
    except:
        return None

def draw_direction_arrows(screen, room_rect: pygame.Rect, neighbors, cam_y):
    rr = room_rect.copy()
    rr.y += cam_y

    dirs = set()
    f, c = neighbors['self']
    for nf, nc in neighbors['list']:
        if nf == f and nc == c - 1: dirs.add('L')
        if nf == f and nc == c + 1: dirs.add('R')
        if nf == f + 1 and nc == c: dirs.add('U')
        if nf == f - 1 and nc == c: dirs.add('D')

    s = 14
    cx, cy = rr.centerx, rr.centery
    padding = 8

    def tri(points):
        pygame.draw.polygon(screen, ARROW_COLOR, points)

    if 'L' in dirs:
        x = rr.left + padding
        tri([(x, cy),
             (x + s, cy - s//2),
             (x + s, cy + s//2)])

    if 'R' in dirs:
        x = rr.right - padding
        tri([(x, cy),
             (x - s, cy - s//2),
             (x - s, cy + s//2)])

    if 'U' in dirs:
        y = rr.top + padding
        tri([(cx, y),
             (cx - s//2, y + s),
             (cx + s//2, y + s)])

    if 'D' in dirs:
        y = rr.bottom - padding
        tri([(cx, y),
             (cx - s//2, y - s),
             (cx + s//2, y - s)])

def build_tower():
    rooms = {}
    links = {}
    monsters = {}

    total_w = COLS * ROOM_W + (COLS - 1) * COL_GAP
    start_x = (WIDTH - total_w) // 2
    cols_x = [start_x + i * (ROOM_W + COL_GAP) for i in range(COLS)]
    stair = stair_col_for(COLS)

    # ชั้นปกติ
    for f in range(FLOORS - 1):
        y = HEIGHT - 120 - f * FLOOR_GAP
        for c in range(COLS):
            rooms[(f, c)] = pygame.Rect(cols_x[c], y, ROOM_W, ROOM_H)
            order = ["Normal", "Tank(HP)", "Tank(DEF)", "Attack"]
            name = order[f % len(order)]
            monsters[(f, c)] = Monster(name, MONSTER_STATS[name])

    # ชั้นบอส
    top = FLOORS - 1
    y = HEIGHT - 120 - top * FLOOR_GAP
    boss_rect = pygame.Rect(start_x, y, total_w, int(ROOM_H * 1.2))
    rooms[(top, stair)] = boss_rect
    monsters[(top, stair)] = Monster("BOSS", MONSTER_STATS["BOSS"])
    BOSS_ID = (top, stair)

    for f in range(FLOORS - 1):
        for c in range(COLS):
            neigh = []
            if c - 1 >= 0: neigh.append((f, c - 1))
            if c + 1 < COLS: neigh.append((f, c + 1))
            if c == stair:
                if f + 1 < FLOORS - 1: neigh.append((f + 1, c))
                if f - 1 >= 0: neigh.append((f - 1, c))
            links[(f, c)] = neigh

    links[(FLOORS - 2, stair)].append(BOSS_ID)
    links[BOSS_ID] = [(FLOORS - 2, stair)]

    return rooms, links, monsters, BOSS_ID, stair

def is_neighbor(links, a, b):
    return b in links.get(a, [])

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("เกมหอคอย (เมาส์ + ลูกศร และลูกศรบอกทิศ)")
    clock = pygame.time.Clock()

    rooms, links, monsters, BOSS_ID, stair = build_tower()
    player = Player()

    player_img = load_player_image()
    if player_img:
        img_off = pygame.Vector2(player_img.get_width() // 2, player_img.get_height() // 2)

    current = (0, stair)
    pos = center_of(rooms[current])
    path = [current]
    cam_y = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                else:
                    f, c = current
                    candidate = None
                    if e.key == pygame.K_LEFT:
                        cand = (f, c - 1)
                        if cand in links[current]: candidate = cand
                    elif e.key == pygame.K_RIGHT:
                        cand = (f, c + 1)
                        if cand in links[current]: candidate = cand
                    elif e.key == pygame.K_UP:
                        cand = (f + 1, c)
                        if cand in links.get(current, []):
                            candidate = cand
                    elif e.key == pygame.K_DOWN:
                        cand = (f - 1, c)
                        if cand in links.get(current, []):
                            candidate = cand

                    if candidate:
                        path = [current, candidate]

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                world_y = my - cam_y
                clicked = None
                for key, rect in rooms.items():
                    if rect.collidepoint(mx, world_y):
                        clicked = key
                        break
                if clicked and is_neighbor(links, current, clicked):
                    path = [current, clicked]

        # การเคลื่อนที่
        if len(path) >= 2:
            nxt = path[1]
            goal = center_of(rooms[nxt])
            dx, dy = goal.x - pos.x, goal.y - pos.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist < 2:
                pos = goal
                current = nxt
                path.pop(0)
            else:
                step = PLAYER_SPEED * dt
                pos.x += step * dx / dist
                pos.y += step * dy / dist
        else:
            path = [current]


        cam_y += ((HEIGHT * 0.45 - (pos.y + cam_y)) * CAM_FOLLOW)

        screen.fill(BG)

        # ห้องทั้งหมด
        for key, rect in rooms.items():
            rr = rect.copy(); rr.y += cam_y
            color = ROOM_BOSS if key == BOSS_ID else ROOM_COLOR
            pygame.draw.rect(screen, color, rr, border_radius=10)
            if key == BOSS_ID:
                label = FONT.render("BOSS", True, TEXT)
                screen.blit(label, (rr.centerx - label.get_width() // 2, rr.y + 8))

        # วาดลูกศร
        neighbors = {"self": current, "list": links.get(current, [])}
        draw_direction_arrows(screen, rooms[current], neighbors, cam_y)

        # ผู้เล่น
        if player_img:
            screen.blit(player_img, (pos.x - img_off.x, pos.y - img_off.y + cam_y))
        else:
            pr = pygame.Rect(0, 0, 30, 40)
            pr.center = (int(pos.x), int(pos.y + cam_y))
            pygame.draw.rect(screen, (255, 236, 90), pr, border_radius=8)

        screen.blit(FONT.render(f"PLAYER | HP:{player.hp}  ATK:{player.atk}  DEF:{player.defense}", True, TEXT), (15, HEIGHT - 80))
        mon = monsters[current]
        screen.blit(FONT.render(f"{mon.name} | HP:{mon.hp}  ATK:{mon.atk}  DEF:{mon.defense}", True, TEXT), (15, HEIGHT - 50))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
