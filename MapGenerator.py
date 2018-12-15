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
display = pygame.display.set_mode((1032, 716))

# Création des variables globales du script :
tile_size = 16
inutile = tkinter.Tk()
inutile.geometry("0x0")
inutile.overrideredirect(True)

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
        tilesets = []
        tileset_size_y = 0
        tileset_size_x = 0
        for name in self.current_map.tilesets_names:
            tiles_file = "Assets\\tilesets\\{}.png".format(name)
            tiles = pygame.image.load(tiles_file).convert_alpha()
            size = tiles.get_size()
            tileset_size_y += size[1]
            tileset_size_x = max(tileset_size_x, size[0])
            tilesets.append(tiles)
        sidebar_map_x = 0
        sidebar_map_y = 0
        sidebar_tileset_x = 0
        sidebar_tileset_y = 0
        sidebar_map_x_size = min(600, 600**2 / (16*self.current_map.size[0]))
        sidebar_tileset_x_size = min(400, 400**2 / tileset_size_x)
        sidebar_map_y_size = min(600, 600**2 / (16*self.current_map.size[1]))
        sidebar_tileset_y_size = min(600, 600**2 / tileset_size_y)
        ram_map_x = -1
        ram_map_y = -1
        ram_tileset_x = -1
        ram_tileset_y = -1
        ecart_map_x = 0
        ecart_map_y = 0
        ecart_tileset_x = 0
        ecart_tileset_y = 0

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if sidebar_map_x <= pos[0] <= sidebar_map_x+sidebar_map_x_size and 700 <= pos[1] <= 716:
                            ram_map_x = pos[0]

                        if 600 <= pos[0] <= 616 and 100+sidebar_map_y <= pos[1] <= 100+sidebar_map_y+sidebar_map_y_size:
                            ram_map_y = pos[1]

                        if 616+sidebar_tileset_x <= pos[0] <= 616+sidebar_tileset_x+sidebar_tileset_x_size and 700 <= pos[1] <= 716:
                            ram_tileset_x = pos[0]

                        if 1016 <= pos[0] <= 1032 and 100+sidebar_tileset_y <= pos[1] <= 100+sidebar_tileset_y+sidebar_tileset_y_size:
                            ram_tileset_y = pos[1]

                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if ram_map_x != -1:
                            ecart_map_x = pos[0]-ram_map_x
                            pos_max = 600 - sidebar_map_x_size
                            pos_min = 0
                            new_pos = sidebar_map_x + ecart_map_x
                            sidebar_map_x = min(max(pos_min, new_pos), pos_max)
                            ram_map_x = -1
                            ecart_map_x = 0

                        if ram_map_y != -1:
                            ecart_map_y = pos[1]-ram_map_y
                            pos_max = 600 - sidebar_map_y_size
                            pos_min = 0
                            new_pos = sidebar_map_y + ecart_map_y
                            sidebar_map_y = min(max(pos_min, new_pos), pos_max)
                            ram_map_y = -1
                            ecart_map_y = 0

                        if ram_tileset_x != -1:
                            ecart_tileset_x = pos[0]-ram_tileset_x
                            pos_max = 400 - sidebar_tileset_x_size
                            pos_min = 0
                            new_pos = sidebar_tileset_x + ecart_tileset_x
                            sidebar_tileset_x = min(max(pos_min, new_pos), pos_max)
                            ram_tileset_x = -1
                            ecart_tileset_x = 0

                        if ram_tileset_y != -1:
                            ecart_tileset_y = pos[1]-ram_tileset_y
                            pos_max = 600 - sidebar_tileset_y_size
                            pos_min = 0
                            new_pos = sidebar_tileset_y + ecart_tileset_y
                            sidebar_tileset_y = min(max(pos_min, new_pos), pos_max)
                            ram_tileset_y = -1
                            ecart_tileset_y = 0

            if ram_map_x != -1:
                pos = pygame.mouse.get_pos()
                ecart_map_x = pos[0]-ram_map_x
                if sidebar_map_x == 600-sidebar_map_x_size:
                    pos_max = 0
                    pos_min = sidebar_map_x_size - 600
                elif sidebar_map_x == 0:
                    pos_max = 600 - sidebar_map_x_size
                    pos_min = 0
                else:
                    pos_max = 600 - sidebar_map_x_size-sidebar_map_x
                    pos_min = -sidebar_map_x
                ecart_map_x = min(max(pos_min, ecart_map_x), pos_max)

            if ram_map_y != -1:
                pos = pygame.mouse.get_pos()
                ecart_map_y = pos[1]-ram_map_y
                if sidebar_map_y == 600-sidebar_map_y_size:
                    pos_max = 0
                    pos_min = sidebar_map_y_size - 600
                elif sidebar_map_x == 0:
                    pos_max = 600 - sidebar_map_y_size
                    pos_min = 0
                else:
                    pos_max = 600 - sidebar_map_y_size-sidebar_map_y
                    pos_min = -sidebar_map_y
                ecart_map_y = min(max(pos_min, ecart_map_y), pos_max)

            if ram_tileset_x != -1:
                pos = pygame.mouse.get_pos()
                ecart_tileset_x = pos[0]-ram_tileset_x
                if sidebar_tileset_x == 400-sidebar_tileset_x_size:
                    pos_max = 0
                    pos_min = sidebar_tileset_x_size - 400
                elif sidebar_tileset_x == 0:
                    pos_max = 400 - sidebar_tileset_x_size
                    pos_min = 0
                else:
                    pos_max = 400 - sidebar_tileset_x_size-sidebar_tileset_x
                    pos_min = -sidebar_tileset_x
                ecart_tileset_x = min(max(pos_min, ecart_tileset_x), pos_max)

            if ram_tileset_y != -1:
                pos = pygame.mouse.get_pos()
                ecart_tileset_y = pos[1]-ram_tileset_y
                if sidebar_tileset_y == 600-sidebar_tileset_y_size:
                    pos_max = 0
                    pos_min = sidebar_tileset_y_size - 600
                elif sidebar_tileset_y == 0:
                    pos_max = 600 - sidebar_tileset_y_size
                    pos_min = 0
                else:
                    pos_max = 600 - sidebar_tileset_y_size-sidebar_tileset_y
                    pos_min = -sidebar_tileset_y
                ecart_tileset_y = min(max(pos_min, ecart_tileset_y), pos_max)

            display.fill((255, 255, 255))

            layouts = self.current_map.get_surfaces()
            surface_map.fill((255, 255, 255))
            surface_map.blit(layouts[0], (-(sidebar_map_x+ecart_map_x)*(16*self.current_map.size[0]) / 600, -(sidebar_map_y+ecart_map_y)*(16*self.current_map.size[1]) / 600))
            if self.see_layout == 2:
                surface = pygame.Surface((self.current_map.size[0]*16, self.current_map.size[1]*16), HWSURFACE | SRCALPHA)
                surface.fill((0, 0, 0, 100))
                surface_map.blit(surface, (-(sidebar_map_x+ecart_map_x)*(16*self.current_map.size[0]) / 600, -(sidebar_map_y+ecart_map_y)*(16*self.current_map.size[1]) / 600))
                surface_map.blit(layouts[1], (-(sidebar_map_x+ecart_map_x)*(16*self.current_map.size[0]) / 600, -(sidebar_map_y+ecart_map_y)*(16*self.current_map.size[1]) / 600))

            if self.see_layout == 3:
                surface_map.blit(layouts[1], (-(sidebar_map_x+ecart_map_x)*(16*self.current_map.size[0]) / 600, -(sidebar_map_y+ecart_map_y)*(16*self.current_map.size[1]) / 600))
                surface = pygame.Surface((self.current_map.size[0]*16, self.current_map.size[1]*16), HWSURFACE | SRCALPHA)
                surface.fill((0, 0, 0, 100))
                surface_map.blit(surface, (-(sidebar_map_x+ecart_map_x)*(16*self.current_map.size[0]) / 600, -(sidebar_map_y+ecart_map_y)*(16*self.current_map.size[1]) / 600))
                surface_map.blit(layouts[2], (-(sidebar_map_x+ecart_map_x)*(16*self.current_map.size[0]) / 600, -(sidebar_map_y+ecart_map_y)*(16*self.current_map.size[1]) / 600))

            y = 0
            surface_tileset.fill((255, 255, 255))

            for tile in tilesets:
                surface_tileset.blit(tile, (-(sidebar_tileset_x+ecart_tileset_x)*tileset_size_x / 400, -(sidebar_tileset_y+ecart_tileset_y)*tileset_size_y / 400))
                y += tile.get_size()[1]

            display.blit(surface_bar, (0, 0))
            display.blit(surface_map, (0, 100))
            display.blit(surface_tileset, (616, 100))

            pygame.draw.rect(display, (255, 255, 255), (0, 700, 600, 16))
            pygame.draw.rect(display, (255, 255, 255), (616, 700, 400, 16))
            pygame.draw.rect(display, (0, 0, 0), (sidebar_map_x+ecart_map_x, 700, sidebar_map_x_size, 16))
            pygame.draw.rect(display, (0, 0, 0), (616+sidebar_tileset_x+ecart_tileset_x, 700, sidebar_tileset_x_size, 16))

            pygame.draw.rect(display, (255, 255, 255), (600, 100, 16, 600))
            pygame.draw.rect(display, (255, 255, 255), (1016, 100, 16, 600))
            pygame.draw.rect(display, (0, 0, 0), (600, 100+sidebar_map_y+ecart_map_y, 16, sidebar_map_y_size))
            pygame.draw.rect(display, (0, 0, 0), (1016, 100+sidebar_tileset_y+ecart_tileset_y, 16, sidebar_tileset_y_size))

            pygame.display.flip()

app = App()
app.open_map()
app.run()
