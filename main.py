import random
import os
import pygame

from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()

HEIGHT = 800
WIDTH = 1200
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

COLOR_BLUE = (66, 135, 245)
COLOR_CRIMSON = (245, 66, 129)
COLOR_GREEN = (71, 171, 5)
COLOR_YELLOW = (255, 201, 23)
COLOR_RED = (186, 12, 0)

FONT = pygame.font.SysFont('Verdana', 20)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

BACKGROUND = pygame.transform.scale(pygame.image.load('./images/background.png'), (WIDTH, HEIGHT))
BACKGROUND_STEP = 3
bg_X1 = 0
bg_X2 = BACKGROUND.get_width()

PLAYER_IMAGE_PATH = './images/player'
PLAYER_IMAGES = os.listdir(PLAYER_IMAGE_PATH)
player_image_index = 0

player = pygame.image.load(os.path.join(PLAYER_IMAGE_PATH, PLAYER_IMAGES[player_image_index])).convert_alpha()

position = pygame.Rect(
    250,
    (HEIGHT - player.get_height()) / 2,
    player.get_width(),
    player.get_height()
)

def create_enemy():
    enemy = pygame.image.load('./images/enemy.png').convert_alpha()
    position = pygame.Rect(
        WIDTH,
        random.randint(0, HEIGHT - enemy.get_height()),
        enemy.get_width(),
        enemy.get_height()
    )
    step = [random.randint(-8, -4), 0]

    return [enemy, position, step]

def create_bonus():
    bonus = pygame.image.load('./images/bonus.png').convert_alpha()
    position = pygame.Rect(
        random.randint(0, WIDTH - bonus.get_width()),
        -bonus.get_height(),
        bonus.get_width(),
        bonus.get_height()
    )
    step = [0, random.randint(4, 8)]

    return [bonus, position, step]

ENEMY_CREATION_INTERVAL = 1500 # ms
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, ENEMY_CREATION_INTERVAL)

BONUS_CREATION_INTERVAL = 3000 # ms
CREATE_BONUS = CREATE_ENEMY + 1
pygame.time.set_timer(CREATE_BONUS, BONUS_CREATION_INTERVAL)

CHANGE_PLAYER_IMAGE = CREATE_BONUS + 1
pygame.time.set_timer(CHANGE_PLAYER_IMAGE, 200)

STEP_DOWN = [0, 4]
STEP_UP = [0, -4]
STEP_RIGHT = [4, 0]
STEP_LEFT = [-4, 0]

enemies = []
bonuses = []
score = 0
FPS = 500
in_progress = True

while in_progress:
    pygame.time.Clock().tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            in_progress = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_PLAYER_IMAGE:
            player_image_index += 1

            if player_image_index == len(PLAYER_IMAGES):
                player_image_index = 0

            player = pygame.image.load(os.path.join(PLAYER_IMAGE_PATH, PLAYER_IMAGES[player_image_index])).convert_alpha()
    
    bg_X1 -= BACKGROUND_STEP
    bg_X2 -= BACKGROUND_STEP

    if bg_X1 < -BACKGROUND.get_width():
        bg_X1 = BACKGROUND.get_width()

    if bg_X2 < -BACKGROUND.get_width():
        bg_X2 = BACKGROUND.get_width()

    main_display.blit(BACKGROUND, (bg_X1, 0))
    main_display.blit(BACKGROUND, (bg_X2, 0))

    keys = pygame.key.get_pressed()
    player_step = [0, 0]

    if keys[K_DOWN] and position.bottom != HEIGHT:
        player_step = STEP_DOWN

    if keys[K_UP] and position.top != 0:
        player_step = STEP_UP

    if keys[K_RIGHT] and position.right != WIDTH:
        player_step = STEP_RIGHT

    if keys[K_LEFT] and position.left != 0:
        player_step = STEP_LEFT

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if position.colliderect(enemy[1]):
            print("Game over")
            in_progress = False

        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if position.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player, position)
    position = position.move(player_step)

    pygame.display.flip()
