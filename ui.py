# ui.py
import pygame
from constants import BUTTON_COLOR, BUTTON_HOVER_COLOR, TILE_SIZE

def play_screen():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Stratego")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
