#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Importation des modules complémentaires nécéssaires :
from pygame.locals import *
import pygame

# Initialisation de pygame :
pygame.init()

# Création de la fenêtre de l'app :
display = pygame.display.set_mode((160, 168))
pygame.display.set_caption("Tests Logiciel retouche image")

# Création des couleurs :
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SELECT = (255, 0, 255)

# Création des variables du module :
selected_color = WHITE
selected_option = "pencil"

# Création des ensembles :
COLORBOXES = []
OPTIONS = {}
matrix = [[WHITE, WHITE, WHITE, WHITE, WHITE],
          [WHITE, WHITE, WHITE, WHITE, WHITE],
          [WHITE, WHITE, WHITE, WHITE, WHITE],
          [WHITE, WHITE, WHITE, WHITE, WHITE],
          [WHITE, WHITE, WHITE, WHITE, WHITE]]

# Création des fonctions du module :
def signe(x, y):
    if x-y < 0:
        return -1
    else:
        return 1

def remplir(pixel, color1, color2):
    if color1 == color2:
        return
    if matrix[pixel[1]][pixel[0]] == color1:
        matrix[pixel[1]][pixel[0]] = color2
        try:
            remplir([pixel[0], pixel[1]-1], color1, color2)
        except:
            pass
        try:
            remplir([pixel[0], pixel[1]+1], color1, color2)
        except:
            pass
        try:
            remplir([pixel[0]-1, pixel[1]], color1, color2)
        except:
            pass
        try:
            remplir([pixel[0]+1, pixel[1]], color1, color2)
        except:
            pass

# Création des objets du module :
class ColorBox:
    """
    Bouton de choix des couleurs
    """
    def __init__(self, color):
        self.color = color
        COLORBOXES.append(self)

    def set_color(self):
        global selected_color
        selected_color = self.color

    def get_surface(self):
        surface = pygame.Surface((8, 8), HWSURFACE)
        surface.fill(self.color)
        if selected_color == self.color:
            pygame.draw.rect(surface, SELECT, (0, 0, 8, 8), 1)

        return surface.convert()

class Pencil:
    """
    Crayon de base pour colorier
    """
    def __init__(self):
        self.name = "pencil"
        OPTIONS["pencil"] = self

    def set_option(self):
        global selected_option
        selected_option = "pencil"

    def get_surface(self):
        surface = pygame.Surface((8, 8), HWSURFACE)
        surface.fill(WHITE)
        pygame.draw.rect(surface, BLACK, (0, 0, 8, 8), 1)
        pygame.draw.rect(surface, BLACK, (4, 2, 2, 4))
        pygame.draw.rect(surface, BLACK, (2, 4, 4, 2))
        if selected_option == "pencil":
            pygame.draw.rect(surface, SELECT, (0, 0, 8, 8), 1)

        return surface.convert()

    def action(self, pos):
        x = pos[0] // 32
        y = pos[1] // 32
        matrix[y][x] = selected_color

class Square:
    """
    Crayon de base pour colorier
    """
    def __init__(self):
        self.name = "square"
        OPTIONS["square"] = self

    def set_option(self):
        global selected_option
        selected_option = "square"

    def get_surface(self):
        surface = pygame.Surface((8, 8), HWSURFACE)
        surface.fill(WHITE)
        pygame.draw.rect(surface, BLACK, (0, 0, 8, 8), 1)
        pygame.draw.rect(surface, BLACK, (4, 2, 2, 4))
        pygame.draw.rect(surface, BLACK, (2, 4, 4, 2))
        if selected_option == "square":
            pygame.draw.rect(surface, SELECT, (0, 0, 8, 8), 1)

        return surface.convert()

    def action(self, pos1, pos2):
        x1 = pos1[0] // 32
        y1 = pos1[1] // 32
        x2 = pos2[0] // 32
        y2 = pos2[1] // 32
        x_f = min(x1, x2)
        x_l = max(x1, x2)
        y_f = min(y1, y2)
        y_l = max(y1, y2)
        for x in range(x_l-x_f+1):
            for y in range(y_l-y_f+1):
                matrix[y_f+y][x_f+x] = selected_color

