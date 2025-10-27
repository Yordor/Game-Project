import pygame

WIDTH, HEIGHT, FPS = 750, 750 # ขนาดหน้าต่าง + เฟรมเรต
FLOORS, COLS = 6, 5 # จำนวนชั้น + จำนวนห้องต่อชั้น
ROOM_W, ROOM_H = 140, 110 # ขนาดห้อง(มอน)
FLOOR_GAP, COL_GAP = 150, 30 # ระยะห่างระหว่างชั้น/ห้อง
PLAYER_SPEED = 250.0 # ความเร็วผู้เล่น
CAM_FOLLOW = 0.1 # ความหนืดของกล้อง
ARRIVE_EPS = 2.5 # ระยะที่จะรู้ว่าถึงตรงกลางห้องแล้ว

BG = (18, 20, 28) # สีพื้นหลัง
ROOM = (70, 110, 160) # สีห้องธรรมดา
ROOM_TARGET = (255, 190, 90) # เส้นกรอบของห้องเป้าหมาย
PLAYER_COLOR = (255, 236, 90) # สีผู้เล่น(ถ้าโหลดรูปไม่ได้)
ARROW_COLOR = (255, 230, 100) # สีลูกศร
BOSS_FILL = (190, 60, 60) # สีห้องบอส (ฺBG)
BOSS_BORDER = (255, 120, 120) # สีห้องบอส (กรอบ)
TEXT_COLOR = (255, 240, 240) # สีข้อความ

PLAYER_IMG_PATH = "player.png" # รูปผู้เล่น
PLAYER_IMG_SIZE = (46, 46) # ขนาดรูปผู้เล่น

pygame.init()
FONT = pygame.font.SysFont("consolas", 28, bold=True) # ฟอนต์สำหรับข้อความแจ้งเตือน

# ฟังก์ชันช่วย หาศูนย์กลางของ rect
def center(r: pygame.Rect) -> pygame.Vector2:
    return pygame.Vector2(r.centerx, r.centery)

# --------------------------------------------------
# สร้างหอคอย
# คืนค่า: rooms(dict), links(dict), boss_id(tuple)
# rooms[(f, c)] = pygame.Rect
# links[(f, c)] = ห้องที่สามารถเดินไปได้
# --------------------------------------------------
def build_tower():
    rooms, links = {}, {}

    # คำนวณตำแหน่งแกน x ของแต่ละคอลัมน์ให้กึ่งกลางจอ
    total_w = COLS * ROOM_W + (COLS - 1) * COL_GAP
    start_x = (WIDTH - total_w) // 2
    cols_x = [start_x + c * (ROOM_W + COL_GAP) for c in range(COLS)]

    # ห้องธรรมดา
    for f in range(FLOORS - 1):
        y = HEIGHT - 120 - f * FLOOR_GAP
        for c in range(COLS):
            rooms[(f, c)] = pygame.Rect(cols_x[c], y, ROOM_W, ROOM_H)

    # ห้องบอสในชั้นบนสุด
    top = FLOORS - 1
    y = HEIGHT - 120 - top * FLOOR_GAP
    bw = WIDTH - 60 # ความกว้างห้องบอส
    bh = int(ROOM_H * 1.4) # ความสูงห้องบอส
    bx = (WIDTH - bw) // 2
    boss = (top, 0)
    rooms[boss] = pygame.Rect(bx, y, bw, bh)

    # สร้างรายชื่อของห้องธรรมดา
    for f in range(FLOORS - 1):
        for c in range(COLS):
            n = (f, c)
            links.setdefault(n, [])
            # ซ้าย/ขวา
            if c > 0: links[n].append((f, c - 1))
            if c < COLS - 1: links[n].append((f, c + 1))
            # ขึ้น/ลง
            if f < FLOORS - 2: links[n].append((f + 1, c))
            if f > 0: links[n].append((f - 1, c))

    top_minus_1 = FLOORS - 2
    for c in range(COLS):
        links[(top_minus_1, c)].append(boss)
        links.setdefault(boss, []).append((top_minus_1, c))

    return rooms, links, boss


# โหลดรูปผู้เล่น
def load_img():
    try:
        img = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
        if PLAYER_IMG_SIZE:
            img = pygame.transform.smoothscale(img, PLAYER_IMG_SIZE)
        return img
    except Exception as e:
        print(f"[WARN] โหลดรูปผู้เล่นไม่ได้: {e}")
        return None
