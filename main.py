import pygame

from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()

HEIGHT = 800
WIDTH = 1200
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_SIZE = (20, 20)

player = pygame.Surface(PLAYER_SIZE)
player.fill(COLOR_WHITE)

position = player.get_rect()

STEP_DOWN = [0, 1]
STEP_UP = [0, -1]
STEP_RIGHT = [1, 0]
STEP_LEFT = [-1, 0]

FPS = 2000
in_progress = True

while in_progress:
    pygame.time.Clock().tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            in_progress = False
    
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

    main_display.blit(player, position)

    position = position.move(player_step)

    pygame.display.flip()
