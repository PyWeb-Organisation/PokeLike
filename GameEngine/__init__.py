from . import logger
from . import constants
from . import entitySystem
from . import mapSystem
from . import playerSystem
from . import sceneSystem
from pygame.locals import *
import pygame

pygame.init()

TILESETS = mapSystem.load_tilesets("GameData/Tilesets.data")
MAPS = mapSystem.load_maps("GameData/maps.data")
PLAYER = playerSystem.Player()
