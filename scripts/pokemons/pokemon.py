from engine import *
import random 

class Pokemon(Entity):
    def __init__(self, game, pos, id, speed, randomness):
        self.id = id
        self.speed = speed
        self.randomness = randomness
        Entity.__init__(self, game, pos, (20, 20), (12,17), 2)
        self.collide = True
        self.moving = False
        self.dir = "up"
        self.state = 1
        self.timer = 0
        self.spawn_pos = self.pos.copy()
        self.shiny = True if random.randint(1, self.game.shiney_chance) == 1 else False
        self.asset = self.game.assets['pokemons'][id-1].copy()
        if self.shiny:
            self.set_asset_to_be_shiny()
    
    def set_asset_to_be_shiny(self):
        for x in range(128):
            for y in range(256):
                pxl = self.asset.get_at((x, y))
                self.asset.set_at((x, y), (pxl[1], pxl[2], pxl[0], pxl[3]))

    def update(self, scene):
        self.z_pos = (0.4/(self.game.size[1]*self.game.tile_size))*self.rect().bottom + 1.8
        if self.moving:
            self.timer += self.speed/15
        if self.timer >= 1:
            self.timer = 0
            self.state = not self.state
        Entity.update(self, scene)
        self.basic_ai(self.speed, *self.randomness)
        self.get_image_from_dir()
        if self.on_screen():
            self.render()
        elif distance(self.pos, self.spawn_pos) > 32*8:
            self.pos = self.spawn_pos.copy()

    def get_image_from_dir(self):
        if self.state == 0:
            if self.dir == "up":
                self.image = self.asset.subsurface(pygame.Rect(0, 0, 64, 64))
            if self.dir in ["right", "up-right", "down-right"]:
                self.image = self.asset.subsurface(pygame.Rect(64, 128, 64, 64))
            if self.dir in ["left", "up-left", "down-left"]:
                self.image = self.asset.subsurface(pygame.Rect(64, 0, 64, 64))
            if self.dir == "down":
                self.image = self.asset.subsurface(0, 128, 64, 64)
        if self.state == 1:
            if self.dir == "up":
                self.image = self.asset.subsurface(pygame.Rect(0, 64, 64, 64))
            if self.dir in ["right", "up-right", "down-right"]:
                self.image = self.asset.subsurface(pygame.Rect(64, 128+64, 64, 64))
            if self.dir in ["left", "up-left", "down-left"]:
                self.image = self.asset.subsurface(pygame.Rect(64, 64, 64, 64))
            if self.dir == "down":
                self.image = self.asset.subsurface(0, 128+64, 64, 64)


    def basic_ai(self, speed, moving_prb, turning_prb, stopping_prb):
        if random.randint(0, int(moving_prb*self.game.get_dt())) == 1:
            self.moving = not self.moving
        if random.randint(0, int(turning_prb*self.game.get_dt())) == 1:
            self.dir = ['right', "up", "left", "down", "up-left", "up-right", "down-right", "up-left", "down-left"][random.randint(0, 7)]
        if random.randint(0, int(stopping_prb*self.game.get_dt())) == 1:
            self.moving = False
        if self.collisions['left'] != []:
            self.dir = ["right", "down-right", "up-right"][random.randint(0,2)]
        if self.collisions['right'] != []:
            self.dir = ["left", "down-left", "up-left"][random.randint(0,2)]
        if self.collisions["up"] != []:
            self.dir = ["down", "down-left", "down-right"][random.randint(0,2)]
        if self.collisions["down"] != []:
            self.dir =  ["up", "up-left", "up-right"][random.randint(0,2)]
        if self.moving:
            self.vel = {"up" : [0, -speed], "down" : [0, speed], "left" : [-speed, 0], "right" : [speed, 0], "up-left" : [-speed/1.4, -speed/1.4], "up-right" : [speed/1.4, -speed/1.4], "down-left" : [-speed/1.4, speed/1.4], "down-right" : [speed/1.4, speed/1.4]}[self.dir]
        else:
            self.vel = [0, 0]
        