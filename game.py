import pygame

WIDTH, HEIGHT, FPS = 750, 750, 60
FLOORS, COLS = 6, 5
ROOM_W, ROOM_H = 140, 110
FLOOR_GAP, COL_GAP = 150, 30
PLAYER_SPEED = 250.0
CAM_FOLLOW = 0.1
ARRIVE_EPS = 2.5

BG = (18, 20, 28)
ROOM = (70, 110, 160)
ROOM_TARGET = (255, 190, 90)
PLAYER_COLOR = (255, 236, 90)
ARROW_COLOR = (255, 230, 100)
BOSS_FILL = (190, 60, 60)
BOSS_BORDER = (255, 120, 120)
TEXT_COLOR = (255, 240, 240)

PLAYER_IMG_PATH = "player.png"
PLAYER_IMG_SIZE = (46, 46)

pygame.init()
FONT = pygame.font.SysFont("consolas", 28, bold=True)

def center(r): return pygame.Vector2(r.centerx, r.centery)

def build_tower():
    rooms, links = {}, {}
    total_w = COLS * ROOM_W + (COLS - 1) * COL_GAP
    start_x = (WIDTH - total_w) // 2
    cols_x = [start_x + c * (ROOM_W + COL_GAP) for c in range(COLS)]

    for f in range(FLOORS - 1):
        y = HEIGHT - 120 - f * FLOOR_GAP
        for c in range(COLS):
            rooms[(f, c)] = pygame.Rect(cols_x[c], y, ROOM_W, ROOM_H)

    top = FLOORS - 1
    y = HEIGHT - 120 - top * FLOOR_GAP
    bw = WIDTH - 60
    bh = int(ROOM_H * 1.4)
    bx = (WIDTH - bw) // 2
    boss = (top, 0)
    rooms[boss] = pygame.Rect(bx, y, bw, bh)

    for f in range(FLOORS - 1):
        for c in range(COLS):
            n = (f, c)
            links.setdefault(n, [])
            if c > 0: links[n].append((f, c - 1))
            if c < COLS - 1: links[n].append((f, c + 1))
            if f < FLOORS - 2: links[n].append((f + 1, c))
            if f > 0: links[n].append((f - 1, c))

    top_minus_1 = FLOORS - 2
    for c in range(COLS):
        links[(top_minus_1, c)].append(boss)
        links.setdefault(boss, []).append((top_minus_1, c))

    return rooms, links, boss

def load_img():
    try:
        i = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
        if PLAYER_IMG_SIZE:
            i = pygame.transform.smoothscale(i, PLAYER_IMG_SIZE)
        return i
    except:
        return None

def draw_arrow(screen, start, end, cam_y):
    d = end - start
    if d.length_squared() == 0:
        return
    vec = d.normalize() * 25
    tip = start + vec
    perp = pygame.Vector2(-vec.y, vec.x).normalize() * 6
    pts = [(tip.x, tip.y + cam_y),
           (start.x - perp.x, start.y - perp.y + cam_y),
           (start.x + perp.x, start.y + perp.y + cam_y)]
    pygame.draw.polygon(screen, ARROW_COLOR, pts)

def main():
    s = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tower (smooth move)")
    clock = pygame.time.Clock()
    rooms, links, boss = build_tower()

    cur = tar = (0, 1)
    pos = center(rooms[cur])
    img = load_img()
    cam_y = 0.0
    boss_msg = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            elif e.type == pygame.KEYDOWN:
                cand = None
                if e.key in (pygame.K_LEFT, pygame.K_a):   cand = (cur[0], cur[1]-1)
                elif e.key in (pygame.K_RIGHT, pygame.K_d): cand = (cur[0], cur[1]+1)
                elif e.key in (pygame.K_UP, pygame.K_w):    cand = (cur[0]+1, cur[1])
                elif e.key in (pygame.K_DOWN, pygame.K_s):  cand = (cur[0]-1, cur[1])
                if cand is not None and cand in links[cur]:
                    tar = cand
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                wy = my - cam_y
                click = None
                for n, r in rooms.items():
                    if r.collidepoint(mx, wy):
                        click = n
                        break
                if click and click in links[cur]:
                    tar = click

        goal = center(rooms[tar])
        d = goal - pos
        dist = d.length()

        if dist <= ARRIVE_EPS:
            pos = goal
            cur = tar
        else:
            step = PLAYER_SPEED * dt
            if step >= dist:
                pos = goal
                cur = tar
            else:
                if dist > 0:
                    pos += (d / dist) * step

        if cur == boss:
            boss_msg = True

        target_y = HEIGHT * 0.45
        player_screen_y = pos.y + cam_y
        cam_y += (target_y - player_screen_y) * CAM_FOLLOW

        s.fill(BG)
        for (n, r) in rooms.items():
            rr = r.copy(); rr.y += cam_y
            if n == boss:
                pygame.draw.rect(s, BOSS_FILL, rr, border_radius=14)
                pygame.draw.rect(s, BOSS_BORDER, rr, 4, 14)
            else:
                pygame.draw.rect(s, ROOM, rr, border_radius=8)

        tr = rooms[tar].copy(); tr.y += cam_y
        pygame.draw.rect(s, ROOM_TARGET, tr, 3, 14 if tar == boss else 8)

        for nb in links[cur]:
            start = center(rooms[cur])
            end = center(rooms[nb])
            draw_arrow(s, start, end, cam_y)

        if img:
            off = pygame.Vector2(img.get_width() / 2, img.get_height() / 2)
            s.blit(img, (pos.x - off.x, pos.y - off.y + cam_y))
        else:
            p = pygame.Rect(0, 0, 32, 42)
            p.center = (pos.x, pos.y + cam_y)
            pygame.draw.rect(s, PLAYER_COLOR, p, 8)

        if boss_msg:
            t = FONT.render("== BOSS ROOM ==", True, TEXT_COLOR)
            s.blit(t, (WIDTH / 2 - t.get_width() / 2, 40))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
