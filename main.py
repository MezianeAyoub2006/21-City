from engine import *
import pygame, os, json 

with open("test.json", "r") as f: 
    data = json.load(f)

set_path("data/images/")

ctx = GameContext((640*(3/4), 360), pygame.SCALED | pygame.RESIZABLE, True)

ctx.tile_size = 32
ctx.size = [25, 25]
ctx.shiney_chance = 4096
ctx.transit = False
ctx.scan_levels = False
ctx.pause = False
ctx.transition_count = 0
ctx.transition_data = None

from scripts import *

ctx.dex_data = load_dex()
ctx.spawn_data = load_spawn()
ctx.biomes_data = load_biomes()
ctx.assets = TILESETS | SPRITES | OTHER | MENU | ATTACKS
ctx.load_font("data/fonts/main.ttf", "main", 15)
ctx.load_font("data/fonts/main.ttf", "main", 30)
ctx.load_font("data/fonts/main.ttf", "main", 60)
ctx.pause_timer = 0


def init(state, biome, player_level, player_inventory):
    global menu
    ctx.scroll_ = [0, 0]
    ctx.camera = [0, 0]
    ctx.labels = {}
    ctx.battle = None
    ctx.state = state
    ctx.items = ITEMS
    player = Player(ctx, [12*32, 12*32], "down", 100, player_level, list(map(lambda x : x if x != [] else None, player_inventory)))
    ctx.biome = biome
    ctx.scenes = generate_room(ctx, biome)
    ctx.index = (0, 0)
    ctx.scenes[(0, 0)].link(player, Shadow(ctx, player, 1.1, (-10, -2)), Swim(ctx, player, 1.1, (-10, 3))) 
    ctx.space = False
    if state == 1:
        menu = Menu(ctx) 
    for i in range(200):
        ctx.scroll(player.rect().center, 15)

ctx.init = init
ctx.init(1, data["biome"], data["player_level"], data["player_inventory"])


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
                if event.key == pygame.K_p and ctx.state == 0:
                    ctx.pause = not ctx.pause
                if event.key == pygame.K_1:
                    player.item_chosen = 0
                if event.key == pygame.K_2:
                    player.item_chosen = 1
                if event.key == pygame.K_3:
                    player.item_chosen = 2
                if event.key == pygame.K_SPACE:
                    if not ctx.pause and ctx.transition_count == 0:
                        if player.inventory[player.item_chosen] != None:
                            if player.inventory[player.item_chosen][0] == 7:
                                player.inventory[player.item_chosen] = (player.inventory[player.item_chosen][0], player.inventory[player.item_chosen][1]-1)
                                player.life = player.max_life
                if event.key == pygame.K_BACKSPACE:
                    player.inventory[player.item_chosen] = None
                    if player.inventory == [None, None, None]:
                        player.inventory[0] = (0, 1)
            if event.key == pygame.K_SPACE:
                ctx.space = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            ctx.mouse_pressed = True

    ctx.draw_rect(pygame.Rect((0,0), ctx.get_display_size()), (0,0,0))
    ctx.set_caption("Pokemon SLASH | FPS : "+str(round(ctx.get_fps())))

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

    if ctx.pause:
        if ctx.pause_timer == 0:
            ctx.pause_timer = 0.1
    
    if ctx.pause_timer > 0 and ctx.pause_timer < 0.8 and ctx.pause:
        ctx.pause_timer += ctx.get_dt()/40
    
    if ctx.pause_timer > 0 and not ctx.pause:
        ctx.pause_timer -= ctx.get_dt()/40
        if ctx.pause_timer < 0:
            ctx.pause_timer = 0
    
    srf = pygame.Surface((640*(3/4), 360))
    srf.fill((0, 0, 0))
    srf.set_alpha(234*(ctx.pause_timer))

    if ctx.pause_timer > 0:
        ctx.screen.blit(srf, (0, 0))
        ctx.draw_text("PAUSE", "main60", [5, -55+ctx.pause_timer*60], (255,255,255))

    if ctx.transition_count > 0:
        ctx.transition_count += ctx.get_dt()/45
        if ctx.transition_count >= 4:
            ctx.transition_count = 0
            ctx.transit = False
        srf = pygame.Surface((640*(3/4), 360))
        srf.fill((0, 0, 0))
        srf.set_alpha(min(400*(ctx.transition_count/2), 255) if ctx.transition_count < 2 else min(400*((4-ctx.transition_count)/2), 255))
        if ctx.transition_count > 2:
            if not ctx.transit:
                ctx.init(*ctx.transition_data)
                ctx.transit = False
                ctx.transit = True
        ctx.screen.blit(srf, (0, 0))

ctx.run(game_loop=game_loop)
