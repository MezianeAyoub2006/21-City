from engine import *
import pygame, os, json, time, pyperclip
from math import *
from random import *

with open("test.json", "r") as f: 
    data = json.load(f)

set_path("data/images/")

ctx = GameContext((640*(3/4), 360), pygame.SCALED, True)

ctx.tile_size = 32
ctx.size = [25, 25]
ctx.shiney_chance = 4096
ctx.transit = False
ctx.debug = False
ctx.looped = False
ctx.debug_code = ""
ctx.scan_levels = False
ctx.pause = False
ctx.transition_count = 0
ctx.acceleration = 1
ctx.debug_show = False
ctx.variables = {}
ctx.loop_variable = None
ctx.loop_count = (0,)
ctx.transition_data = None

from scripts import *

ctx.dex_data = load_dex()
ctx.spawn_data = load_spawn()
ctx.biomes_data = load_biomes()
ctx.assets = TILESETS | SPRITES | OTHER | MENU | ATTACKS
for i in range(1, 61):
    ctx.load_font("data/fonts/main.ttf", "main", i)
ctx.pause_timer = 0


def init(state, biome, player_level, player_inventory, player_clip=True, player_speed=3):
    global menu
    ctx.scroll_ = [0, 0]
    ctx.camera = [0, 0]
    ctx.labels = {}
    ctx.battle = None
    ctx.state = state
    ctx.items = ITEMS
    player = Player(ctx, [12*32, 12*32], "down", 100, player_level, list(map(lambda x : x if x != [] else None, player_inventory)), speed=player_speed, collide=player_clip)
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
    ctx.dt *= ctx.acceleration
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
                pygame.display.toggle_fullscreen()
            if player.switch:
                if event.key == pygame.K_v:
                    if pygame.key.get_pressed()[pygame.K_LCTRL] and len(ctx.debug_code) + len(pyperclip.paste()) <= 130:
                        ctx.debug_code += pyperclip.paste()
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
                if event.key == pygame.K_RETURN:
                    if ctx.debug_code == "DEBUG_MODE":
                        ctx.debug = not ctx.debug
                    elif ctx.debug:
                        command = ctx.debug_code.split()
                        if ctx.loop_variable != None:
                            loop_count = ctx.loop_count
                            ctx.looped = True 
                        else:
                            loop_count = (1,)
                        for i in range(*loop_count):
                            ctx.variables[ctx.loop_variable] = i
                            if ctx.loop_variable != None:
                                print(ctx.variables)
                            if command != "":
                                if ctx.debug_code[:10] == "/inventory":      
                                    cmd = ctx.debug_code.split(" ", 1)
                                    try: player.inventory = eval(cmd[1], ctx.variables|globals())
                                    except: pass
                                if ctx.debug_code[:7] == "/define":
                                    cmd = ctx.debug_code[8:].split(" ", 1)
                                    try: ctx.variables[cmd[0]] = eval(cmd[1], ctx.variables|globals())
                                    except: pass
                            if len(command) == 1:
                                if command[0] == "/default":
                                    player.life = 100
                                    player.collide = True
                                    ctx.debug_show = False
                                    player.speed = 3
                                    ctx.acceleration = 1
                                    ctx.loop_variable = None
                                    ctx.loop_count = (0,)
                                if command[0] == "/heal":
                                    player.life = 100
                                if command[0] == "/clip":
                                    player.collide = not player.collide
                                if command[0] == "/kill":
                                    player.life = 0
                                if command[0] == "/debug":
                                    ctx.debug_show = not ctx.debug_show
                            if len(command) == 2:
                                if command[0] == "/portal":
                                    try: ctx.scenes[ctx.index].link(Portal(ctx, [player.pos[0] - 70, player.pos[1] - 60], {0:0, 1:1, 2:2, 3:6, 4:5}[int(eval(command[1], ctx.variables|globals()))], 1.05))
                                    except: pass
                                if command[0] == "/speed":
                                    try: player.speed = float(eval(command[1], ctx.variables|globals()))
                                    except: pass
                                if command[0] == "/life":
                                    try: player.life = int(eval(command[1], ctx.variables|globals()))
                                    except: pass
                                if command[0] == "/level":
                                    try: player.level = int(eval(command[1], ctx.variables|globals()))
                                    except: pass
                                if command[0] == "/tick":
                                    try: ctx.acceleration = float(eval(command[1], ctx.variables|globals()))
                                    except: pass
                            if len(command) == 3:
                                if command[0] == "/tp":
                                    try: player.pos = [eval(command[1], ctx.variables|globals())*32, eval(command[2], ctx.variables|globals())*32]
                                    except: pass
                                if command[0] == "/give":
                                    try: 
                                        for j, item in enumerate(player.inventory):
                                            if item == None:
                                                player.inventory[j] = (int(eval(command[1], ctx.variables|globals())), int(eval(command[2], ctx.variables|globals())))
                                                break
                                            if item[0] == int(eval(command[1])):
                                                player.inventory[j] = (player.inventory[j][0], player.inventory[j][1]+int(eval(command[2], ctx.variables|globals())))
                                                break
                                    except: 
                                        pass
                            if len(command) == 5:
                                if command[0] == "/spawn":
                                    try: spawn_pokemon(ctx.scenes[ctx.index], int(eval(command[1], ctx.variables|globals())), [int(eval(command[3], ctx.variables|globals()))*32, int(eval(command[4], ctx.variables|globals()))*32], int(eval(command[2], ctx.variables|globals())), 2)
                                    except: pass
                                if command[0] == "/loop":
                                    try: 
                                        int(command[1])
                                    except: 
                                        ctx.loop_variable = command[1]
                                        ctx.loop_count = (eval(command[2],ctx.variables|globals()), eval(command[3],ctx.variables|globals()), eval(command[4],ctx.variables|globals()))
                    ctx.debug_code = ""
                    if ctx.looped:
                        if ctx.loop_variable in ctx.variables:
                            del ctx.variables[ctx.loop_variable]
                        ctx.loop_variable = None
                        ctx.looped = False
                if event.key == pygame.K_BACKSPACE:
                    if ctx.pause:
                        ctx.debug_code = ctx.debug_code[:len(ctx.debug_code)-1]
                    else:   
                        player.inventory[player.item_chosen] = None
                        if player.inventory == [None, None, None]:
                            player.inventory[0] = (0, 1)
                elif ctx.pause and not (pygame.key.get_pressed()[pygame.K_LSHIFT] and pygame.key.get_pressed()[pygame.K_p]) and event.unicode in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789&é\"'(-è_çà)=+#{[|\\^@]}^$ù*,;:!?./§£%µ<> ":
                    if len(ctx.debug_code) <= 130:
                        ctx.debug_code += event.unicode             
                if event.key == pygame.K_p and ctx.state == 0:
                    if ctx.debug:
                        if ctx.pause:
                            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                                ctx.pause = not ctx.pause
                                ctx.debug_code = ""
                        else:
                            ctx.pause = not ctx.pause
                            ctx.debug_code = ""
                    else:
                        ctx.debug_code = ""
                        ctx.pause = not ctx.pause
            if event.key == pygame.K_SPACE:
                ctx.space = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            ctx.mouse_pressed = True

    ctx.draw_rect(pygame.Rect((0,0), ctx.get_display_size()), (0,0,0))
    pygame.display.set_caption("Pokemon SLASH | FPS : "+str(round(ctx.get_fps())), "logo.png")

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

    pygame.display.set_icon(pygame.image.load("logo.png"))

    if ctx.pause_timer > 0:
        ctx.screen.blit(srf, (0, 0))
        ctx.draw_text("PAUSE", "main60", [5, -55+ctx.pause_timer*60], (255,255,255))
        if ctx.debug:
            ctx.draw_text(ctx.debug_code+("|" if math.floor(time.time()*2.5)%2==0 else ""), "main"+str(int(min(40, 1270/(len(ctx.debug_code)+1)))), [5, 372-ctx.pause_timer*60+len(ctx.debug_code)/8], (255,255,255))

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
