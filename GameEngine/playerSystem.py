#-*-coding:utf-8-*-
""""""

# Information sur le fichier :
__name__ = "mapSystem"
__version__ = "1"
__authors__ = "Lightpearl"

# Importation des modules complémentaires nécéssaires :
from . import entitySystem
from pygame.locals import *
import pygame
from . import workerSystem
from . import constants

#Création de l'objet joueur#
class Player(entitySystem.Entity):
    """
    Player of the game
    """
    def __init__(self):
        entitySystem.Entity.__init__(self,48, pygame.image.load('GameData\\pictures\\Character\\Actor1.png').convert_alpha(),'Player', 1,'action',[],(0,0),0)

    def get_camera(self):
        from . import MAPS, TILESETS
        map_real_pos = (self.save_pos[0]*TILESETS[MAPS[constants.CURRENT_MAP].tileset_id].size+self.real_pos*entitySystem.DIRECTIONS[self.facing][0], (self.save_pos[1]*TILESETS[MAPS[constants.CURRENT_MAP].tileset_id].size+self.real_pos*entitySystem.DIRECTIONS[self.facing][1]))
        ideal_pos = (constants.DISPLAY_SIZE[0]//2*TILESETS[MAPS[constants.CURRENT_MAP].tileset_id].size, constants.DISPLAY_SIZE[1]//2*TILESETS[MAPS[constants.CURRENT_MAP].tileset_id].size)
        camera_x = min(0, max(ideal_pos[0]-map_real_pos[0], -(MAPS[constants.CURRENT_MAP].size[0]-constants.DISPLAY_SIZE[0])*TILESETS[MAPS[constants.CURRENT_MAP].tileset_id].size))
        camera_y = min(0, max(ideal_pos[1]-map_real_pos[1], -(MAPS[constants.CURRENT_MAP].size[1]-constants.DISPLAY_SIZE[1])*TILESETS[MAPS[constants.CURRENT_MAP].tileset_id].size))
        return (camera_x, camera_y)
