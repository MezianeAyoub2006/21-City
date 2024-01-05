from engine import *
import pygame

# on définit un raccourcit vers le chemin des images
set_path("data/images/")

# création du contexte de jeu
ctx = GameContext((640, 360), pygame.SCALED | pygame.RESIZABLE, True)

# chargement des données 
ctx.tile_size = 32
ctx.size = [25, 25]
ctx.shiney_chance = 4096
ctx.scan_levels = False
from scripts import *
ctx.dex_data = load_dex()
ctx.spawn_data = load_spawn()
ctx.assets = TILESETS | SPRITES | OTHER
ctx.load_font("data/fonts/main.ttf", "main", 15)
ctx.labels = {}

#création du joueur et de la scène
ctx.player = Player(ctx, [30, 30])
ctx.scene = Scene(ctx)

collection = generate_biome_collection(ctx, ctx.size, 32, 0, 5)
collection.link(ctx.scene)

ctx.scene.link(ctx.player)

spawn_group(ctx.scene, 0, [400, 400], 2)

def game_loop():
    # evénements 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctx.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                ctx.toggle_fullscreen()

    # boucle du jeu
    ctx.draw_rect(pygame.Rect((0,0), ctx.get_display_size()), (0,0,0))
    ctx.scene.update()
    ctx.set_caption(str(round(ctx.get_fps())))
    ctx.scroll(ctx.player.rect().center, 15)

    # ajustement de la caméra pour qu'elle ne dépasse pas les limites de la carte
    if ctx.camera[0] < 0: ctx.camera[0] = 0
    if ctx.camera[1] < 0: ctx.camera[1] = 0
    if ctx.camera[0] + ctx.get_display_size()[0]> ctx.size[0]*32: ctx.camera[0] = ctx.size[0]*32-ctx.get_display_size()[0]
    if ctx.camera[1] + ctx.get_display_size()[1]> ctx.size[1]*32: ctx.camera[1] = ctx.size[1]*32-ctx.get_display_size()[1]

ctx.run(game_loop=game_loop)

#salut