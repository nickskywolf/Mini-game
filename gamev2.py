import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_LEFT, K_UP, K_RIGHT
import pygame_menu

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

FONT = pygame.font.SysFont("Verdana", 30)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

player_size = (20, 20)
player = pygame.image.load("player.png").convert_alpha()
player_rect = player.get_rect()
player_rect.centery = HEIGHT // 2

player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]

score = 0

def create_enemy():
    enemy_image = pygame.image.load("enemy.png").convert_alpha()
    enemy_width = enemy_image.get_width()
    enemy_height = enemy_image.get_height()

    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - enemy_height), enemy_width, enemy_height)
    enemy_move = [random.randint(-6, -4), 0]
    return [enemy_image, enemy_rect, enemy_move]

enemies = []

CREATE_ENEMY = pygame.USEREVENT +1
pygame.time.set_timer(CREATE_ENEMY, 1500)

def create_bonus():
    bonus_image = pygame.image.load("bonus.png").convert_alpha()
    bonus_width = bonus_image.get_width()
    bonus_height = bonus_image.get_height()

    bonus_rect = pygame.Rect(random.randint(0, WIDTH - bonus_width), -bonus_height, bonus_width, bonus_height)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus_image, bonus_rect, bonus_move]


CREATE_BONUS = pygame.USEREVENT +2
pygame.time.set_timer(CREATE_BONUS, 1500)

bonuses = []

def start_game():
    global playing, game_active
    playing = True
    game_active = True
    print("Starting game...")



menu = pygame_menu.Menu('Main Menu', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
menu.add.button('Start', start_game)
menu.add.button('Exit', QUIT)

bonuses = []

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

game_over = False
game_active = False
playing = False

while True:
    while not playing:
        menu.mainloop(main_display)
    
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            game_over = True

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1
    
    if game_over:
        # Отображение сообщения об окончании игры и кнопки перезапуска
        pass
    elif game_active:
        # Отображение игровых объектов, обработка действий игрока и врагов
        main_display.blit(bg, (bg_x1, 0))
        main_display.blit(bg, (bg_x2, 0))
        main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-60, 20))
        main_display.blit(player, player_rect)
        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])
            if player_rect.colliderect(enemy[1]):
                game_over = True
        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])
            if player_rect.colliderect(bonus[1]):
                bonuses.pop(bonuses.index(bonus))
                score += 1
        for enemy in enemies:
            if enemy[1].left < 0:
                enemies.pop(enemies.index(enemy))
        for bonus in bonuses:
            if bonus[1].bottom > HEIGHT:
                bonuses.pop(bonuses.index(bonus))
        pygame.display.flip()

    menu.clear()
    pygame.display.update()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
