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

    def move(self,direction):
        from . import MAPS, TILESETS
        self.facing=direction
        map=MAPS[constants.CURRENT_MAP]
        new_x= max(0,min(self.pos[0]+entitySystem.DIRECTIONS[direction][0],map.size[0]-1))
        new_y= max(0,min(self.pos[1]+entitySystem.DIRECTIONS[direction][1],map.size[1]-1))
        map_hitbox=map.map_hitbox[new_y*map.size[0]+new_x]
        entity_hitbox=map.get_entities_hitbox()[new_y*map.size[0]+new_x]
        if map_hitbox != 1 and entity_hitbox != 1 and not self.pos==(new_x,new_y) and self.real_pos==0:
            self.move_worker.put((direction, (new_x, new_y)))
            self.pos = (new_x, new_y)
