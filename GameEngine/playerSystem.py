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
