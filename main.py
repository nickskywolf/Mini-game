import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_LEFT, K_UP, K_RIGHT
import pygame_menu

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

bg = pygame.transform.scale (pygame.image.load("background.png"), (WIDTH, HEIGHT))
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
player = pygame.image.load("player.png").convert_alpha() #pygame.Surface(player_size)
player_rect = player.get_rect()
player_rect.centery = HEIGHT // 2  # Установка координаты Y в центре экрана

# player_speed = [1, 1]
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

game_over = False
game_over_text = FONT.render("Вы проиграли", True, COLOR_BLACK)
restart_text = FONT.render("Нажмите клавишу Пробел или Enter, чтобы начать сначала", True, COLOR_BLACK)

playing = True

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Сброс состояния игры и перезапуск
                score = 0
                enemies = []
                bonuses = []
                player_rect.centery = HEIGHT // 2
                game_over = False
       
    bg_x1 -= bg_move
    bg_x2 -= bg_move


    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

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


        # if player_rect.colliderect(enemy[1]):
            

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1
    
    if game_over:
        score_text = FONT.render(f"Вы заработали {score} очков", True, COLOR_BLACK)
        text_width = score_text.get_width()
        text_height = score_text.get_height()
        main_display.blit(score_text, (WIDTH // 2 - text_width // 2, HEIGHT // 2))

        text_width = game_over_text.get_width()
        text_height = game_over_text.get_height()
        main_display.blit(game_over_text, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - text_height))
        text_width = score_text.get_width()
        text_height = score_text.get_height()
        main_display.blit(score_text, (WIDTH // 2 - text_width // 2, HEIGHT // 2))
        text_width = restart_text.get_width()
        text_height = restart_text.get_height()
        main_display.blit(restart_text, (WIDTH // 2 - text_width // 2, HEIGHT // 2 + text_height))

    # Ожидание нажатия клавиши для перезапуска игры
    # Ожидание нажатия клавиши для перезапуска игры
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Сброс состояния игры и перезапуск
                score = 0
                enemies = []
                bonuses = []
                player_rect.centery = HEIGHT // 2
                game_over = False


    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-60, 20) )
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
 