#------------------------------------------
# วาดลูกศรสามเหลี่ยม(บอกห้องเดินที่ไปได้)
# cam_y เลื่อนเลื่อนหน้าจอตามผู้เล่น
#------------------------------------------
def draw_arrow(screen, start: pygame.Vector2, end: pygame.Vector2, cam_y: float):
    d = end - start
    if d.length_squared() == 0:
        return
    vec = d.normalize() * 25 # ความยาวหัวลูกศร
    tip = start + vec # จุดปลายลูกศร
    
    #วาดสามเหลี่ยม
    perp = pygame.Vector2(-vec.y, vec.x).normalize() * 6

    pts = [
        (tip.x, tip.y + cam_y),
        (start.x - perp.x, start.y - perp.y + cam_y),
        (start.x + perp.x, start.y + perp.y + cam_y)
    ]
    pygame.draw.polygon(screen, ARROW_COLOR, pts)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("เกมหอคอย:D")

    clock = pygame.time.Clock()

    # สร้างแผนที่ + ทางเดิน + ห้องบอส
    rooms, links, boss = build_tower()

    # ห้องstart + ตำแหน่งผู้เล่น
    cur = tar = (0, 1)
    pos = center(rooms[cur])

    # โหลดรูปผู้เล่น ถ้าไม่ได้ใช้สี่เหลี่ยมแทน
    img = load_img()

    # กล้องแกน y + แสดงข้อความบอส
    cam_y = 0.0
    boss_msg = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for e in pygame.event.get():
            # ปิดเกม
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False

            # คลิกเมาส์ (เลือกห้องที่จะเดิน)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                wy = my - cam_y # พิกัดกล้อง
                click = None
                for n, r in rooms.items():
                    if r.collidepoint(mx, wy):
                        click = n
                        break
                if click and click in links[cur]: # คลิกได้เเค่ห้องที่ติดกัน
                    tar = click
            # เดินเหมือนกันเเค่เป็นปุ่มลูกศร       
            elif e.type == pygame.KEYDOWN:
                cand = None
                if e.key in (pygame.K_LEFT, pygame.K_a):   cand = (cur[0], cur[1] - 1)
                elif e.key in (pygame.K_RIGHT, pygame.K_d): cand = (cur[0], cur[1] + 1)
                elif e.key in (pygame.K_UP, pygame.K_w):    cand = (cur[0] + 1, cur[1])
                elif e.key in (pygame.K_DOWN, pygame.K_s):  cand = (cur[0] - 1, cur[1])
                if cand is not None and cand in links[cur]:
                    tar = cand

        # อัปเดตการเคลื่อนที่ของผู้เล่น
        goal = center(rooms[tar]) # ศูนย์กลางของห้องที่ไป
        d = goal - pos # เวกเตอร์ทิศทาง
        dist = d.length() # ระยะห่างถึงเป้าหมาย

        if dist <= ARRIVE_EPS:
            # ถ้าเข้าใกล้ห้องใหม่มากพอ จะอัปเดตเป็นห้องปัจจุบัน
            pos = goal
            cur = tar
        else:
            step = PLAYER_SPEED * dt
            if step >= dist:
                # ถ้าก้าวเกินระยะที่เหลือจะปัดเป็นศูนย์กลางเลย จะได้ไม่สั่น
                pos = goal
                cur = tar
            else:
                if dist > 0:
                    pos += (d / dist) * step

        # ถ้าเข้าห้องบอส ให้ขึ้นว่าเจอบอสเเล้ว
        if cur == boss:
            boss_msg = True

        # กล้องตามผู้เล่น
        target_y = HEIGHT * 0.45
        player_screen_y = pos.y + cam_y
        cam_y += (target_y - player_screen_y) * CAM_FOLLOW

        screen.fill(BG)

        # วาดห้องทุกห้อง
        for (n, r) in rooms.items():
            rr = r.copy()
            rr.y += cam_y
            if n == boss:
                pygame.draw.rect(screen, BOSS_FILL, rr, border_radius=14)
                pygame.draw.rect(screen, BOSS_BORDER, rr, 4, 14)
            else:
                pygame.draw.rect(screen, ROOM, rr, border_radius=8)

        # วาดกรอบของห้องที่ไป
        tr = rooms[tar].copy()
        tr.y += cam_y
        pygame.draw.rect(screen, ROOM_TARGET, tr, 3, 14 if tar == boss else 8)

        # วาดลูกศรบอกห้องที่ไปได้ จากห้องปัจจุบันไปห้องข้างๆ
        for nb in links[cur]:
            start = center(rooms[cur])
            end = center(rooms[nb])
            draw_arrow(screen, start, end, cam_y)

        # วาดผู้เล่น
        if img:
            off = pygame.Vector2(img.get_width() / 2, img.get_height() / 2)
            screen.blit(img, (pos.x - off.x, pos.y - off.y + cam_y))
        else:
            p = pygame.Rect(0, 0, 32, 42)
            p.center = (pos.x, pos.y + cam_y)
            pygame.draw.rect(screen, PLAYER_COLOR, p, border_radius=8)

        # ข้อความแจ้งเตือนตอนอยู่ในห้องบอส
        if boss_msg:
            t = FONT.render("== BOSS ROOM ==", True, TEXT_COLOR)
            screen.blit(t, (WIDTH / 2 - t.get_width() / 2, 40))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
