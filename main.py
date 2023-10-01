import random
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

player = pygame.image.load('./images/player.png').convert_alpha()

position = player.get_rect()

ENEMY_SIZE = (30, 30)
ENEMY_CREATION_INTERVAL = 750 # ms
ENEMY_COLORS = [COLOR_BLUE, COLOR_GREEN, COLOR_RED]

def create_enemy():
    enemy = pygame.Surface(ENEMY_SIZE)
    enemy.fill(random.choice(ENEMY_COLORS))
    position = pygame.Rect(WIDTH, random.randint(0, HEIGHT - 30), *ENEMY_SIZE)
    step = [random.randint(-8, -4), 0]

    return [enemy, position, step]

BONUS_SIZE = (15, 15)
BONUS_CREATION_INTERVAL = 1500 # ms
BONUS_COLORS = [COLOR_CRIMSON, COLOR_YELLOW]

def create_bonus():
    bonus = pygame.Surface(BONUS_SIZE)
    bonus.fill(random.choice(BONUS_COLORS))
    position = pygame.Rect(random.randint(0, WIDTH - 15), 0, *BONUS_SIZE)
    step = [0, random.randint(4, 8)]

    return [bonus, position, step]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, ENEMY_CREATION_INTERVAL)

CREATE_BONUS = CREATE_ENEMY + 1
pygame.time.set_timer(CREATE_BONUS, BONUS_CREATION_INTERVAL)

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
            print("Boom")
            in_progress = False

        if enemy[1].left < 0:
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
