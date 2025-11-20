import sys
import pygame

from button import Button
from config import (
    WIDTH, HEIGHT, FPS,
    PLAYER_SPEED, CAM_FOLLOW,
    PLAYER_IMG_PATH,
    BG, TEXT,
)
from player import Player
from tower import (
    center_of,
    load_monster_images, load_item_images,load_room_backgrounds,
    build_tower, is_neighbor,
    draw_direction_arrows, draw_rooms_and_entities,
)
from combat import fight_until_end,defeat_enemy
from item import apply_item,ITEM_STATS

pygame.init()
FONT = pygame.font.SysFont("consolas", 20)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

def load_player_image():
    try:
        img = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
        return pygame.transform.smoothscale(img, (60, 60))
    except:
        return None
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)
def draw_text(text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    SCREEN.blit(img, (x, y))

def main_menu():
    while True:

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(150).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(940, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(940, 450),
                         text_input="PLAY", font=get_font(75), base_color="#000000", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(940, 750),
                         text_input="QUIT", font=get_font(75), base_color="#000000", hovering_color="White")
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
def end(HP,ATK,DEF):
    running = True
    while running:
        SCREEN.fill((0, 0, 0))
        draw_text("Final Score",get_font((150)),(255,255,255),640,150)
        draw_text(f"HP score = {HP}", get_font((75)), (255, 255, 255), 640, 450)
        draw_text(f"Attack score  {ATK} * 10 = {ATK*10}", get_font((75)), (255, 255, 255), 640, 550)
        draw_text(f"Defense score {DEF} * 10 = {DEF*10}", get_font((75)), (255, 255, 255), 640, 650)
        draw_text(f"Final score =  {HP+ATK*10+DEF*10}", get_font((75)), (255, 255, 255), 640, 750)
        draw_text(f"Press F To Restart", get_font((75)),(255, 255, 255), 640, 850)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    from main import main
                    main()    

        pygame.display.flip()
def main():
    pygame.init()
    Cooldown = 0
    Winner = 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("เกมไต่หอคอยสุดโหดดดด")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("consolas", 20)

    rooms, links, monsters, items, BOSS_ID, stair = build_tower()
    player = Player()

    player_img = load_player_image()
    if player_img:
        img_off = pygame.Vector2(player_img.get_width() // 2,
                                 player_img.get_height() // 2)
    else:
        img_off = pygame.Vector2(0, 0)

    monster_images = load_monster_images()
    item_images = load_item_images()
    room_bg, boss_bg = load_room_backgrounds()
    
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
                elif e.key == pygame.K_e and Winner == 1:
                    end(player.hp, player.atk, player.defense)
                else:
                    f, c = current
                    candidate = None
                    if Cooldown == 0:
                        if e.key == pygame.K_LEFT:
                            Cooldown = 1
                            cand = (f, c - 1)
                            if cand in links[current]:
                                candidate = cand
                        elif e.key == pygame.K_RIGHT:
                            Cooldown = 1
                            cand = (f, c + 1)
                            if cand in links[current]:
                                candidate = cand
                        elif e.key == pygame.K_UP:
                            Cooldown = 1
                            cand = (f + 1, c)
                            if cand in links.get(current, []):
                                candidate = cand
                        elif e.key == pygame.K_DOWN:
                            Cooldown = 1
                            cand = (f - 1, c)
                            if cand in links.get(current, []):
                                candidate = cand
                    if candidate:
                        path = [current, candidate]
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and Cooldown == 0:
                Cooldown = 1
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

                if current in monsters:
                    mon = monsters[current]
                    fight_until_end(screen, font, player, mon)

                    if mon.hp <= 0:
                        if mon.name == "BOSS":
                            Winner = 1
                            pygame.display.flip()
                        defeat_enemy(player,mon)
                        del monsters[current]

                if current in items and player.hp > 0:
                    item_name = items[current]
                    apply_item(player, item_name)
                    del items[current]

            else:
                step = PLAYER_SPEED * dt
                pos.x += step * dx / dist
                pos.y += step * dy / dist
        else:
            path = [current]
            Cooldown = 0
        # กล้องตามผู้เล่น
        cam_y += ((HEIGHT * 0.45 - (pos.y + cam_y)) * CAM_FOLLOW)

        screen.fill(BG)

        draw_rooms_and_entities(screen, rooms, monsters, items,
                                BOSS_ID, cam_y, monster_images, item_images,
                                room_bg, boss_bg, font)

        neighbors = {"self": current, "list": links.get(current, [])}
        draw_direction_arrows(screen, rooms[current], neighbors, cam_y)

        # วาดผู้เล่น
        if player_img:
            screen.blit(player_img,
                        (pos.x - img_off.x, pos.y - img_off.y + cam_y))
        else:
            pr = pygame.Rect(0, 0, 30, 40)
            pr.center = (int(pos.x), int(pos.y + cam_y))
            pygame.draw.rect(screen, (255, 236, 90), pr, border_radius=8)

        player_text = font.render(
            f"PLAYER | HP:{player.hp}  ATK:{player.atk}  DEF:{player.defense}",
            True, TEXT
        )
        screen.blit(player_text, (15, HEIGHT - 80))

        if current in monsters:
            mon_now = monsters[current]
            mon_text = font.render(
                f"{mon_now.name} | HP:{mon_now.hp}  ATK:{mon_now.atk}  DEF:{mon_now.defense}",
                True, TEXT
            )
        else:
            mon_text = font.render("", True, TEXT)
        screen.blit(mon_text, (15, HEIGHT - 50))
        
        mx, my = pygame.mouse.get_pos()
        mon_ui = None
        item_ui = None
        for key, mon in monsters.items():
            rect = rooms[key]
            rr = rect.copy()
            rr.y += cam_y
            if rr.collidepoint(mx, my):
                mon_ui = mon
                break
        for key, item_1 in items.items():
            rect = rooms[key]
            rr = rect.copy()
            rr.y += cam_y
            if rr.collidepoint(mx, my):
                item_ui = item_1
                break
        if mon_ui:
            mon_ui_text = font.render(f"{mon_ui.name} | HP:{mon_ui.hp}  ATK:{mon_ui.atk}  DEF:{mon_ui.defense}",True, (255, 255, 255))
            SCREEN.blit(mon_ui_text, (mx+30, my+30))
        if item_ui:
            stats = ITEM_STATS[item_ui]
            bonus = ""
            for stats, amount in stats.items():
                bonus = f"+{amount} {stats}"
            if item_ui:
                item_ui_text = font.render(f"{item_ui} | {bonus}",True, (255, 255, 255))
            SCREEN.blit(item_ui_text, (mx+30, my+30))
        if Winner == 1:
            draw_text("Press E to Finish the game", get_font((40)), (255, 255, 255), 40, 0)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":

    main_menu()




