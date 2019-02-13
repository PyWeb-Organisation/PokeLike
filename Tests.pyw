#-*- coding:utf-8-*-

# Importation du GameEngine
import GameEngine as GE
import random


size = (GE.constants.DISPLAY_SIZE[0]*GE.TILESETS[0].size, GE.constants.DISPLAY_SIZE[1]*GE.TILESETS[0].size)

display = GE.pygame.display.set_mode(size, GE.HWSURFACE | GE.SRCALPHA)

icone = GE.pygame.image.load("GameData\\pictures\\icone.png").convert_alpha()

GE.pygame.display.set_icon(icone)

GE.pygame.display.set_caption("Test Envirronement PokéLike")

JOYSTICK_CONNECTED = GE.pygame.joystick.get_count() >= 1

clock=GE.pygame.time.Clock()

current_map = GE.MAPS[GE.constants.CURRENT_MAP]

player=GE.PLAYER

for entity in current_map.entities:
    entity.move_worker.start()

player.move_worker.start()
player_pos = (0, 0)

continuer = True

ENTITYTIMER = GE.USEREVENT + 1
GE.pygame.time.set_timer(ENTITYTIMER, GE.constants.ENTITY_FREQUECY)

if JOYSTICK_CONNECTED:
    MAIN_JOYSTICK = GE.pygame.joystick.Joystick(0)
    MAIN_JOYSTICK.init()

while continuer:
    clock.tick(120)
    for event in GE.pygame.event.get():
        if event.type == GE.QUIT:
            continuer = False

        elif event.type == ENTITYTIMER:
            for entity in current_map.entities:
                if entity.real_pos == 0:
                    entity.move(random.choice(["North", "South", "East", "West"]))

    if JOYSTICK_CONNECTED:

        if MAIN_JOYSTICK.get_button(1):
            for entity in current_map.entities:
                if entity.pos == (player.pos[0]+GE.entitySystem.DIRECTIONS[player.facing][0], player.pos[1]+GE.entitySystem.DIRECTIONS[player.facing][1]):
                    entity.action()

        hat_state = MAIN_JOYSTICK.get_hat(0)
        if hat_state == (0, 1):
            player.move("North")
        elif hat_state == (0, -1):
            player.move("South")
        elif hat_state == (1, 0):
            player.move("East")
        elif hat_state == (-1, 0):
            player.move("West")

    keys = GE.pygame.key.get_pressed()
    if keys[GE.K_q]:
        for entity in current_map.entities:
            if entity.pos == (player.pos[0]+GE.entitySystem.DIRECTIONS[player.facing][0], player.pos[1]+GE.entitySystem.DIRECTIONS[player.facing][1]):
                entity.action()
    elif keys[GE.K_UP]:
        player.move("North")
    elif keys[GE.K_DOWN]:
        player.move("South")
    elif keys[GE.K_LEFT]:
        player.move("West")
    elif keys[GE.K_RIGHT]:
        player.move("East")

    entities = current_map.render_entities()

    display.fill((0, 0, 0))
    camera = player.get_camera()
    display.blit(current_map.ground_surface, camera)
    display.blit(entities, camera)
    display.blit(player.sprites[player.facing][player.walk_state], (player.save_pos[0]*48+player.real_pos*GE.entitySystem.DIRECTIONS[player.facing][0]+camera[0], player.save_pos[1]*48+player.real_pos*GE.entitySystem.DIRECTIONS[player.facing][1]+camera[1]))
    display.blit(current_map.air_surface, camera)

    GE.pygame.display.flip()

for entity in current_map.entities:
    entity.move_worker.destroy()


GE.pygame.quit()
exit(-1)
