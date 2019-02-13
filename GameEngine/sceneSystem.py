#-*-coding:utf-8-*-

"""
"""

# Information sur le fichier :
__name__ = "sceneSystem"
__version__ = "1"
__authors__ = "Lightpearl"

# Importation des modules complémentaires nécéssaires :
from . import logger
from . import constants
from pygame.locals import *
import pygame

# Création des variables globales du module
SCENES = {}

# Création des objets du module :
class Scene:
    """
    """
    def __init__(self, name, size):
        self.name = name
        self.size = size
        SCENES[name] = self

    def render(self):
        surface = pygame.Surface(self.size, HWSURFACE | SRCALPHA)
        return surface.convert_alpha()

class TitleScreen(Scene):
    """
    """
    def __init__(self):
        super().__init__("TitleScreen", (constants.DISPLAY_SIZE[0]*constants.TILE_SIZE, constants.DISPLAY_SIZE[1]*constants.TILE_SIZE))
        self.cursor_pos = 0
        self.options = ["Nouvelle Partie", "Continuer", "Options", "Quitter"]
        self.render()
        logger.log("Rendu du TitleScreen éffectué")

    def move_cursor(self, direction):
        self.cursor_pos = (self.cursor_pos + direction) % len(self.options)

    def render(self):
        surface = Scene.render(self)

        title_pos = constants.DISPLAY_SIZE[0] * constants.TILE_SIZE // 2, constants.DISPLAY_SIZE[1] * constants.TILE_SIZE // 4

        title = constants.FONT_BIG.render(constants.GAME_TITLE, True, constants.Color.yellow)

        return surface.convert_alpha()
