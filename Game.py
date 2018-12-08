#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Informations sur le fichier :
__name__ = "PokéLike"
__version__ = "1"
__authors__ = "Lightpearl26 | Flashership"
__organisation__ = "PyWeb"

# Importation des modules complémentaires nécéssaires :
from pygame.locals import *
import pygame
import time
import sys
import os

pygame.init()

# Création des contantes du jeu :
window_size = (27*32, 21*32)
window_title = "PyWeb | PokéLike - "

# Création des couleurs :
WHITE = (255, 255, 255)
BLACK = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Création de la fenêtre du jeu :
DISPLAY = pygame.display.set_mode(window_size, HWSURFACE | DOUBLEBUF)
pygame.display.set_caption(window_title)

# Chargement des images du jeu :
BACKGROUND = pygame.Surface(window_size, HWSURFACE)
BACKGROUND_TITLESCREEN = pygame.image.load("Assets\\pictures\\backgrounds\\titlescreen.jpg").convert(BACKGROUND)

# Chargement des polices du jeu :
poke_hollow_font_big = pygame.font.Font("Assets\\fonts\\Pokemon Hollow.ttf", 64)
poke_solid_font_big = pygame.font.Font("Assets\\fonts\\Pokemon Solid.ttf", 64)
poke_hollow_font_medium = pygame.font.Font("Assets\\fonts\\Pokemon Hollow.ttf", 32)
poke_solid_font_medium = pygame.font.Font("Assets\\fonts\\Pokemon Solid.ttf", 32)
poke_hollow_font_small = pygame.font.Font("Assets\\fonts\\Pokemon Hollow.ttf", 16)
poke_solid_font_small = pygame.font.Font("Assets\\fonts\\Pokemon Solid.ttf", 16)

# Création des fonctions du jeu :
def get_alpha(color, alpha):
    return color[0], color[1], color[2], alpha

# Création des scènes du jeu :
class TitleScreen:
    """
    Scène d'écran titre du jeu
    """
    def __init__(self):
        self.options = ["Nouvelle Partie", "Continuer", "Options", "Quitter"]
        self.cursor_pos = 0

    def get_surface(self):
        surface = pygame.Surface(window_size, HWSURFACE)

        cursor = pygame.Surface((window_size[0]/2, 64), HWSURFACE | SRCALPHA)
        cursor.fill(get_alpha(WHITE, 100))
        pygame.draw.rect(cursor, WHITE, (0, 0, window_size[0]/2, 64), 2)

        surface.blit(BACKGROUND_TITLESCREEN, (0, 0))
        text = poke_solid_font_big.render("PokéLike", True, YELLOW)
        text_rect = text.get_rect(center=(window_size[0]/2, window_size[1]/4))
        surface.blit(text, text_rect)

        for i, option in enumerate(self.options):
            if i == self.cursor_pos:
                surface.blit(cursor, (window_size[0]/4, window_size[1]/2 + i*64))
            text = poke_solid_font_medium.render(option, True, YELLOW)
            text_rect = text.get_rect(center=(window_size[0]/2, 32 + window_size[1]/2 + i*64))
            surface.blit(text, text_rect)

        return surface.convert()

# Chargement des scènes du jeu :
titlescreen = TitleScreen()

# Lancement du jeu :
DISPLAY .blit(titlescreen.get_surface(), (0, 0))
pygame.display.flip()
input()
