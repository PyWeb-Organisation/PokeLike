#-*- coding:utf-8-*-

# Importation du GameEngine
import GameEngine as GE

size = (GE.constants.DISPLAY_SIZE[0]*GE.TILESETS[0].size, GE.constants.DISPLAY_SIZE[1]*GE.TILESETS[0].size)

display = GE.pygame.display.set_mode(size, GE.HWSURFACE | GE.SRCALPHA)

current_map = GE.MAPS[0]

player_pos = (0, 0)

continuer = True

while continuer:
    for event in GE.pygame.event.get():
        if event.type == GE.QUIT:
            continuer = False

        else:
            pass

    surfaces = current_map.render(player_pos)

    display.fill((0, 0, 0))

    for surface in surfaces:
        display.blit(surface, (0, 0))

    GE.pygame.display.flip()

pygame.quit()
exit(-1)
