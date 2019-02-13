#-*-coding:utf-8-*-
""""""

# Information sur le fichier :
__name__ = "mapSystem"
__version__ = "1"
__authors__ = "Lightpearl"

# Importation des modules complémentaires nécéssaires :
from . import logger
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
        self.blocked = False
        self.facing = "South"
        self.real_pos = 0
        self.walk_state = 1
        self.save_pos = pos
        self.move_worker = workerSystem.QueueWorker(self.process_move)
        self.load_sprites(sprites, sprite_size)
        logger.log("Création de l'entitée [{}] éffectuée".format(self.name))

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
        new_x = max(0, min(map.size[0]-1, self.pos[0] + DIRECTIONS[direction][0]))
        new_y = max(0, min(map.size[1]-1, self.pos[1] + DIRECTIONS[direction][1]))
        if self.real_pos == 0 and not self.blocked:
            self.move_worker.put((direction, (new_x, new_y)))

    def action(self):
        for code in self.code:
            CODE_DICTIONNARY[code[0]](*code[1:], self)

    def process_move(self, action):
        logger.log("process move of entity {} with parameters {}".format(self.name, action), worker="MOVE-WORKER")
        self.facing = action[0]
        from . import MAPS, TILESETS, PLAYER
        map = MAPS[self.map_id]
        map_hitbox=map.map_hitbox[action[1][1]*map.size[0]+action[1][0]]
        entity_hitbox=map.get_entities_hitbox()[action[1][1]*map.size[0]+action[1][0]]
        if  not map_hitbox == 1 and not entity_hitbox == 1 and not self.pos == (action[1][0], action[1][1]) and not PLAYER.pos == (action[1][0], action[1][1]): #not map_tile.nage and map_tile.passages[PASSAGES[direction]] and
            self.real_pos = constants.ENTITY_PIXEL_SPEED
            self.pos = action[1]
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
            self.save_pos = self.pos


def get_entity_from_str(string, map_id):
    content = dict([component.split(": ") for component in string[1:-1].split("; ")])
    return Entity(int(content["sprite_size"]), pygame.image.load(content["sprite"]).convert_alpha(), content["name"], int(content["hitbox"]), content["loader"], eval(content["code"]), eval(content["pos"]), map_id)

def show_message(message_list, entity):
    from . import PLAYER
    entity.blocked = True
    PLAYER.blocked = True
    time.sleep(2)
    entity.blocked = False
    PLAYER.blocked = False


# Création des variables du module :
CODE_DICTIONNARY = {
    "message": show_message,
}
