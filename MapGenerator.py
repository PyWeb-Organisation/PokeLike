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

pygame.init()
display = pygame.display.set_mode((1032, 716))

# Création des variables globales du script :
tile_size = 16
inutile = tkinter.Tk()
inutile.geometry("0x0")
inutile.overrideredirect(True)

# Création des fonctions du script :
def save_map(size, tilesets, layouts, filename):
    with open(filename, "w") as file:
        file.write("size : {}\n".format(", ".join([str(item) for item in size])))

        for tileset in tilesets:
            file.write("tileset : {}\n".format(tileset))

        file.write("[Layout1]\n")
        for line in layouts[0]:
            file.write("{}\n".format(" ".join([str(item) for item in line])))
        file.write("[/Layout1]\n")

        file.write("[Layout2]\n")
        for line in layouts[1]:
            file.write("{}\n".format(" ".join([str(item) for item in line])))
        file.write("[/Layout2]\n")

        file.write("[Layout3]\n")
        for line in layouts[2]:
            file.write("{}\n".format(" ".join([str(item) for item in line])))
        file.write("[/Layout3]\n")
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
        f.quit()
    button = tkinter.Button(f, text="Valider", command=get_size)
    entry1.grid(row=0, column=0)
    entry2.grid(row=1, column=0)
    button.grid(row=1, column=1)
    f.mainloop()
    return Map(sizes, [TileSet("main_tile_set")])

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
        print("loading new map")
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
        self.current_map = Map([21, 21], [TileSet("main_tile_set")])
        self.see_layout = 1
        self.tool = "pencil"
        self.selected_tile = 0

    def add_tileset_to_map(self):
        path = fd.askopenfilename()
        filename = os.path.splitext(os.path.basename(path))[0]
        tileset = TileSet(filename)
        self.current_map.add_tileset(tileset)

    def create_map(self):
        self.current_map = create_new_map()

    def save_current_map(self):
        path = fd.asksaveasfilename()
        if not path == '':
            save_map(self.current_map.size, self.current_map.tilesets_names, self.current_map.layouts, path)

    def filler(self, pos, old_tile, new_tile):
        if old_tile == new_tile:
            return
        if self.current_map.layouts[self.see_layout-1][pos[1]][pos[0]] == old_tile:
            self.current_map.layouts[self.see_layout-1][pos[1]][pos[0]] = new_tile
            try:
                self.filler([pos[0], pos[1]-1], old_tile, new_tile)
            except:
                pass
            try:
                self.filler([pos[0], pos[1]+1], old_tile, new_tile)
            except:
                pass
            try:
                self.filler([pos[0]-1, pos[1]], old_tile, new_tile)
            except:
                pass
            try:
                self.filler([pos[0]+1, pos[1]], old_tile, new_tile)
            except:
                pass

    def open_map(self):
        path = fd.askopenfilename()
        tilesets = []
        size = []
        layouts = [[], [], []]
        layout1 = False
        layout2 = False
        layout3 = False
        current_layout = []

        if not path == '':

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
        font = pygame.font.SysFont("Arial", 8, bold=True)
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

        pencil_button = pygame.Surface((50, 50), HWSURFACE | SRCALPHA)
        square_button = pygame.Surface((50, 50), HWSURFACE | SRCALPHA)
        filler_button = pygame.Surface((50, 50), HWSURFACE | SRCALPHA)
        pencil_button.fill((200, 200, 200))
        square_button.fill((200, 200, 200))
        filler_button.fill((200, 200, 200))
        pygame.draw.rect(pencil_button, (0, 0, 0), (20, 10, 10, 30))
        pygame.draw.rect(pencil_button, (0, 0, 0), (10, 20, 30, 10))
        pygame.draw.rect(square_button, (0, 0, 0), (10, 10, 30, 30))
        pygame.draw.circle(filler_button, (0, 0, 0), (25, 25), 15)

        layout1_button = pygame.Surface((100, 50), HWSURFACE | SRCALPHA)
        layout2_button = pygame.Surface((100, 50), HWSURFACE | SRCALPHA)
        layout3_button = pygame.Surface((100, 50), HWSURFACE | SRCALPHA)
        layout1_button.fill((150, 100, 50))
        layout2_button.fill((255, 0, 0))
        layout3_button.fill((100, 200, 255))
        text_1 = font.render("Sol", True, (255, 255, 255))
        text_1_rect = text_1.get_rect(center=(50, 25))
        layout1_button.blit(text_1, text_1_rect)
        text_2 = font.render("Objets", True, (255, 255, 255))
        text_2_rect = text_2.get_rect(center=(50, 25))
        layout2_button.blit(text_2, text_2_rect)
        text_3 = font.render("Ciel", True, (255, 255, 255))
        text_3_rect = text_3.get_rect(center=(50, 25))
        layout3_button.blit(text_3, text_3_rect)

        save_button = pygame.Surface((50, 50), HWSURFACE | SRCALPHA)
        load_button = pygame.Surface((50, 50), HWSURFACE | SRCALPHA)
        load_tileset_button = pygame.Surface((50, 50), HWSURFACE | SRCALPHA)
        create_new_button = pygame.Surface((50, 50), HWSURFACE | SRCALPHA)
        save_button.fill((220, 220, 220))
        load_button.fill((220, 220, 220))
        load_tileset_button.fill((220, 220, 220))
        create_new_button.fill((220, 220, 220))
        pygame.draw.rect(save_button, (0, 0, 0), (0, 0, 50, 50), 1)
        pygame.draw.rect(load_button, (0, 0, 0), (0, 0, 50, 50), 1)
        pygame.draw.rect(load_tileset_button, (0, 0, 0), (0, 0, 50, 50), 1)
        pygame.draw.rect(create_new_button, (0, 0, 0), (0, 0, 50, 50), 1)
        text = font.render("Save", True, (0, 0, 0))
        text_rect = text.get_rect(center=(25, 25))
        save_button.blit(text, text_rect)
        text = font.render("Load map", True, (0, 0, 0))
        text_rect = text.get_rect(center=(25, 25))
        load_button.blit(text, text_rect)
        text = font.render("Load tileset", True, (0, 0, 0))
        text_rect = text.get_rect(center=(25, 25))
        load_tileset_button.blit(text, text_rect)
        text = font.render("Create new", True, (0, 0, 0))
        text_rect = text.get_rect(center=(25, 25))
        create_new_button.blit(text, text_rect)

        cursor = pygame.Surface((16, 16), HWSURFACE | SRCALPHA)
        pygame.draw.rect(cursor, (150, 175, 0), (0, 0, 15, 15), 2)

        click_map = False
        click_map_pos = [-1, -1]
        ram_click_map = [-1, -1]

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

                        if 732 <= pos[0] <= 832 and 50 <= pos[1] <= 100:
                            self.see_layout = 1

                        if 832 <= pos[0] <= 932 and 50 <= pos[1] <= 100:
                            self.see_layout = 2

                        if 932 <= pos[0] <= 1032 and 50 <= pos[1] <= 100:
                            self.see_layout = 3

                        if 0 <= pos[0] <= 50 and 50 <= pos[1] <= 100:
                            self.tool = "pencil"

                        if 50 <= pos[0] <= 100 and 50 <= pos[1] <= 100:
                            self.tool = "square"

                        if 100 <= pos[0] <= 150 and 50 <= pos[1] <= 100:
                            self.tool = "filler"

                        if 0 <= pos[0] <= 50 and 0 <= pos[1] <= 50:
                            self.save_current_map()

                        if 50 <= pos[0] <= 100 and 0 <= pos[1] <= 50:
                            self.open_map()
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

                        if 100 <= pos[0] <= 150 and 0 <= pos[1] <= 50:
                            self.add_tileset_to_map()
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

                        if 150 <= pos[0] <= 200 and 0 <= pos[1] <= 50:
                            self.create_map()
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

                        if 616 <= pos[0] <= 1016 and 100 <= pos[1] <= 700:
                            real_pos_x = sidebar_tileset_x*tileset_size_x / 400 + pos[0] - 616
                            real_pos_y = sidebar_tileset_y*tileset_size_y / 600 + pos[1] - 100
                            x = (real_pos_x) // 16
                            y = (real_pos_y) // 16
                            self.selected_tile = y * (tileset_size_x//16) + x

                        if 0 <= pos[0] <= 600 and 100 <= pos[1] <= 700:
                            click_map = True
                            click_map_pos = pos
                            if self.tool == "filler":
                                try:
                                    mouse_pos = pygame.mouse.get_pos()
                                    real_pos_x = sidebar_map_x*(16*self.current_map.size[0]) / 600 + mouse_pos[0]
                                    real_pos_y = sidebar_map_y*(16*self.current_map.size[1]) / 600 + mouse_pos[1]
                                    x = int(real_pos_x // 16)
                                    y = int((real_pos_y-100) // 16)
                                    self.filler((x, y), self.current_map.layouts[self.see_layout-1][y][x], int(self.selected_tile))
                                except:
                                    pass

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

                        if click_map:
                            click_map = False
                            ram_click_map = pos

            if click_map and self.tool == "pencil":
                try:
                    mouse_pos = pygame.mouse.get_pos()
                    real_pos_x = sidebar_map_x*(16*self.current_map.size[0]) / 600 + mouse_pos[0]
                    real_pos_y = sidebar_map_y*(16*self.current_map.size[1]) / 600 + mouse_pos[1]
                    x = int(real_pos_x // 16)
                    y = int((real_pos_y-100) // 16)
                    self.current_map.layouts[self.see_layout-1][y][x] = int(self.selected_tile)
                except:
                    pass

            if self.tool == "square" and ram_click_map != [-1, -1]:
                real_pos_x_1 = min(16*self.current_map.size[0], sidebar_map_x*(16*self.current_map.size[0]) / 600 + click_map_pos[0])
                real_pos_y_1 = min(16*self.current_map.size[1]+100, sidebar_map_y*(16*self.current_map.size[1]) / 600 + click_map_pos[1])
                real_pos_x_2 = min(16*self.current_map.size[0], sidebar_map_x*(16*self.current_map.size[0]) / 600 + ram_click_map[0])
                real_pos_y_2 = min(16*self.current_map.size[1]+100, sidebar_map_y*(16*self.current_map.size[1]) / 600 + ram_click_map[1])
                ram_click_map = [-1, -1]
                click_map_pos = [-1, -1]
                x1 = int(real_pos_x_1 // 16)
                y1 = int((real_pos_y_1-100) // 16)
                x2 = int(real_pos_x_2 // 16)
                y2 = int((real_pos_y_2-100) // 16)
                for i in range(abs(x2-x1)):
                    for j in range(abs(y2-y1)):
                        self.current_map.layouts[self.see_layout-1][min(y1, y2)+j][min(x1, x2)+i] = int(self.selected_tile)

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

            mouse_pos = pygame.mouse.get_pos()

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
                surface_tileset.blit(tile, (-(sidebar_tileset_x+ecart_tileset_x)*tileset_size_x / 400, y-(sidebar_tileset_y+ecart_tileset_y)*tileset_size_y / 600))
                y += tile.get_size()[1]

            pygame.draw.rect(surface_tileset, (150, 0, 125), ((self.selected_tile%(tileset_size_x//16))*16-(sidebar_tileset_x+ecart_tileset_x)*tileset_size_x / 400, (self.selected_tile//(tileset_size_x//16))*16-(sidebar_tileset_y+ecart_tileset_y)*tileset_size_y / 600, 15, 15), 2)

            display.blit(surface_bar, (0, 0))
            display.blit(surface_map, (0, 100))
            display.blit(surface_tileset, (616, 100))

            # Drawing Cursor
            if 0 <= mouse_pos[0] <= 600 and 100 <= mouse_pos[1] <= 700:
                if click_map_pos == [-1, -1]:
                    real_pos_x = sidebar_map_x*(16*self.current_map.size[0]) / 600 + mouse_pos[0]
                    real_pos_y = sidebar_map_y*(16*self.current_map.size[1]) / 600 + mouse_pos[1]
                    x = (real_pos_x // 16) * 16 - sidebar_map_x*(16*self.current_map.size[0]) / 600
                    y = 100 + ((real_pos_y-100) // 16) * 16 - sidebar_map_y*(16*self.current_map.size[1]) / 600
                    display.blit(cursor, (x, y))

                elif self.tool == "square":
                    mouse_pos = pygame.mouse.get_pos()
                    real_pos_x_1 = min(16*self.current_map.size[0], sidebar_map_x*(16*self.current_map.size[0]) / 600 + click_map_pos[0])
                    real_pos_y_1 = min(16*self.current_map.size[1]+100, sidebar_map_y*(16*self.current_map.size[1]) / 600 + click_map_pos[1])
                    real_pos_x_2 = min(16*self.current_map.size[0], sidebar_map_x*(16*self.current_map.size[0]) / 600 + mouse_pos[0])
                    real_pos_y_2 = min(16*self.current_map.size[1]+100, sidebar_map_y*(16*self.current_map.size[1]) / 600 + mouse_pos[1])
                    x1 = (real_pos_x_1 // 16) * 16 - sidebar_map_x*(16*self.current_map.size[0]) / 600
                    y1 = 100 + ((real_pos_y_1-100) // 16) * 16 - sidebar_map_y*(16*self.current_map.size[1]) / 600
                    x2 = (real_pos_x_2 // 16) * 16 - sidebar_map_x*(16*self.current_map.size[0]) / 600
                    y2 = 100 + ((real_pos_y_2-100) // 16) * 16 - sidebar_map_y*(16*self.current_map.size[1]) / 600
                    x = min(x1, x2)
                    y = min(y1, y2)
                    rect_x = abs(x1-x2)
                    rect_y = abs(y1-y2)
                    print(rect_y, y1, y2)
                    pygame.draw.rect(display, (150, 175, 0), (x, y, rect_x-1, rect_y-1), 2)


            if 616 <= mouse_pos[0] <= 1016 and 100 <= mouse_pos[1] <= 700:
                real_pos_x = sidebar_tileset_x*tileset_size_x / 400 + mouse_pos[0]
                real_pos_y = sidebar_tileset_y*tileset_size_y / 600 + mouse_pos[1]
                x = 616 + ((real_pos_x-616) // 16) * 16 - sidebar_tileset_x*tileset_size_x / 400
                y = 100 + ((real_pos_y-100) // 16) * 16 - sidebar_tileset_y*tileset_size_y / 600
                display.blit(cursor, (x, y))

            pygame.draw.rect(display, (255, 255, 255), (0, 700, 600, 16))
            pygame.draw.rect(display, (255, 255, 255), (616, 700, 400, 16))
            pygame.draw.rect(display, (0, 0, 0), (sidebar_map_x+ecart_map_x, 700, sidebar_map_x_size, 16))
            pygame.draw.rect(display, (0, 0, 0), (616+sidebar_tileset_x+ecart_tileset_x, 700, sidebar_tileset_x_size, 16))

            pygame.draw.rect(display, (255, 255, 255), (600, 100, 16, 600))
            pygame.draw.rect(display, (255, 255, 255), (1016, 100, 16, 600))
            pygame.draw.rect(display, (0, 0, 0), (600, 100+sidebar_map_y+ecart_map_y, 16, sidebar_map_y_size))
            pygame.draw.rect(display, (0, 0, 0), (1016, 100+sidebar_tileset_y+ecart_tileset_y, 16, sidebar_tileset_y_size))

            display.blit(layout1_button, (732, 50))
            display.blit(layout2_button, (832, 50))
            display.blit(layout3_button, (932, 50))
            pygame.draw.rect(display, (0, 0, 0), (732+100*(self.see_layout-1), 50, 99, 49), 2)

            display.blit(pencil_button, (0, 50))
            display.blit(square_button, (50, 50))
            display.blit(filler_button, (100, 50))
            if self.tool == "pencil":
                pygame.draw.rect(display, (0, 0, 0), (0, 50, 49, 49), 2)

            if self.tool == "square":
                pygame.draw.rect(display, (0, 0, 0), (50, 50, 49, 49), 2)

            if self.tool == "filler":
                pygame.draw.rect(display, (0, 0, 0), (100, 50, 49, 49), 2)

            display.blit(save_button, (0, 0))
            display.blit(load_button, (50, 0))
            display.blit(load_tileset_button, (100, 0))
            display.blit(create_new_button, (150, 0))

            pygame.display.flip()

app = App()
#app.open_map()
app.run()
