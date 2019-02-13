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

    def run(self, display):
        logger.log("Start {}".format(self.name), level="Info")
        continuer = True
        while continuer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    continuer = False
            display.fill(constants.Color.white)
            display.blit(self.render(), (0, 0))
            pygame.display.flip()

        logger.log("Quit {}".format(self.name), level="Info")

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

        title_pos = ((constants.DISPLAY_SIZE[0] * constants.TILE_SIZE) // 2, (constants.DISPLAY_SIZE[1] * constants.TILE_SIZE) // 4)

        title = constants.FONT_BIG.render(constants.GAME_TITLE, True, constants.Color.yellow)
        title_rect = title.get_rect(center=title_pos)

        surface.blit(title, title_rect)

        surf_bis = pygame.Surface((constants.DISPLAY_SIZE[0]*constants.TILE_SIZE, len(self.options)*constants.TILE_SIZE), HWSURFACE | SRCALPHA)

        for i, option in enumerate(self.options):
            if i == self.cursor_pos:
                text = constants.FONT_REGULAR.render(option, True, constants.Color.green)
            else:
                text = constants.FONT_REGULAR.render(option, True, constants.Color.black)
            text_pos = (constants.DISPLAY_SIZE[0]*constants.TILE_SIZE // 2, constants.TILE_SIZE // 2 + i*constants.TILE_SIZE)
            text_rect = text.get_rect(center=text_pos)
            surf_bis.blit(text, text_rect)

        options_pos = ((constants.DISPLAY_SIZE[0] * constants.TILE_SIZE) // 2, 2*(constants.DISPLAY_SIZE[1] * constants.TILE_SIZE) // 3)
        surf_bis_rect = surf_bis.get_rect(center=options_pos)

        surface.blit(surf_bis, surf_bis_rect)

        return surface.convert_alpha()

class Options_Screen (Scene):
    """
    """
    def __init__(self):
        super().__init__("Options_Screen", (constants.DISPLAY_SIZE[0]*constants.TILE_SIZE, constants.DISPLAY_SIZE[1]*constants.TILE_SIZE))
        self.cursor_pos = 0
        self.options = ["option 1","option 2","option 3","option 4","option 5","option 6"]
        logger.log("le joueur a ouvert les options")

    def move_cursor(self,direction):
        self.cursor_pos = (self.cursor_pos+ direction)%len(self.options)



    def render(self):
        surface = Scene.render(self)

        surf_bis = pygame.Surface((constants.DISPLAY_SIZE[0]*constants.TILE_SIZE, len(self.options)*constants.TILE_SIZE), HWSURFACE | SRCALPHA)

        for i,option in enumerate(self.options):
            if i == self.cursor_pos:
                text = constants.FONT_REGULAR.render(option, True, constants.Color.green)
            else:
                text = constants.FONT_REGULAR.render(option, True, constants.Color.black)
            text_pos = (constants.DISPLAY_SIZE[0]*constants.TILE_SIZE-constants.TILE_SIZE, constants.TILE_SIZE // 2 + i*constants.TILE_SIZE)
            text_rect = text.get_rect(midright=text_pos)
            surf_bis.blit(text, text_rect)

        options_pos = ((constants.DISPLAY_SIZE[0] * constants.TILE_SIZE) // 2, (constants.DISPLAY_SIZE[1] * constants.TILE_SIZE) // 2)
        surf_bis_rect = surf_bis.get_rect(center=options_pos)

        surface.blit(surf_bis, surf_bis_rect)
        return surface.convert_alpha()
    
