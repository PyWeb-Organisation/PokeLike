#-*- coding:utf-8-*-

# Importation du GameEngine
import GameEngine as GE
import random

size = (GE.constants.DISPLAY_SIZE[0]*GE.TILESETS[0].size, GE.constants.DISPLAY_SIZE[1]*GE.TILESETS[0].size)

display = GE.pygame.display.set_mode(size, GE.HWSURFACE | GE.SRCALPHA)

icone = GE.pygame.image.load("GameData\\pictures\\icone.png").convert_alpha()

GE.pygame.display.set_icon(icone)

GE.pygame.display.set_caption("Test Envirronement PokéLike")

current_map = GE.MAPS[0]

player_pos = (0, 0)

continuer = True

ENTITYTIMER = GE.USEREVENT + 1
GE.pygame.time.set_timer(ENTITYTIMER, GE.constants.ENTITY_FREQUECY)

while continuer:
    for event in GE.pygame.event.get():
        if event.type == GE.QUIT:
            continuer = False

        elif event.type == ENTITYTIMER:
            for entity in current_map.entities:
                if not entity.real_pos == 0:
                    entity.move(random.choice(["North", "South", "East", "West"]))

        else:
            pass

    for entity in current_map.entities:
        entity.process_path()

    surfaces = current_map.render(player_pos)

    display.fill((0, 0, 0))

    for surface in surfaces:
        display.blit(surface, (0, 0))

    GE.pygame.display.flip()

GE.pygame.quit()
exit(-1)
