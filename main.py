from engine import *
import pygame, os, json 

with open("test.json", "r") as f:
    data = json.load(f)

# on définit un raccourcit vers le chemin des images
set_path("data/images/")

ctx = GameContext((640, 360), pygame.SCALED | pygame.RESIZABLE, True)

ctx.tile_size = 32
ctx.size = [25, 25]
ctx.shiney_chance = 4096
ctx.scan_levels = False

from scripts import *

ctx.dex_data = load_dex()
ctx.spawn_data = load_spawn()
ctx.biomes_data = load_biomes()
ctx.assets = TILESETS | SPRITES | OTHER | MENU | ATTACKS
ctx.load_font("data/fonts/main.ttf", "main", 15)
ctx.load_font("data/fonts/main.ttf", "main", 30)
ctx.labels = {}
ctx.battle = None
ctx.state = 1
ctx.items = ITEMS

player = Player(ctx, [30, 30], "down", 100, data["player_level"], data["player_inventory"])
ctx.biome = data["biome"]
ctx.scenes = generate_room(ctx, ctx.biome)
ctx.index = (0, 0)
ctx.scenes[(0, 0)].link(player, Shadow(ctx, player, 1.1, (-10, -2)), Swim(ctx, player, 1.1, (-10, 3))) 
ctx.space = False

menu = Menu(ctx)

def game_loop(): 
    try:
        player = ctx.scenes[ctx.index].get_objects_by_tag("@player")[0]
    except:
        player = Entity(ctx, [0, 0], [0, 0], [0, 0], 0)
    ctx.mouse_pressed = False
    ctx.space = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctx.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                ctx.toggle_fullscreen()
            if player.switch:
                if event.key == pygame.K_1:
                    player.item_chosen = 0
                if event.key == pygame.K_2:
                    player.item_chosen = 1
                if event.key == pygame.K_3:
                    player.item_chosen = 2
                if event.key == pygame.K_4:
                    player.item_chosen = 3
                if event.key == pygame.K_5:
                    player.item_chosen = 4
                if event.key == pygame.K_BACKSPACE:
                    player.inventory[player.item_chosen] = None
                    if player.inventory == [None, None, None, None, None]:
                        player.inventory[0] = (0, 1)
            if event.key == pygame.K_SPACE:
                ctx.space = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            ctx.mouse_pressed = True

    ctx.draw_rect(pygame.Rect((0,0), ctx.get_display_size()), (0,0,0))
    ctx.set_caption(str(round(ctx.get_fps())))

    if ctx.state == 0: 
        ctx.scenes[ctx.index].update()
        ctx.scroll(player.rect().center, 15)
        player.inventory_()

    if ctx.state == 1: 
        menu.update()

    if ctx.camera[0] < 0: ctx.camera[0] = 0
    if ctx.camera[1] < 0: ctx.camera[1] = 0
    if ctx.camera[0] + ctx.get_display_size()[0]> ctx.size[0]*32: ctx.camera[0] = ctx.size[0]*32-ctx.get_display_size()[0]
    if ctx.camera[1] + ctx.get_display_size()[1]> ctx.size[1]*32: ctx.camera[1] = ctx.size[1]*32-ctx.get_display_size()[1]

ctx.run(game_loop=game_loop)