class Filler:
    """
    Crayon de base pour colorier
    """
    def __init__(self):
        self.name = "filler"
        OPTIONS["filler"] = self

    def set_option(self):
        global selected_option
        selected_option = "filler"

    def get_surface(self):
        surface = pygame.Surface((8, 8), HWSURFACE)
        surface.fill(WHITE)
        pygame.draw.rect(surface, BLACK, (0, 0, 8, 8), 1)
        pygame.draw.rect(surface, BLACK, (4, 2, 2, 4))
        pygame.draw.rect(surface, BLACK, (2, 4, 4, 2))
        if selected_option == "filler":
            pygame.draw.rect(surface, SELECT, (0, 0, 8, 8), 1)

        return surface.convert()

    def action(self, pos):
        x = pos[0] // 32
        y = pos[1] // 32
        remplir([x, y], matrix[y][x], selected_color)

w = ColorBox(WHITE)
b = ColorBox(BLACK)
r = ColorBox(RED)
bl = ColorBox(BLUE)
g = ColorBox(GREEN)
p = Pencil()
s = Square()
f = Filler()

ram = [-1, -1]

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = pygame.mouse.get_pos()
                if 0 <= click[0] <= 8 and 0 <= click[1] <= 8:
                    p.set_option()

                elif 8 <= click[0] <= 16 and 0 <= click[1] <= 8:
                    s.set_option()

                elif 16 <= click[0] <= 24 and 0 <= click[1] <= 8:
                    f.set_option()

                elif 32 <= click[0] <= 40 and 0 <= click[1] <= 8:
                    w.set_color()

                elif 40 <= click[0] <= 48 and 0 <= click[1] <= 8:
                    b.set_color()

                elif 48 <= click[0] <= 56 and 0 <= click[1] <= 8:
                    r.set_color()

                elif 56 <= click[0] <= 64 and 0 <= click[1] <= 8:
                    bl.set_color()

                elif 64 <= click[0] <= 72 and 0 <= click[1] <= 8:
                    g.set_color()

                elif click[1] >= 8:
                    pos = [click[0], click[1]-8]
                    if selected_option == "pencil":
                        p.action(pos)

                    elif selected_option == "square":
                        ram = pos

                    elif selected_option == "filler":
                        f.action(pos)

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if not ram == [-1, -1]:
                    click = pygame.mouse.get_pos()
                    pos = [min(160, max(0, click[0])), min(160, max(0, click[1]-8))]
                    s.action(ram, pos)
                    ram = [-1, -1]

    display.fill(WHITE)
    display.blit(p.get_surface(), (0, 0))
    display.blit(s.get_surface(), (8, 0))
    display.blit(f.get_surface(), (16, 0))
    display.blit(w.get_surface(), (32, 0))
    display.blit(b.get_surface(), (40, 0))
    display.blit(r.get_surface(), (48, 0))
    display.blit(bl.get_surface(), (56, 0))
    display.blit(g.get_surface(), (64, 0))
    for x in range(5):
        for y in range(5):
            pygame.draw.rect(display, matrix[y][x], (x*32, 8+y*32, 32, 32))

    if not ram == [-1, -1]:
        pos = pygame.mouse.get_pos()
        pos = [pos[0], pos[1]+8]
        x1 = ram[0] // 32
        y1 = ram[1] // 32
        x2 = pos[0] // 32
        y2 = pos[1] // 32
        x_f = min(x1, x2)
        x_l = max(x1, x2)
        y_f = min(y1, y2)
        y_l = max(y1, y2)
        pygame.draw.rect(display, SELECT, (x_f*32, 8+y_f*32, 32*(x_l-x_f+1), 32*(y_l-y_f+1)), 2)
    
    pygame.display.flip()
        
