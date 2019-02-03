from . import constants
from . import entitySystem
from . import mapSystem
from . import playerSystem
from pygame.locals import *
import pygame

TILESETS = mapSystem.load_tilesets("GameData/Tilesets.data")
MAPS = mapSystem.load_maps("GameData/maps.data")
