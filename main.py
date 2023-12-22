from engine import *
import pygame

ctx = GameContext((640, 360), pygame.SCALED, False)

GRASS_ID = 1
TILESET = load_sprite("data/images/tilesets/main.png", (32, 32))

wall = [
    [None for i in   range(5)],
    [None, 13, None, 13, None],
    [13, None, None, 13,   13],
    [13, 13, 13, None,     13],
    [None, None, 13, None, 13]
]

background = Tilemap(ctx, 32, 0) 
background.tileset = TILESET
background.place_pattern([[GRASS_ID for i in range(100)] for j in range(100)], (0, 0))
background.place_tile(338, (10, 10))
background.place_pattern([[338 for i in range(5)] for i in range(5)], (0, 0), 0)
background.set_animation_tile(338, 0.1, [338, 346, 354, 362, 370, 394])

collision = Tilemap(ctx, 32, 1)
collision.tileset = TILESET
collision.place_pattern(wall, (5, 5))

class Player(Entity):
    def __init__(self, game, pos, size):
        Entity.__init__(self, game, pos, size, [0, 0], 2)
        self.vel = [2, 2]
    def update(self, scene):
        super().update(scene)
        self.debug_rect()

player = Player(ctx, [0, 0], [32, 32])

scene = Scene()
scene.link(background, collision, player)

def game_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctx.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                ctx.toggle_fullscreen()
    ctx.draw_rect(pygame.Rect((0,0), ctx.get_display_size()), (0,0,0))
    scene.update()
    ctx.set_caption(str(round(ctx.get_fps())))
    ctx.scroll(player.rect().center, 15)

ctx.run(game_loop=game_loop)
