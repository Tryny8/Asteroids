import pygame
import sys

IS_WEB = sys.platform == "emscripten"

if IS_WEB:
    KEY_LEFT  = pygame.K_a
    KEY_UP    = pygame.K_w
else:
    KEY_LEFT  = pygame.K_q
    KEY_UP    = pygame.K_z
    

KEY_RIGHT = pygame.K_d
KEY_DOWN  = pygame.K_s

KEY_SHOOT = pygame.K_SPACE