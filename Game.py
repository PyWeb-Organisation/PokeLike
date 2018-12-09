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
window_size = (21*32, 21*32)
window_title = "PyWeb | PokéLike - "
tile_size = 32

# Création des couleurs :
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GOLD = (175, 175, 0)

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

def set_text(surface, text, font, color, shadow=(0, 0, 0, 0), **kwargs):
    shadow_pos = {}
    for key in kwargs:
        shadow_pos[key] = (kwargs[key][0]+1, kwargs[key][1]+1)
    surf = font.render(text, True, color)
    shadow = font.render(text, True, shadow)
    surf_rect = surf.get_rect(**kwargs)
    shadow_rect = shadow.get_rect(**shadow_pos)
    surface.blit(shadow, shadow_rect)
    surface.blit(surf, surf_rect)

# Création des scènes du jeu :
class TitleScreen:
    """
    Scène d'écran titre du jeu
    """
    def __init__(self):
        self.options = ["Nouvelle Partie", "Continuer", "Options", "Quitter"]
        self.cursor_pos = 0
        self.background = pygame.Surface(window_size, HWSURFACE)
        self.cursor = pygame.Surface((window_size[0]/4, 32), HWSURFACE | SRCALPHA)
        self.get_background()

    def get_background(self):
        self.cursor.fill(get_alpha(BLUE, 100))
        pygame.draw.rect(self.cursor, BLUE, (0, 0, window_size[0]/4, 32), 2)

        self.background.blit(BACKGROUND_TITLESCREEN, (0, 0))
        set_text(self.background, "PokéLike", poke_solid_font_big, YELLOW, WHITE, center=(window_size[0]/2, window_size[1]/4))

        self.background = self.background.convert(BACKGROUND)
        self.cursor = self.cursor.convert_alpha()

    def get_surface(self):
        surface = pygame.Surface(window_size, HWSURFACE)

        surface.blit(self.background, (0, 0))

        for i, option in enumerate(self.options):
            if i == self.cursor_pos:
                surface.blit(self.cursor, (3*window_size[0]/4-32, 3*window_size[1]/4 + i*32))
            set_text(surface, option, poke_solid_font_small, GOLD, BLACK, midright=(window_size[0]-48, 16 + 3*window_size[1]/4 + i*32))

        return surface.convert()

    def cursor_up(self):
        self.cursor_pos -= 1
        self.cursor_pos %= len(self.options)

    def cursor_down(self):
        self.cursor_pos += 1
        self.cursor_pos %= len(self.options)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.cursor_up()

                    elif event.key == K_DOWN:
                        self.cursor_down()

                    elif event.key in [K_RETURN, K_a]:
                        running = False

                    else:
                        pass

                else:
                    pass

            DISPLAY.blit(self.get_surface(), (0, 0))
            pygame.display.flip()

        return self.options[self.cursor_pos]

class LoadingScene:
    pass

class Field:
    pass

class Battle:
    pass

# Création des Instances du jeu :
class Save:
    pass

class Options:
    pass

class TileSet:
    """
    TileSet used for building maps
    """
    def __init__(self, name):
        self.name = name
        self.cut_tiles()

    def cut_tiles(self):
        tiles_file = "Assets\\tileset\\{}.png".format(name)
        hitbox_file = "Assets\\tileset\\{}.hitbox".format(name)
        tiles = pygame.image.load(tiles_file).convert_alpha()
        hitbox = []
        self.tiles = []
        with open(hitbox_file, "r") as file:
            for line in file:
                if not line == "":
                    hitbox.append(int(line))
            file.close()

        sizes = [x//32 for x in tiles.get_size()]
        for j in range(size[1]):
            for i in range(size[0]):
                surf = pygame.surface((tile_size, tiles_size), HWSURFACE | SRCALPHA)
                surf.blit(tiles, (-i*32, -j*32))
                self.tiles.append({"surface": surf.convert_alpha(), "hitbox": hitbox[32*j + i]})


class Map:
    """
    Map System
    """
    def __init__(self, file):
        self.file = file
        self.entities = []
        self.decode_file()
        self.build_surface()

    def decode_file(self):
        self.tilesets = []
        self.size = []
        self.layouts = {}
        layout1 = False
        layout2 = False
        layout3 = False
        current_layout = []

        with open(self.file, 'r') as file:
            for line in file:
                line = line[:-1]
                if not line == "" and not layout1 and not layout2 and not layout3:
                    if line == "[Layout1]":
                        layout1 = True
                        current_layout = []

                    elif line == "[Layout2]":
                        layout2 = True

                    elif line == "[Layout3]":
                        layout3 = True

                    else:
                        variable, content = line.split(":")
                        if variable[:-1] == "size":
                            self.size = [int(value) for value in line[1:].split(", ")]

                        elif variable[:-1] == "tileset":
                            self.tilesets.append(TileSet(content[1:]))

                        else:
                            pass

                elif layout1:
                    if line == "[\Layout1]":
                        layout1 = False
                        self.layouts["ground"] = current_layout
                        current_layout = []

                    else:
                        current_layout.append([int(value) for value in line.split(" ")])

                elif layout2:
                    if line == "[\Layout2]":
                        layout2 = False
                        self.layouts["objects"] = current_layout
                        current_layout = []

                    else:
                        current_layout.append([int(value) for value in line.split(" ")])

                elif layout3:
                    if line == "[\Layout3]":
                        layout3 = False
                        self.layouts["air"] = current_layout
                        current_layout = []

                    else:
                        current_layout.append([int(value) for value in line.split(" ")])

                else:
                    pass

            file.close()

        self.tileset = []
        for tileset in tilesets:
            self.tileset += tileset.tiles

    def build_surface(self):
        self.layout1 = pygame.Surface((32*self.size[0], 32*self.size[1]), HWSURFACE, SRCALPHA)
        self.layout2 = pygame.Surface((32*self.size[0], 32*self.size[1]), HWSURFACE, SRCALPHA)
        self.layout3 = pygame.Surface((32*self.size[0], 32*self.size[1]), HWSURFACE, SRCALPHA)
        self.map_hitbox = [[0 for x in range(self.size[0])] for x in range(self.size[1])]
        for i, tile in enumerate(self.layouts["ground"]):
            x = i%self.size[1]
            y = i//self.size[1]
            self.map_hitbox[y][x] = max(self.tileset[tile]["hitbox"], self.map_hitbox[y][x])
            self.layout1.blit(self.tilset[tile]["surface"], (x*32, y*32))

        for i, tile in enumerate(self.layouts["objects"]):
            x = i%self.size[1]
            y = i//self.size[1]
            self.map_hitbox[y][x] = max(self.tileset[tile]["hitbox"], self.map_hitbox[y][x])
            self.layout2.blit(self.tilset[tile]["surface"], (x*32, y*32))

        for i, tile in enumerate(self.layouts["air"]):
            x = i%self.size[1]
            y = i//self.size[1]
            self.map_hitbox[y][x] = max(self.tileset[tile]["hitbox"], self.map_hitbox[y][x])
            self.layout3.blit(self.tilset[tile]["surface"], (x*32, y*32))

class Player:
    pass

class Entity:
    pass

class NPC(Entity):
    pass

class Door(Entity):
    pass

class Tp(Entity):
    pass

class Chest(Entity):
    pass

class Pokemon(Entity):
    pass

class Dresseur(NPC):
    pass

# Chargement des composants du jeu

# Chargement des scènes du jeu :
titlescreen = TitleScreen()
savechoose = SaveChoose()
loadingscene = LoadingScene()
field = Field()
battle = Battle()

# Lancement du jeu :
print(titlescreen.run())
