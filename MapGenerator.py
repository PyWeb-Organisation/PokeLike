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

pygame.display.init()
display = pygame.display.set_mode((1000, 700))

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
    global sizes
    sizes = []
    f = tkinter.Tk()
    size1 = tkinter.StringVar()
    size2 = tkinter.StringVar()
    entry1 = tkinter.Entry(f, textvariable=size1)
    entry2 = tkinter.Entry(f, textvariable=size2)
    def get_size():
        global sizes
        sizes = [int(entry1.get()), int(entry2.get())]
        f.destroy()
    button = tkinter.Button(f, text="Valider", command=get_size)
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

    def get_surfaces(self):
         layout1 = pygame.Surface((tile_size*self.size[0], tile_size*self.size[1]), HWSURFACE | SRCALPHA)
         layout2 = pygame.Surface((tile_size*self.size[0], tile_size*self.size[1]), HWSURFACE | SRCALPHA)
         layout3 = pygame.Surface((tile_size*self.size[0], tile_size*self.size[1]), HWSURFACE | SRCALPHA)
         self.map_hitbox = [[0 for x in range(self.size[0])] for x in range(self.size[1])]
         for y, line in enumerate(self.layouts[0]):
             for x, tile in enumerate(line):
                 self.map_hitbox[y][x] = max(self.tileset[tile]["hitbox"], self.map_hitbox[y][x])
                 layout1.blit(self.tileset[tile]["surface"], (x*tile_size, y*tile_size))

         for y, line in enumerate(self.layouts[1]):
             for x, tile in enumerate(line):
                 self.map_hitbox[y][x] = max(self.tileset[tile]["hitbox"], self.map_hitbox[y][x])
                 layout2.blit(self.tileset[tile]["surface"], (x*tile_size, y*tile_size))

         for y, line in enumerate(self.layouts[2]):
             for x, tile in enumerate(line):
                 self.map_hitbox[y][x] = max(self.tileset[tile]["hitbox"], self.map_hitbox[y][x])
                 layout3.blit(self.tileset[tile]["surface"], (x*tile_size, y*tile_size))

         return layout1.convert_alpha(), layout2.convert_alpha(), layout3.convert_alpha()

class App:
    """
    Prcesseur logique de l'application
    """
    def __init__(self):
        self.current_map = Map([0, 0], [])
        self.see_layout = 1

    def add_tileset_to_map(self):
        path = fd.askopenfilename()
        filename = os.path.splitext(os.path.basename(path))[0]
        tileset = TileSet(filename)
        self.current_map.add_tileset(tileset)

    def create_map(self):
        self.current_map = create_new_map()

    def open_map(self):
        path = fd.askopenfilename()
        tilesets = []
        size = []
        layouts = [[], [], []]
        layout1 = False
        layout2 = False
        layout3 = False
        current_layout = []

        with open(path, 'r') as file:
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
                            size = [int(value) for value in content.split(", ")]

                        elif variable == "tileset":
                            tilesets.append(TileSet(content))

                        else:
                            pass

                elif layout1:
                    if line == "[/Layout1]":
                        layout1 = False
                        layouts[0] = current_layout
                        current_layout = []

                    elif not line == "[Layout1]":
                        current_layout.append([int(value) for value in line.split(" ")])

                elif layout2:
                    if line == "[/Layout2]":
                        layout2 = False
                        layouts[1] = current_layout
                        current_layout = []

                    elif not line == "[Layout2]":
                        current_layout.append([int(value) for value in line.split(" ")])

                elif layout3:
                    if line == "[/Layout3]":
                        layout3 = False
                        layouts[2] = current_layout
                        current_layout = []

                    elif not line == "[Layout3]":
                        current_layout.append([int(value) for value in line.split(" ")])

                else:
                    pass

            file.close()

        self.current_map = Map(size, tilesets)
        self.current_map.layouts = layouts

    def run(self):
        running = True
        surface_bar = pygame.Surface((1000, 100), HWSURFACE | SRCALPHA)
        surface_map = pygame.Surface((600, 600), HWSURFACE | SRCALPHA)
        surface_tileset = pygame.Surface((400, 600), HWSURFACE | SRCALPHA)
        camera_map = [0, 0]
        camera_tileset = [0, 0]

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                elif event.type == MOUSEBUTTONDOWN:
                    pass

            layouts = self.current_map.get_surfaces()
            surface_map.blit(layouts[0], camera_map)
            if self.see_layout == 2:
                surface = pygame.Surface((self.current_map.size[0]*16, self.current_map.size[1]*16), HWSURFACE | SRCALPHA)
                surface.fill((0, 0, 0, 100))
                surface_map.blit(surface, camera_map)
                surface_map.blit(layouts[1], camera_map)

            if self.see_layout == 3:
                surface_map.blit(layouts[1], camera_map)
                surface = pygame.Surface((self.current_map.size[0]*16, self.current_map.size[1]*16), HWSURFACE | SRCALPHA)
                surface.fill((0, 0, 0, 100))
                surface_map.blit(surface, camera_map)
                surface_map.blit(layouts[2], camera_map)

            y = 0

            for name in self.current_map.tilesets_names:
                tiles_file = "Assets\\tilesets\\{}.png".format(name)
                tiles = pygame.image.load(tiles_file).convert_alpha()
                surface_tileset.blit(tiles, (0, y))
                y += tiles.get_size()[1]

            display.blit(surface_bar, (0, 0))
            display.blit(surface_map, (0, 100))
            display.blit(surface_tileset, (600, 100))
            pygame.display.flip()

app = App()
app.open_map()
app.run()
