#-*-coding:utf-8-*-
""""""

# Information sur le fichier :
__name__ = "mapSystem"
__version__ = "1"
__authors__ = "Lightpearl"

# Importation des modules complémentaires nécéssaires :
from pygame.locals import *
from . import workerSystem
from . import constants
import pygame
import time

DIRECTIONS = {"North": (0, -1), "South": (0, 1), "East": (1, 0), "West": (-1, 0)}
PASSAGES = {"North": 0, "South": 1, "East": 2, "West": 3}

# Création des objets du module :
class Entity:
    """
    Entity class of the game
    """
    def __init__(self, sprite_size, sprites, name, hitbox, loader, code, pos, map_id):
        self.name = name
        self.hitbox = hitbox
        self.loader = loader
        self.code = code
        self.pos = pos
        self.map_id = map_id
        self.facing = "South"
        self.real_pos = 0
        self.state_pos = pos
        self.walk_state = 1
        self.save_pos = pos
        self.move_worker = workerSystem.QueueWorker(self.process_move)
        self.load_sprites(sprites, sprite_size)

    def load_sprites(self, sprites, sprite_size):
        self.sprites = {}
        self.sprite = pygame.Surface((sprite_size, sprite_size), HWSURFACE | SRCALPHA)

        # Nord
        self.sprites["North"] = []
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (0, -3*sprite_size))
        self.sprites["North"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (-sprite_size, -3*sprite_size))
        self.sprites["North"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (-2*sprite_size, -3*sprite_size))
        self.sprites["North"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

        # Sud
        self.sprites["South"] = []
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (0, 0))
        self.sprites["South"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (-sprite_size, 0))
        self.sprites["South"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (-2*sprite_size, 0))
        self.sprites["South"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

        # Est
        self.sprites["East"] = []
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (0, -2*sprite_size))
        self.sprites["East"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (-sprite_size, -2*sprite_size))
        self.sprites["East"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (-2*sprite_size, -2*sprite_size))
        self.sprites["East"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

        # Ouest
        self.sprites["West"] = []
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (0, -sprite_size))
        self.sprites["West"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (-sprite_size, -sprite_size))
        self.sprites["West"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

        self.sprite.blit(sprites, (-2*sprite_size, -sprite_size))
        self.sprites["West"].append(self.sprite.convert_alpha())
        self.sprite.fill((0, 0, 0, 0))

    def move(self, direction):
        from . import MAPS, TILESETS
        map = MAPS[self.map_id]
        entities_hitbox = map.get_entities_hitbox()
        new_x = max(0, min(map.size[0]-1, self.pos[0] + DIRECTIONS[direction][0]))
        new_y = max(0, min(map.size[1]-1, self.pos[1] + DIRECTIONS[direction][1]))
        entities_pos = entities_hitbox[new_y*map.size[0]+new_x]
        if  not map.map_hitbox[new_y*map.size[0]+new_x] == 1 and not entities_pos == 1 and not self.pos == (new_x, new_y): #not map_tile.nage and map_tile.passages[PASSAGES[direction]] and
            self.move_worker.put((direction, (new_x, new_y)))
            self.pos = (new_x, new_y)

    def process_move(self, action):
        self.facing = action[0]
        self.real_pos = constants.ENTITY_PIXEL_SPEED
        self.state_pos = action[1]
        from . import MAPS, TILESETS
        goal = TILESETS[MAPS[self.map_id].tileset_id].size
        while self.real_pos % goal != 0:
            if self.real_pos % goal <= goal//2:
                self.walk_state = 0
                self.real_pos += constants.ENTITY_PIXEL_SPEED

            elif self.real_pos % goal > goal//2:
                self.walk_state = 2
                self.real_pos += constants.ENTITY_PIXEL_SPEED

            time.sleep(constants.ENTITY_SPEED)

        self.real_pos = 0
        self.walk_state = 1
        self.save_pos = self.state_pos


def get_entity_from_str(string, map_id):
    content = dict([component.split(": ") for component in string[1:-1].split("; ")])
    return Entity(int(content["sprite_size"]), pygame.image.load(content["sprite"]).convert_alpha(), content["name"], int(content["hitbox"]), content["loader"], eval(content["code"]), eval(content["pos"]), map_id)
