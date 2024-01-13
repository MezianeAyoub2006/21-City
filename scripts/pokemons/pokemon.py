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
        self.seen = True
        if game.labels == {}: generate_labels(game)
        self.aggressive = False
        self.focus = 2
        self.stay = False
        self.fairy = fairy
        self.shiny = True if random.randint(1, self.game.shiney_chance) == 1 else False
        self.tags.append("@pokemon")
        if self.shiny: self.tags.append("#shiny")
        self.dir = ['right', "up", "left", "down", "up-left", "up-right", "down-right", "up-left", "down-left"][random.randint(0, 7)]
        self.state = 1
        self.timer = 0
        self.time = 0.3
        self.toggle_player = None
        self.spawn_pos = self.pos.copy()
        self.asset = self.game.assets['pokemons'][id-1].copy()
        self.speed = max(0.4, self.get_stat("Speed")/50)
        self.ac_speed = self.speed
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
        self.max_life = self.get_stat("HP")
        self.life = self.max_life
        if self.shiny: self.set_asset_to_be_shiny()
        self.types = self.get_data()["type"]
    
    def set_asset_to_be_shiny(self): 
        for x in range(128):
            for y in range(256):
                pxl = self.asset.get_at((x, y))
                self.asset.set_at((x, y), (pxl[1], pxl[2], pxl[0], pxl[3]))
    
    def goto(self, pos, escape=False, factor=1.2): 
        if distance(self.pos, pos) >= 15:
            target_vector = pygame.math.Vector2(pos[0] - self.pos[0], pos[1] - self.pos[1])
            target_vector.normalize_ip()
            velocity = target_vector * self.ac_speed
            velocity *= factor
            if escape:
                velocity *= -1
            self.vel = [velocity.x, velocity.y]
            self.dir = direction(self.vel)
    
    def stay_goto(self, pos, escape, factor):
        if self.time <= 0.3:
            self.time -= self.game.get_dt()*(1/60)
        self.stay = pos
        if self.time < 0:
            self.stay = False
            self.time = 0.3
        else:
            self.goto(self.stay, escape, factor)

    def get_stat(self, stat):
        return self.game.dex_data[self.id-1]["base"][stat]

    def get_data(self):
        return self.game.dex_data[self.id-1]

    def scene_init(self, scene):
        scene.link(Swim(self.game, self, 1.1, (-10, 3)))

    def update(self, scene):
        try:
            player = self.game.scenes[self.game.index].get_objects_by_tag("@player")[0]
        except:
            player = Entity(self.game, [0, 0], [0, 0], [0, 0], 0)
        self.z_pos = ((1/(self.game.size[1]*self.game.tile_size))*self.rect().bottom + 2)
        if self.focus <= 0:
            if self.stay == False:
                self.vel = [0, 0]
            if random.randint(0, 120) == 1:
                self.focus = random.randint(20, 50)/10
        if (self.moving or self.aggressive or self.fairy) and not self.vel == [0, 0]:
            self.timer += (self.speed/10)*self.game.get_dt()
        if self.timer >= 1:
            self.timer = 0
            self.state = not self.state
        if distance(self.pos, player.rect().center) <= 32*6:
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
            if self.stay == False:
                if self.fairy:
                    self.goto(player.rect().center, True)
                if self.aggressive:
                    if self.focus > 0:
                        self.goto([player.rect().centerx-20, player.rect().centery-20])
                        self.focus -= (1/60) * self.game.get_dt()
        if self.rect().colliderect(player.attack_rect) or self.stay:  
            if self.stay == False:
                self.toggle_player = player.rect().center  
            self.stay_goto(self.toggle_player, True, self.game.items[player.attack]["knockback"])

        self.render_label()
        
    def render_label(self):
        self.game.render(self.game.labels[self.level], [self.pos[0]+5, self.pos[1] - min(float(self.get_data()["profile"]["height"].split(" ")[0])*15 + 10, 40)])
        life_pos = [self.pos[0]+5, self.pos[1] - min(float(self.get_data()["profile"]["height"].split(" ")[0])*15 - 10, 40)]
        self.game.render_rect(pygame.rect.Rect(life_pos, (29, 6)), (0, 0, 0))
        self.game.render_rect(pygame.rect.Rect((life_pos[0]+1, life_pos[1]+1), (30*(self.life/self.max_life)-3, 3)), (255, 0, 0))

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
        