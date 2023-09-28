import pygame

from pygame.constants import QUIT

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
player_step = [1, 1]

FPS = 2000
in_progress = True

while in_progress:
    pygame.time.Clock().tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            in_progress = False
    
    main_display.fill(COLOR_BLACK)

    if position.bottom == HEIGHT or position.top == -1:
        player_step[1] = -player_step[1]

    if position.right == WIDTH or position.left == -1:
        player_step[0] = -player_step[0]

    main_display.blit(player, position)

    position = position.move(player_step)

    pygame.display.flip()
