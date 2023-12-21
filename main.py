from engine import *
import pygame

ctx = GameContext((640, 360), pygame.SCALED, True)

GRASS_ID = 1
TILESET = load_sprite("data/images/tilesets/main.png", (32, 32))

background = Tilemap(ctx, 32, 0)
background.tileset = TILESET
background.place_pattern([[GRASS_ID for i in range(100)] for j in range(100)], (0, 0))

scene = Scene()
scene.link(background)

def game_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctx.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                ctx.toggle_fullscreen()
    scene.update()
    ctx.set_caption(str(round(ctx.get_fps())))

ctx.run(game_loop=game_loop)
