import pygame

WIDTH, HEIGHT, FPS = 750, 750, 60
FLOORS, COLS = 3, 2
ROOM_W, ROOM_H = 140, 110
FLOOR_GAP, COL_GAP = 150, 30
PLAYER_SPEED = 250.0
BG = (18, 20, 28)
ROOM = (70, 110, 160)
ROOM_TARGET = (255, 190, 90)
PLAYER_COLOR = (255, 236, 90)
PLAYER_IMG_PATH = "player.png"
PLAYER_IMG_SIZE = (46, 46)

pygame.init()

def center(rect):
    return pygame.Vector2(rect.centerx, rect.centery)

def build_rooms():
    rooms = {}
    total_w = COLS * ROOM_W + (COLS - 1) * COL_GAP
    start_x = (WIDTH - total_w) // 2
    cols_x = [start_x + c * (ROOM_W + COL_GAP) for c in range(COLS)]
    for f in range(FLOORS):
        y = HEIGHT - 120 - f * FLOOR_GAP
        for c in range(COLS):
            rooms[(f, c)] = pygame.Rect(cols_x[c], y, ROOM_W, ROOM_H)
    return rooms

def in_bounds(node):
    f, c = node
    return 0 <= f < FLOORS and 0 <= c < COLS

def is_neighbor(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1])) == 1

def load_player_image():
    try:
        img = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
        if PLAYER_IMG_SIZE:
            img = pygame.transform.smoothscale(img, PLAYER_IMG_SIZE)
        return img
    except Exception as e:
        return None

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("เกมหอคอยสุดโหดดXD")
    clock = pygame.time.Clock()

    rooms = build_rooms()
    start = (0, 1) if (0, 1) in rooms else (0, 0)
    current = start
    target = start
    player_pos = center(rooms[current])

    player_img = load_player_image()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key in (pygame.K_LEFT, pygame.K_a):
                    nxt = (current[0], current[1] - 1)
                    if in_bounds(nxt): target = nxt
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    nxt = (current[0], current[1] + 1)
                    if in_bounds(nxt): target = nxt
                elif e.key in (pygame.K_UP, pygame.K_w):
                    nxt = (current[0] + 1, current[1])
                    if in_bounds(nxt): target = nxt
                elif e.key in (pygame.K_DOWN, pygame.K_s):
                    nxt = (current[0] - 1, current[1])
                    if in_bounds(nxt): target = nxt

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                clicked = None
                for node, rect in rooms.items():
                    if rect.collidepoint(mx, my):
                        clicked = node
                        break
                if clicked and is_neighbor(current, clicked):
                    target = clicked

        goal = center(rooms[target])
        delta = goal - player_pos
        dist = delta.length()
        if dist > 1.0:
            step = min(dist, PLAYER_SPEED * dt)
            player_pos += delta.normalize() * step
        else:
            player_pos = goal
            current = target

        screen.fill(BG)
        for rect in rooms.values():
            pygame.draw.rect(screen, ROOM, rect, border_radius=8)
        pygame.draw.rect(screen, ROOM_TARGET, rooms[target], width=3, border_radius=8)

        if player_img:
            offx, offy = player_img.get_width() // 2, player_img.get_height() // 2
            screen.blit(player_img, (player_pos.x - offx, player_pos.y - offy))
        else:
            pr = pygame.Rect(0, 0, 32, 42)
            pr.center = (int(player_pos.x), int(player_pos.y))
            pygame.draw.rect(screen, PLAYER_COLOR, pr, border_radius=8)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
