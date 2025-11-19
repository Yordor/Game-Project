import sys
import pygame

from config import WIDTH, HEIGHT
from player import Player
from monster import Monster


def fight_round(player: Player, monster: Monster):
    dmg_to_player = max(1, monster.atk - player.defense)
    player.hp -= dmg_to_player

    dmg_to_mon = max(1, player.atk - monster.defense)
    monster.hp -= dmg_to_mon

    return dmg_to_player, dmg_to_mon


def show_game_over(screen: pygame.Surface, font: pygame.font.Font):
    Restart = True
    while Restart:
        screen.fill((0, 0, 0))
        
        die_text = font.render("YOU DIE", True, (255, 50, 50))
        screen.blit(die_text,die_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        
        restart_text = font.render("Press F to Restart", True, (255, 255, 255))
        screen.blit(restart_text,restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

        pygame.display.flip()
        
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    from main import main
                    main()


def fight_until_end(screen: pygame.Surface, font: pygame.font.Font,
                    player: Player, monster: Monster):
    while monster.hp > 0 and player.hp > 0:
        fight_round(player, monster)

    if player.hp <= 0:

        show_game_over(screen, font)
def defeat_enemy(player: Player,monster: Monster):
    if monster.name == "Ghost":
        player.hp += 100
    elif monster.name == "Spider":
        player.hp += 50
        player.defense += 2
    elif monster.name == "Bat":
        player.hp += 30
        player.atk += 3
    elif monster.name == "Slime":
        player.hp += 40
        player.atk += 1
    elif monster.name == "BOSS":
        player.hp += 200
        player.atk += 5
        player.defense += 3



