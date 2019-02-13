#-*-coding:utf-8-*-

# Importation des modules complémentaires nécéssaires :
from . import logger
from pygame.locals import *
import pygame

pygame.font.init()

# Création des variables du module :
GAME_TITLE = "Pokélike"

DISPLAY_SIZE = (17, 13)
ENTITY_FREQUECY = 2000 # ms
ENTITY_PIXEL_SPEED = 2
ENTITY_SPEED =  0.01 # s
CURRENT_MAP = 0
TILE_SIZE = 48

FONT_SMALL = pygame.font.Font("GameData\\Fonts\\Pokemon Solid.ttf", 16)
FONT_REGULAR = pygame.font.Font("GameData\\Fonts\\Pokemon Solid.ttf", 32)
FONT_BIG = pygame.font.Font("GameData\\Fonts\\Pokemon Solid.ttf", 48)

# Création des objets du module :
class Color:
    green = (0, 100, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    lime = (0, 255, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    cyan = (0, 255, 255)
    magenta = (255, 0, 255)
    yellow = (255, 255, 0)
    orange = (255, 155, 0)
    violet = (155, 0, 100)
    vermillon = (175, 10, 45)

logger.log("Création des constantes du module éffectué")
