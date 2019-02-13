#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Importation du GameEngine :
from GameEngine import *
logger.log("Importation du GameEngine réussie avec succès")

# Création de la fenêtre du jeu
DISPLAY = pygame.display.set_mode((constants.DISPLAY_SIZE[0]*constants.TILE_SIZE, constants.DISPLAY_SIZE[1]*constants.TILE_SIZE), HWSURFACE | DOUBLEBUF)

# Lancement du programme
chosen_option = sceneSystem.SCENES["TitleScreen"].run(DISPLAY)

if chosen_option == "Nouvelle Partie":
    pass

elif chosen_option == "continuer":
    pass

elif chosen_option == "Options":
    pass

else:
    pygame.quit()
