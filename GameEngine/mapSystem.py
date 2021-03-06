#-*-coding:utf-8-*-

"""
MapSystem of Game PokéLike
include :
    Tile class
    Tileset class
    Map class
"""

# Information sur le fichier :
__name__ = "mapSystem"
__version__ = "1"
__authors__ = "Lightpearl"

# Importation des modules complémentaires nécéssaires :
from . import logger
from . import constants
from . import entitySystem
from pygame.locals import *
import pygame
import os

display = pygame.display.set_mode((1, 1), HWSURFACE | SRCALPHA | NOFRAME)

# Création des objets du module :
class Tile:
    """
    Simple tile of a map
    """
    def __init__(self, id, size, image, hitbox, passages, ladder, nage, animated):
        self.id = id
        self.size = size
        self.image = image.convert_alpha()
        self.hitbox = hitbox
        self.passages = passages
        self.ladder = ladder
        self.nage = nage
        self.animated = animated

    def __repr__(self):
        return "<MapSystem.Tile:\n\tid={}\n\tsize={}\n\timage={}\n\thitbox={}\n\tpassages={}\n\tladder={}\n\tnage={}\n\tanimated={}\n>".format(self.id, self.size, self.image, self.hitbox, self.passages, self.ladder, self.nage, self.animated)

    def get_image(self):
        """
        Return the image of the tile
        """
        return self.image

    def get_hitbox(self):
        """
        Return the hitbox of the tile
        """
        return self.hitbox

    def get_passages(self):
        """
        Return the passages of the tile
        """
        return self.passages

    def is_ladder(self):
        """
        Return True if the tile can be considered as a ladder
        """
        return self.ladder

    def is_nage(self):
        """
        Return True if the player can swim on the tile
        """
        return self.nage

    def is_animated(self):
        """
        Return True if the tile is animated
        """
        return self.animated

    def set_id(self, new_id):
        """
        Change the id of the tile
        """
        self.id = new_id

class Tileset:
    """
    Set of tiles
    """
    def __init__(self, name, id, size, tiles):
        self.name = name
        self.id = id
        self.size = size
        self.tiles = tiles

    def get_tile(self, id):
        return self.tiles[id]

class Map:
    """
    Map of the game
    """
    def __init__(self, id, size, name, displayed_name, tileset_id, tiles_id, entities):
        from . import TILESETS
        self.id = id
        self.size = size
        self.name = name
        self.displayed_name = displayed_name
        self.tileset_id = tileset_id
        self.tiles_id = tiles_id
        self.entities = entities
        self.map_hitbox = [0 for _ in range(self.size[0]*self.size[1])]
        for pos, tile_id in enumerate(self.tiles_id):
            real_pos = pos % (self.size[0]*self.size[1])
            self.map_hitbox[real_pos] = max(self.map_hitbox[real_pos], TILESETS[self.tileset_id].tiles[tile_id].hitbox)
        self.render_surfaces()
        logger.log("Création de la map [{}] éffectué".format(self.name))

    def get_entities_hitbox(self):
        hitbox_data = [0 for _ in range(self.size[0] * self.size[1])]
        for entity in self.entities:
            pos = entity.pos[1] * self.size[0] + entity.pos[0]
            hitbox_data[pos] = entity.hitbox

        return hitbox_data

    def render_surfaces(self):
        from . import TILESETS
        air = pygame.Surface((self.size[0]*TILESETS[self.tileset_id].size, self.size[1]*TILESETS[self.tileset_id].size), HWSURFACE | SRCALPHA)
        ground = pygame.Surface((self.size[0]*TILESETS[self.tileset_id].size, self.size[1]*TILESETS[self.tileset_id].size), HWSURFACE | SRCALPHA)

        for x, tile_id in enumerate(self.tiles_id):
            pos_x = x % (self.size[0]*self.size[1]) % self.size[0] * TILESETS[self.tileset_id].size
            pos_y = x % (self.size[0]*self.size[1]) // self.size[0] * TILESETS[self.tileset_id].size
            tile = TILESETS[self.tileset_id].tiles[tile_id]
            if tile.hitbox == 2:
                air.blit(tile.image, (pos_x, pox_y))

            else:
                ground.blit(tile.image, (pos_x, pos_y))

        self.air_surface = air.convert_alpha()
        self.ground_surface = ground.convert_alpha()

    def render_entities(self):
        from . import TILESETS
        surface = pygame.Surface((self.size[0]*TILESETS[self.tileset_id].size, self.size[1]*TILESETS[self.tileset_id].size), HWSURFACE | SRCALPHA)
        for entity in self.entities:
            surface.blit(entity.sprites[entity.facing][entity.walk_state], (entity.save_pos[0]*TILESETS[self.tileset_id].size+entity.real_pos*entitySystem.DIRECTIONS[entity.facing][0], (entity.save_pos[1]*TILESETS[self.tileset_id].size+entity.real_pos*entitySystem.DIRECTIONS[entity.facing][1])))
        return surface.convert_alpha()

