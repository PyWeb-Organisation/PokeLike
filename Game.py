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
window_size = (41*16, 41*16)
window_title = "PyWeb | PokéLike - "
tile_size = 16

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
        tiles_file = "Assets\\tilesets\\{}.png".format(self.name)
        hitbox_file = "Assets\\tilesets\\{}.hitbox".format(self.name)
        tiles = pygame.image.load(tiles_file).convert_alpha()
        hitbox = []
        self.tiles = []
        with open(hitbox_file, "r") as file:
            for line in file:
                if not line == "":
                    hitbox += [int(value) for value in line[:-1].split(" ")]
            file.close()

        size = [x//tile_size for x in tiles.get_size()]
        for j in range(size[1]):
            for i in range(size[0]):
                surf = pygame.Surface((tile_size, tile_size), HWSURFACE | SRCALPHA)
                surf.blit(tiles, (-i*tile_size, -j*tile_size))
                self.tiles.append({"surface": surf.convert_alpha(), "hitbox": hitbox[size[0]*j + i]})

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

                    elif line == "[Layout2]":
                        layout2 = True

                    elif line == "[Layout3]":
                        layout3 = True

                    else:
                        variable, content = line.split(" : ")
                        if variable == "size":
                            self.size = [int(value) for value in content.split(", ")]

                        elif variable == "tileset":
                            self.tilesets.append(TileSet(content))

                        else:
                            pass

                elif layout1:
                    if line == "[/Layout1]":
                        layout1 = False
                        self.layouts["ground"] = current_layout
                        current_layout = []

                    elif not line == "[Layout1]":
                        current_layout += [int(value) for value in line.split(" ")]

                elif layout2:
                    if line == "[/Layout2]":
                        layout2 = False
                        self.layouts["objects"] = current_layout
                        current_layout = []

                    elif not line == "[Layout2]":
                        current_layout += [int(value) for value in line.split(" ")]

                elif layout3:
                    if line == "[/Layout3]":
                        layout3 = False
                        self.layouts["air"] = current_layout
                        current_layout = []

                    elif not line == "[Layout3]":
                        current_layout += [int(value) for value in line.split(" ")]

                else:
                    pass

            file.close()

        self.tileset = []
        for tileset in self.tilesets:
            self.tileset += tileset.tiles

    def build_surface(self):
        self.layout1 = pygame.Surface((tile_size*self.size[0], tile_size*self.size[1]), HWSURFACE | SRCALPHA)
        self.layout2 = pygame.Surface((tile_size*self.size[0], tile_size*self.size[1]), HWSURFACE | SRCALPHA)
        self.layout3 = pygame.Surface((tile_size*self.size[0], tile_size*self.size[1]), HWSURFACE | SRCALPHA)
        self.map_hitbox = [[0 for x in range(self.size[0])] for x in range(self.size[1])]
        for i, tile in enumerate(self.layouts["ground"]):
            x = i%self.size[1]
            y = i//self.size[1]
            self.map_hitbox[y][x] = max(self.tileset[tile]["hitbox"], self.map_hitbox[y][x])
            self.layout1.blit(self.tileset[tile]["surface"], (x*tile_size, y*tile_size))

        for i, tile in enumerate(self.layouts["objects"]):
            x = i%self.size[1]
            y = i//self.size[1]
            self.map_hitbox[y][x] = max(self.tileset[tile]["hitbox"], self.map_hitbox[y][x])
            self.layout2.blit(self.tileset[tile]["surface"], (x*tile_size, y*tile_size))

        for i, tile in enumerate(self.layouts["air"]):
            x = i%self.size[1]
            y = i//self.size[1]
            self.map_hitbox[y][x] = max(self.tileset[tile]["hitbox"], self.map_hitbox[y][x])
            self.layout3.blit(self.tileset[tile]["surface"], (x*tile_size, y*tile_size))

        self.layout1 = self.layout1.convert_alpha()
        self.layout2 = self.layout2.convert_alpha()
        self.layout3 = self.layout3.convert_alpha()

class Player:
    """personnage du jeu"""
    def __init__(self):#initialisation la totalité des variables du personnage
            self.name = "" #Initialisation du nom
            self.skin = ""#Initialisation de l'apparence
            self.x = 0#Coordonnées x du personnage
            self.y = 0#Coordonnée y du personnage

    def go_up(self):#Aller en haut
        self.y += 1

    def go_down(self):#Aller en bas
        self.y -= 1

    def go_right(self):#Aller à droite
        self.x += 1

    def go_left(self):#Aller à gauche
        self.x -= 1

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
    """Pokémons"""
    def __init__(self):#Initialisation de la totalité des variables des pokémons
        self.name = ""#Initialisation du nom
        self.skin = ""#Initialisation de l'apparence


class Dresseur(NPC):
    pass

# Chargement des composants du jeu
main_tileset = TileSet("main_tile_set")

map001 = Map("Assets\\maps\\map001.map")

# Chargement des scènes du jeu :
titlescreen = TitleScreen()
loadingscene = LoadingScene()
field = Field()
battle = Battle()

# Lancement du jeu :
print(titlescreen.run())
DISPLAY.fill(BLACK)
DISPLAY.blit(map001.layout1, (0, 0))
DISPLAY.blit(map001.layout2, (0, 0))
DISPLAY.blit(map001.layout3, (0, 0))
pygame.display.flip()
input()
