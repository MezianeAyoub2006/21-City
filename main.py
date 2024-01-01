from engine import *
import pygame

set_path("data/images/")

ctx = GameContext((640, 360), pygame.SCALED | pygame.RESIZABLE, True)

ctx.tile_size = 32
ctx.size = [30, 30]
ctx.shiney_chance = 4096
ctx.scan_levels = False

from scripts import *

ctx.dex_data = load_dex()
ctx.spawn_data = load_spawn()

ctx.assets = TILESETS | SPRITES | OTHER

ctx.load_font("data/fonts/main.ttf", "main", 15)
ctx.labels = {}

wall = [
    [None for i in   range(5)],
    [None, 13, None, None, None],
    [13, None, None, 510,   None],
    [13, 13, 13, None,     13],
    [None, None, 13, None, 13]
]

collection = TilemapCollection(ctx, 32)
collection.add_tilemaps(Tilemap(ctx, 32, 0), Tilemap(ctx, 32, 1))

collection[0].tileset = ctx.assets["main_tileset"]
collection[0].place_pattern([[1 for i in range(ctx.size[0])] for j in range(ctx.size[1])], (0, 0))
collection[0].place_tile(338, (10, 10))
collection[0].place_pattern([[338 for i in range(5)] for i in range(5)], (0, 0), 0)
collection[0].set_animation_tile(338, 0.1, [338, 346, 354, 362, 370, 394])

collection[1].tileset = ctx.assets["main_tileset"]
collection[1].place_pattern(wall, (5, 5))
collection[1].place_pattern([[13 for i in range(ctx.size[0]+2)]], (-1, -1))
collection[1].place_pattern([[13 for i in range(ctx.size[0]+2)]], (-1, ctx.size[1]))
collection[1].place_pattern([[13] for i in range(ctx.size[0]+2)], (-1, -1))
collection[1].place_pattern([[13] for i in range(ctx.size[0]+2)], (ctx.size[0], -1))
collection[1].tags.append("#solid")

ctx.player = Player(ctx, [0, 0])
ctx.scene = Scene(ctx)

ctx.scene.link(ctx.player)
collection.link(ctx.scene)

spawn_group(ctx.scene, 1, [400, 400], 2)

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
    ctx.scroll(ctx.player.rect().center, 15)

    if ctx.camera[0] < 0: ctx.camera[0] = 0
    if ctx.camera[1] < 0: ctx.camera[1] = 0
    if ctx.camera[0] + ctx.get_display_size()[0]> ctx.size[0]*32: ctx.camera[0] = ctx.size[0]*32-ctx.get_display_size()[0]
    if ctx.camera[1] + ctx.get_display_size()[1]> ctx.size[1]*32: ctx.camera[1] = ctx.size[1]*32-ctx.get_display_size()[1]

ctx.run(game_loop=game_loop)