# Création des fonctions du module :
def load_tilesets(filename):
    tilesets = []
    generate_tileset = False
    get_tile_data = False
    tileset_name = ""
    tileset_id = 0
    tileset_size = 0
    tileset_pictures = []
    tileset_tiles = []
    images = {}

    with open(filename, "r") as file:
        for line in file:
            if line == "<Tileset>\n":
                generate_tileset = True
                get_tile_data = False
                tileset_name = ""
                tileset_id = 0
                tileset_size = 0
                tileset_pictures = []
                tileset_tiles = []
                images = {}

            elif line == "</Tileset>\n":
                generate_tileset = False
                tilesets.append(Tileset(tileset_name, tileset_id, tileset_size, tileset_tiles))

            elif generate_tileset and line == "[Data]\n":
                get_tile_data = True

            elif generate_tileset and line == "[/Data]\n":
                get_tile_data = False

            elif not get_tile_data and ":" in line and generate_tileset:
                command, content = line[:-1].split(":")
                if command == "Name":
                    tileset_name = content

                elif command == "Id":
                    tileset_id = int(content)

                elif command == "Size":
                    tileset_size = int(content)

                elif command == "Pictures":
                    tileset_pictures = eval(content)
                    images = {}
                    for picture in tileset_pictures:
                        images[picture] = pygame.image.load("GameData/pictures/Tilesets/{}.png".format(picture)).convert_alpha()

                else:
                    pass

            elif get_tile_data and ":" in line and generate_tileset:
                tiles_infos = [eval(info) for info in line[:-1].split(":")[1][1:-1].split(";")]
                picture = images[tiles_infos[5]]
                tile_surface = pygame.Surface((tileset_size, tileset_size), HWSURFACE | SRCALPHA)
                tile_surface.blit(picture, (-tiles_infos[6][0], -tiles_infos[6][1]))
                tileset_tiles.append(Tile(len(tileset_tiles), tileset_size, tile_surface.convert_alpha(), *tiles_infos[:-2]))

        file.close()

    TILESETS = [0 for _ in range(len(tilesets))]
    for tileset in tilesets:
        TILESETS[tileset.id] = tileset

    return TILESETS

def load_maps(filename):
    maps = []
    with open(filename, "r") as file1:
        for i, line in enumerate(file1):
            if line in ["\n", "", "empty"]:
                maps.append(None)
            else:
                map_id = i
                map_infos = line[:-1].split(":")[1][1:-1].split(", ")
                map_name = map_infos[0]
                map_displayed_name = map_infos[1]
                map_file = "GameData\\maps\\map{}.data".format(map_id)
                with open(map_file, "r") as file2:
                    map_tileset_id = -1
                    map_size = []
                    map_tiles_id = []
                    map_entities = []
                    getting_entities = False
                    for line in file2:
                        if not getting_entities and not line == "\n":
                            if line == "[Entities]\n":
                                getting_entities = True

                            else:
                                command, content = line[:-1].split(":")
                                if command == "Tileset":
                                    map_tileset_id = int(content)

                                elif command == "Size":
                                    map_size = [int(size) for size in content[1:-1].split(", ")]

                                else:
                                    map_tiles_id = [int(tile_id) for tile_id in content[1:-1].split(", ")]

                        elif getting_entities and not line in ["\n", "[/Entities]\n"]:
                            new_entity = entitySystem.get_entity_from_str(line[:-1], map_id)
                            map_entities.append(new_entity)

                        elif getting_entities and line == "[/Entities]\n":
                            getting_entities = False

                    file2.close()

                maps.append(Map(map_id, map_size, map_name, map_displayed_name, map_tileset_id, map_tiles_id, map_entities))
        file1.close()

    return maps

# Tests éffectués sur le module:
if __name__ == "__main__":
    os.chdir("../")
