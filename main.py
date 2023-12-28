from engine import *
import pygame

set_path("data/images/")

ctx = GameContext((640, 360), pygame.SCALED | pygame.RESIZABLE, True)

ctx.tile_size = 32
ctx.size = [30, 30]
ctx.shiney_chance = 100

from scripts import *

ctx.assets = TILESETS | SPRITES | OTHER
GRASS_ID = 1

wall = [
    [None for i in   range(5)],
    [None, 13, None, None, None],
    [13, None, None, 510,   None],
    [13, 13, 13, None,     13],
    [None, None, 13, None, 13]
]

background = Tilemap(ctx, 32, 0) 
background.tileset = ctx.assets["main_tileset"]
background.place_pattern([[GRASS_ID for i in range(ctx.size[0])] for j in range(ctx.size[1])], (0, 0))
background.place_tile(338, (10, 10))
background.place_pattern([[338 for i in range(5)] for i in range(5)], (0, 0), 0)
background.set_animation_tile(338, 0.1, [338, 346, 354, 362, 370, 394])

collision = Tilemap(ctx, 32, 1)
collision.tileset = ctx.assets["main_tileset"]
collision.place_pattern(wall, (5, 5))
collision.place_pattern([[13 for i in range(ctx.size[0]+2)]], (-1, -1))
collision.place_pattern([[13] for i in range(ctx.size[0]+2)], (-1, -1))
collision.tags.append("#solid")

player = Player(ctx, [0, 0])

ctx.scene = Scene()
ctx.scene.link(background, collision, player)
for i in range(10):
    ctx.scene.link(Pokemon(ctx, [100, 100], range(60-10, 61)[i+1], 1.5, (100, 90, 50)))

def game_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctx.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                ctx.toggle_fullscreen()
                
    ctx.draw_rect(pygame.Rect((0,0), ctx.get_display_size()), (0,0,0))
    ctx.scene.update()
    ctx.set_caption(str(round(ctx.get_fps())))
    ctx.scroll(player.rect().center, 15)
    if ctx.camera[0] < 0:
        ctx.camera[0] = 0
    if ctx.camera[1] < 0:
        ctx.camera[1] = 0

ctx.run(game_loop=game_loop)
