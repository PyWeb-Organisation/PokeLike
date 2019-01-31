#-*-coding:utf-8-*-
""""""

# Information sur le fichier :
__name__ = "mapSystem"
__version__ = "1"
__authors__ = "Lightpearl"

# Importation des modules complémentaires nécéssaires :
from pygame.locals import *
import pygame

DIRECTIONS = [(0, -1), (0, 1), (1, 0), (-1, 0)]

# Création des objets du module :
class Entity:
    """
    Entity class of the game
    """
    def __init__(self, sprite_size, sprite, name, hitbox, loader, code, pos, map):
        self.name = name
        self.hitbox = hitbox
        self.loader = loader
        self.code = code
        self.pos = pos
        self.map = map
        self.load_sprites(sprites, sprite_size)

    def load_sprites(self, sprites, sprite_size):
        self.sprites = {}
        self.sprite = pygame.Surface((sprite_size, sprite_size), HWSURFACE | SRCALPHA)

        # Nord
        self.sprites["Nord"] = []
        self.sprite.blit(sprites, (0, -3*sprite_size))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

        self.sprite.blit(sprites, (-sprite_size, -3*sprite_size))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

        self.sprite.blit(sprites, (-2*sprite_size, -3*sprite_size))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

        # Sud
        self.sprites["Sud"] = []
        self.sprite.blit(sprites, (0, 0))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

        self.sprite.blit(sprites, (-sprite_size, 0))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

        self.sprite.blit(sprites, (-2*sprite_size, 0))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

        # Est
        self.sprites["Est"] = []
        self.sprite.blit(sprites, (0, -2*sprite_size))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

        self.sprite.blit(sprites, (-sprite_size, -2*sprite_size))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

        self.sprite.blit(sprites, (-2*sprite_size, -2*sprite_size))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

        # Ouest
        self.sprites["Ouset"] = []
        self.sprite.blit(sprites, (0, -sprite_size))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

        self.sprite.blit(sprites, (-sprite_size, -sprite_size))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

        self.sprite.blit(sprites, (-2*sprite_size, -sprite_size))
        self.sprites["Nord"].append(self.sprite.convert_alpha())

    def move(self, direction):
        entities_hitbox = self.map.get_entities_hitbox()
        new_x = max(0, min(self.map.size[0]-1, self.pos[0] + DIRECTIONS[direction][0]))
        new_y = max(0, min(self.map.size[1]-1, self.pos[1] + DIRECTIONS[direction][1]))
        map_tile = self.map.tiles[new_y*self.map.size[0]+new_x]
        entities_pos = entities_hitbox[new_y*self.map.size[0]+new_x]
        if not map_tile.nage and map_tile.passages[direction] and not map_tile.hitbox == 1 and not entities_pos == 1:
            self.pos = (new_x, new_y)

def get_entity_from_str(string):
    return None
