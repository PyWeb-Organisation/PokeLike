#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Importation du GameEngine :
from GameEngine import *
logger.log("Importation du GameEngine réussie avec succès")

DISPLAY = pygame.display.set_mode((constants.DISPLAY_SIZE[0]*constants.TILE_SIZE, constants.DISPLAY_SIZE[1]*constants.TILE_SIZE), HWSURFACE | DOUBLEBUF)

sceneSystem.SCENES["Options_Screen"].run(DISPLAY)
