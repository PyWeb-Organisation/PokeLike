#-*- coding:utf-8-*-

# Importation du GameEngine
import GameEngine as GE
import random


size = (GE.constants.DISPLAY_SIZE[0]*GE.TILESETS[0].size, GE.constants.DISPLAY_SIZE[1]*GE.TILESETS[0].size)

display = GE.pygame.display.set_mode(size, GE.HWSURFACE | GE.SRCALPHA)

icone = GE.pygame.image.load("GameData\\pictures\\icone.png").convert_alpha()

GE.pygame.display.set_icon(icone)

GE.pygame.display.set_caption("Test Envirronement PokéLike")

<<<<<<< HEAD
clock = GE.pygame.time.Clock()

current_map = GE.MAPS[0]
=======
clock=GE.pygame.time.Clock()

current_map = GE.MAPS[GE.constants.CURRENT_MAP]

player=GE.playerSystem.Player()
>>>>>>> b02a77da180dba24f4092ce4f766f538dd9ad39a

for entity in current_map.entities:
    entity.move_worker.start()

player.move_worker.start()
player_pos = (0, 0)

continuer = True

ENTITYTIMER = GE.USEREVENT + 1
GE.pygame.time.set_timer(ENTITYTIMER, GE.constants.ENTITY_FREQUECY)

while continuer:
    clock.tick(60)
    for event in GE.pygame.event.get():
        if event.type == GE.QUIT:
            continuer = False

        elif event.type == ENTITYTIMER:
            for entity in current_map.entities:
                if entity.real_pos == 0:
                    entity.move(random.choice(["North", "South", "East", "West"]))
        elif event.type == GE.KEYDOWN:
            if event.key == GE.K_UP:
                player.move('North')
            elif event.key == GE.K_DOWN:
                player.move('South')
            elif event.key == GE.K_LEFT:
                player.move('West')
            elif event.key == GE.K_RIGHT:
                player.move('East')
        else:
            pass

    surfaces = current_map.render(player.save_pos)

    display.fill((0, 0, 0))
    min_x=max(0,min(player.save_pos[0]-GE.constants.DISPLAY_SIZE[0]//2,current_map.size[0]-GE.constants.DISPLAY_SIZE[0]))
    min_y=max(0,min(player.save_pos[1]-GE.constants.DISPLAY_SIZE[1]//2,current_map.size[1]-GE.constants.DISPLAY_SIZE[1]))
    display.blit(surfaces[0],(0,0))
    display.blit(player.sprites[player.facing][player.walk_state],((player.save_pos[0]-min_x)*GE.TILESETS[current_map.tileset_id].size+GE.entitySystem.DIRECTIONS[player.facing][0]*player.real_pos,(player.save_pos[1]-min_y)*GE.TILESETS[current_map.tileset_id].size+GE.entitySystem.DIRECTIONS[player.facing][1]*player.real_pos))
    display.blit(surfaces[1],(0,0))
    display.blit(surfaces[2],(0,0))
    GE.pygame.display.flip()

for entity in current_map.entities:
    entity.move_worker.destroy()


GE.pygame.quit()
exit(-1)
