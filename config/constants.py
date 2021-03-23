import os
import pygame
"""Give the absolute path of the directory"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# pygame config
FPS = 20

TITLE_WINDOW = "Sokoban"

SIDE_WINDOW = 550
PRINTER_SURFACE_HEIGHT = 45

COMPUTER_EVENT = pygame.USEREVENT + 1