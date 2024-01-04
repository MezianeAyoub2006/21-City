from engine import *
from scripts.utils import *
from scripts.player.shadow import *
import random, pygame

def generate_labels(game):
    for i in range(1, 101):
        game.labels[i] = game.render_text(f"Lv. {i}", "main15", [0, 0])

class Pokemon(Entity):
    def __init__(self, game, pos, id, level, z_pos, fairy=False, aggressive=False):
        self.id = id
        Entity.__init__(self, game, pos, (20, 20), (12,17), z_pos)
        self.collide = True
        self.moving = False
        self.move_by_itself = True
        self.seen = False
        if game.labels == {}: generate_labels(game)
        self.aggressive = aggressive
        self.fairy = fairy
        self.shiny = True if random.randint(1, self.game.shiney_chance) == 1 else False
        self.tags.append("@pokemon")
        if self.shiny: self.tags.append("#shiny")
        self.dir = ['right', "up", "left", "down", "up-left", "up-right", "down-right", "up-left", "down-left"][random.randint(0, 7)]
        self.state = 1
        self.timer = 0
        self.spawn_pos = self.pos.copy()
        self.asset = self.game.assets['pokemons'][id-1].copy()
        self.speed = max(0.4, self.get_stat("Speed")/50)
        self.level = level
        self.randomness = (
            (1/self.get_stat("Attack"))*5000, 
            (1/self.get_stat("Sp. Attack"))*8000, 
            mean(
                self.get_stat("HP"), 
                self.get_stat("Defense"), 
                self.get_stat("Sp. Defense")
                )
        )
        if self.shiny: self.set_asset_to_be_shiny()
    
    def set_asset_to_be_shiny(self): 
        for x in range(128):
            for y in range(256):
                pxl = self.asset.get_at((x, y))
                self.asset.set_at((x, y), (pxl[1], pxl[2], pxl[0], pxl[3]))
    
    def goto(self, pos, escape=False): 
        if distance(pos, self.pos) <= 32:
            return
        target_vector = pygame.math.Vector2(pos[0] - self.pos[0], pos[1] - self.pos[1])
        target_vector.normalize_ip()
        velocity = target_vector * self.speed
        if escape:
            velocity = -velocity
        velocity *= 1.5
        self.vel = [velocity.x, velocity.y]
        self.dir = direction(self.vel)

    def get_stat(self, stat):
        return self.game.dex_data[self.id-1]["base"][stat]

    def get_data(self):
        return self.game.dex_data[self.id-1]

    def update(self, scene):
        self.z_pos = ((1/(self.game.size[1]*self.game.tile_size))*self.rect().bottom + 2)
        if self.moving or self.aggressive or self.fairy:
            self.timer += (self.speed/10)*self.game.get_dt()
        if self.timer >= 1:
            self.timer = 0
            self.state = not self.state
        if distance(self.pos, self.game.player.rect().center) <= 32*6:
            self.seen = True
        Entity.update(self, scene)
        if not (self.fairy and self.seen) and not (self.aggressive and self.seen) and self.move_by_itself:
            self.basic_ai(self.speed, *self.randomness)
        self.get_image_from_dir()
        if self.on_screen():
            self.render()
        elif self.fairy and self.seen:
            self.kill()
        if self.fairy and self.seen and (self.rect().centerx <= 10 or self.rect().centery <= 10):
            self.kill()
        if self.seen:
            if self.fairy:
                self.goto(self.game.player.rect().center, True)
            if self.aggressive:
                self.goto([self.game.player.rect().centerx-20, self.game.player.rect().centery-20])
        
    def render_label(self):
        self.game.render(self.game.labels[self.level], [self.pos[0]+5, self.pos[1] - min(float(self.get_data()["profile"]["height"].split(" ")[0])*15 + 5, 20)])

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
        if random.randint(0, int(moving_prb/self.game.get_dt())) == 1:
            self.moving = not self.moving
        if random.randint(0, int(turning_prb/self.game.get_dt())) == 1:
            self.dir = ['right', "up", "left", "down", "up-left", "up-right", "down-right", "up-left", "down-left"][random.randint(0, 7)]
        if random.randint(0, int(stopping_prb/self.game.get_dt())) == 1:
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
        