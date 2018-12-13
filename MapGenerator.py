#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Informations sur le code :
__name__ = "MapGenerator"
__version__ = "1"
__authors__ = "Lightpearl26"
__description__ = "Créateur de map pour le jeu [PokéLike]"

# Importation des modules complémentaires nécéssaires :
from pygame.locals import *
import tkinter.filedialog as fd
import pygame
import tkinter
import os
import sys

# Création des variables globales du script :
tile_size = 16

# Création des fonctions du script :
def save_map(size, tilesets, layouts, filename):
    with open(filename, "w") as file:
        file.write("size : {}\n".format(size.join(", ")))

        for tileset in tilesets:
            file.write("tileset : {}\n".format(tileset))

        file.write("[Layout1]")
        for line in layouts[0]:
            file.write("{}\n".format(line.join(" ")))
        file.write("[/Layout1]")

        file.write("[Layout2]")
        for line in layouts[1]:
            file.write("{}\n".format(line.join(" ")))
        file.write("[/Layout2]")

        file.write("[Layout3]")
        for line in layouts[2]:
            file.write("{}\n".format(line.join(" ")))
        file.write("[/Layout3]")
        file.close()

def create_new_map():
    global sizes, entry1, entry2
    f = tkinter.Tk()
    size1 = tkinter.StringVar()
    size2 = tkinter.StringVar()
    entry1 = tkinter.Entry(f, textvariable=size1)
    entry2 = tkinter.Entry(f, textvariable=size2)
    sizes = []
    def get_entries():
        global sizes
        print(sizes)
        sizes = [int(entry1.get()), int(entry2.get())]
        f.destroy()
    button = tkinter.Button(f, text="Valider", command=get_entries)
    entry1.grid(row=0, column=0)
    entry2.grid(row=1, column=0)
    button.grid(row=1, column=1)
    f.mainloop()
    return Map(sizes, [])


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
    Map prévu pour le jeu [PokéLike]
    """
    def __init__(self, size, tilesets):
        self.size = size
        self.tilesets_names = []
        self.tileset = []
        for tileset in tilesets:
            self.tilesets_names.append(tileset.name)
            self.tileset += tileset.tiles
        self.layouts = [[[0 for _ in range(size[0])] for _ in range(size[1])] for _ in range(3)]

    def add_tileset(self, tileset):
        self.tilesets_names.append(tileset.name)
        self.tileset += tileset.tiles

class App:
    """
    Prcesseur logique de l'application
    """
    def __init__(self):
        self.current_map = Map([0, 0], [])

print(create_new_map())
input()
