from engine import *
from scripts.player.shadow import *

class Player(Entity, Animated):

    def __init__(self, game, pos):
        Entity.__init__(self, game, pos, [24, 16], [10, 24], 2)
        self.speed = 3
        Animated.__init__(self, game.assets["player_walk_cycle"])
        self.collide = True
        self.flip = False

    def scene_init(self, scene):
        scene.link(Shadow(self.game, self, 1.1, (-10, -2)))

    def update(self, scene):
        self.z_pos = ((1/(self.game.size[1]*self.game.tile_size))*self.rect().bottom + 2)
        keys = pygame.key.get_pressed()
        Entity.update(self, scene)
        self.stop = False
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]) or (keys[pygame.K_UP] and keys[pygame.K_DOWN]):
            self.stop = True
        elif (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and keys[pygame.K_LEFT]:
            self.set_animation(1)
            self.dir = "left"
            self.flip = False
        elif (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and keys[pygame.K_RIGHT]:
            self.set_animation(1)
            self.dir = "right"
            self.flip = True
        elif keys[pygame.K_UP]:
            self.dir = "up"
            self.set_animation(0)
        elif keys[pygame.K_DOWN]:
            self.dir = "down"
            self.set_animation(2)
        elif keys[pygame.K_LEFT]:
            self.dir = "left"
            self.set_animation(1)
            self.flip = False
        elif keys[pygame.K_RIGHT]:
            self.dir = "right"
            self.set_animation(1)
            self.flip = True
       
        self.vel = [(int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]))*self.speed,(int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))*self.speed]
        if self.stop : self.vel = [0, 0]
        if abs(self.vel[0]) == abs(self.vel[1]) != 0:
            self.vel[0] *= (1/1.4)
            self.vel[1] *= (1/1.4)
        if (keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP]) and not self.stop:
            self.animate(self.game.get_dt())
        else:
            self.set_animation_cursor(2)
        self.render()
    
    def render(self):
        self.flip_image(self.flip, False)
        super().render()