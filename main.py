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

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_SIZE = (20, 20)

player = pygame.Surface(PLAYER_SIZE)
player.fill(COLOR_WHITE)

position = player.get_rect()

ENEMY_SIZE = (30, 30)
ENEMY_CREATION_INTERVAL = 1500 # ms
ENEMY_COLORS = [COLOR_BLUE, COLOR_CRIMSON, COLOR_GREEN, COLOR_YELLOW, COLOR_RED]

def create_enemy():
    enemy = pygame.Surface(ENEMY_SIZE)
    enemy.fill(random.choice(ENEMY_COLORS))
    position = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *ENEMY_SIZE)

    return [enemy, position]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, ENEMY_CREATION_INTERVAL)

STEP_DOWN = [0, 1]
STEP_UP = [0, -1]
STEP_RIGHT = [1, 0]
STEP_LEFT = [-1, 0]

enemies = []
FPS = 2000
in_progress = True

while in_progress:
    pygame.time.Clock().tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            in_progress = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
    
    main_display.fill(COLOR_BLACK)

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
        enemy[1] = enemy[1].move(STEP_LEFT)
        main_display.blit(enemy[0], enemy[1])

    main_display.blit(player, position)
    position = position.move(player_step)

    pygame.display.flip()
