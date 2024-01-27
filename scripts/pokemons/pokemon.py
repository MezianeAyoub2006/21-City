from engine import *
from scripts.utils import *
from scripts.player.shadow import *
import random, pygame

def generate_labels(game):
    for i in range(1, 200):
        game.labels[i] = game.render_text(f"Lv. {i}", "main15", [0, 0])

class Attack(Entity):
    def __init__(self, pokemon, game, type, speed, damage, look, bounce=0):
        Entity.__init__(self, game, (0, 0), (8, 8), (0, 0), pokemon.z_pos+0.05)
        self.pos = pokemon.pos.copy()
        self.type = type
        self.speed = speed
        self.damage = damage
        self.collide = True
        self.bounce = bounce
        self.pos = list(pokemon.rect().center)
        self.look = look
        try: player = self.game.scenes[self.game.index].get_objects_by_tag("@player")[0]
        except: player = Entity(self.game, [0, 0], [0, 0], [0, 0], 0)
        if self.type == 0:
            target = player.pos.copy()
            self.vector = pygame.math.Vector2(target[0] - self.pos[0], target[1] - self.pos[1])
            self.vector.normalize_ip()
            self.vector *= self.speed
        if type == 2:
            dirs = {'right' : (1, 0), "up" : (0, -1), "left" : (-1, 0), "down": (0, 1), "up-left": (-1/1.4, -1/1.4), "up-right": (1/1.4, -1/1.4), "down-right": (1/1.4, 1/1.4), "down-left": (-1/1.4, 1/1.4)}
            self.vector = pygame.Vector2(*(i*self.speed for i in dirs[pokemon.dir]))
        if type == 1:
            self.angle = random.randint(0, 360)
            self.vector = pygame.math.Vector2(1, 0)
            self.vector.rotate_ip(self.angle)
            self.vector *= self.speed
        self.vector.rotate_ip(random.randint(-15, 15))
    def update(self, scene):
        if not self.game.pause:
            try:
                player = self.game.scenes[self.game.index].get_objects_by_tag("@player")[0]
            except:
                player = Entity(self.game, [0, 0], [0, 0], [0, 0], 0)
            if self.rect().colliderect(player.rect()):
                player.life -= (self.damage/player.level)*20
                self.kill()
                return
            if self.type == 0 or self.type == 1 or self.type == 2:
                self.vel[0] = self.vector.x
                self.vel[1] = self.vector.y
            self.image = self.game.assets["pokemon_attack0"][0] if self.look == 0 else self.game.assets["pokemon_attack1"][0]
            super().update(scene)
            collide = False
            for i in self.collisions.values():
                if i != []:
                    collide = True
            if collide:
                if self.bounce == 0:
                    self.kill()
                else:
                    if self.collisions["left"] != [] or self.collisions["right"] != []:
                        self.vector.x *= -1
                    if self.collisions["up"] != [] or self.collisions["down"] != []:
                        self.vector.y *= -1
                    self.bounce -= 1

        super().render()

class Portal(GameObject):
    def __init__(self, game, pos, id, z_pos):
        GameObject.__init__(self, game, z_pos)
        self.pos = pos
        self.id = id
        self.count = 0
        self.rect = pygame.Rect(self.pos[0]+70, self.pos[1]+30, 50, 120)
    
    def update(self, scene):
        self.count += self.game.get_dt()/10
        try:
            player = self.game.scenes[self.game.index].get_objects_by_tag("@player")[0]
        except:
            player = Entity(self.game, [0, 0], [0, 0], [0, 0], 0)
        if player.rect().colliderect(self.rect) and pygame.key.get_pressed()[pygame.K_e] and self.game.transition_count == 0:
            self.game.transition_count = 0.1
            self.game.transition_data = (0, {0:1, 1:2, 2:6, 5:4, 6:5}[self.game.biome], player.level, player.inventory)
        try:
            self.game.render(self.game.assets["portal"][int(self.count)], self.pos)
        except IndexError:
            self.count = 0
            self.game.render(self.game.assets["portal"][int(self.count)], self.pos)
        
class Pokemon(Entity):
    def __init__(self, game, pos, id, level, z_pos, fairy=False, aggressive=False):
        self.id = id
        self.attack_timer = 0
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
        self.damage_couldown = -1
        if self.id in [60, 59, 58, 57, 56, 55]:
            if self.game.biome == 0:
                self.timey = 0.075
            if self.game.biome == 1:
                self.timey = 0.2
            if self.game.biome == 2:
                self.timey = 0.18
            if self.game.biome == 6:
                self.timey = 0.04
            if self.game.biome == 5:
                self.timey = 0.001
        else:
            self.timey = 0.2
            if self.game.biome == 6:
                self.timey = 0.1 
            if self.game.biome == 0:
                self.timey = 0.075
    
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
        self.swimmer = Swim(self.game, self, 1.1, (-10, 3))
        scene.link(self.swimmer)

    def deal_damage(self, damage, player):
        if random.randint(0, 10) == 4:
            return (((damage/self.get_stat("Defense")))*20*(((player.level/self.level)/2)*0.15)*(2 if self.id in [60, 59, 58, 57, 56, 55] else 7))*5
        else:
            return (((damage/self.get_stat("Defense")))*20*(((player.level/self.level)/2)*0.15)*(2 if self.id in [60, 59, 58, 57, 56, 55] else 7))

    def update(self, scene):
        if not self.game.pause:
            self.attack_timer += (1/60) * self.game.get_dt()
            if self.attack_timer >= self.timey:
                self.attack_timer = 0
                if self.aggressive and self.vel == [0, 0]:
                    if self.game.biome == 0:
                        scene.link(Attack(self, self.game, 1, (self.get_stat("Sp. Attack")*8)/(5*50), (self.get_stat("Sp. Attack")*self.level*1.5)/(5*50), 0))
                    elif self.game.biome == 1:
                        scene.link(Attack(self, self.game, 0, (self.get_stat("Sp. Attack")*9)/(5*50), (self.get_stat("Sp. Attack")*self.level*1.5)/(5*50), 0))
                    elif self.game.biome == 2:
                        scene.link(Attack(self, self.game, 2, (self.get_stat("Sp. Attack")*10.5*(1.5 if self.id in [60, 59, 58, 57, 56, 55] else 1))/(5*50), (self.get_stat("Sp. Attack")*self.level*1.5)/(5*50), 0))
                    elif self.game.biome == 6:
                        scene.link(Attack(self, self.game, 1, (self.get_stat("Sp. Attack")*9*(0.7 if self.id in [60, 59, 58, 57, 56, 55] else 1))/(5*50), (self.get_stat("Sp. Attack")*self.level*2)/(5*50), 0, 1 if self.id in [60, 59, 58, 57, 56, 55] else 0))
                    elif self.game.biome == 5:
                        scene.link(Attack(self, self.game, 0, (self.get_stat("Sp. Attack")*8.35)/(5*50), (self.get_stat("Sp. Attack")*self.level*(0.8 if self.id in [60, 59, 58, 57, 56, 55] else 1.5))/(5*50), 0, 0))

            Entity.update(self, scene)
            if self.pos[0] < 0 or self.pos[1] < 0 or self.pos[0] > 25 * 32 or self.pos[1] > 25 * 32:
                self.pos = self.spawn_pos.copy()
                self.stay = False
            else:
                self.stay = False
            try:
                player = self.game.scenes[self.game.index].get_objects_by_tag("@player")[0]
            except:
                player = Entity(self.game, [0, 0], [0, 0], [0, 0], 0)
            self.z_pos = ((1/(self.game.size[1]*self.game.tile_size))*self.rect().bottom + 2)
            if self.life <= 0:
                self.kill()
                self.swimmer.kill()
                if self.id in [60, 59, 58, 57, 56, 55]:
                    scene.link(Portal(self.game, [self.pos[0] - 40, self.pos[1] - 60], 0, 1.05))
                player.xp += self.level * (sum(self.get_stat(i) for i in ["Attack", "Sp. Attack", "Sp. Defense", "Defense", "Speed", "HP"]))/75
                if self.game.biome == 0:
                    if random.randint(0, 10) == 5:
                        for i, item in enumerate(player.inventory):
                            if item == None:
                                player.inventory[i] = (1, 1)
                                break
                            if item[0] == 1:
                                player.inventory[i] = (player.inventory[i][0], player.inventory[i][1]+1)
                                break
                if self.game.biome == 1:
                    if random.randint(0, 10) == 5:
                        for i, item in enumerate(player.inventory):
                            if item == None:
                                player.inventory[i] = (2, 1)
                                break
                            if item[0] == 2:
                                player.inventory[i] = (player.inventory[i][0], player.inventory[i][1]+1)
                                break
                if self.game.biome == 6:
                    if random.randint(0, 10) == 5:
                        for i, item in enumerate(player.inventory):
                            if item == None:
                                player.inventory[i] = (3, 1)
                                break
                            if item[0] == 3:
                                player.inventory[i] = (player.inventory[i][0], player.inventory[i][1]+1)
                                break
                if random.randint(0, 10) == 5:
                        for i, item in enumerate(player.inventory):
                            if item == None:
                                player.inventory[i] = (7, 1)
                                break
                            if item[0] == 7:
                                player.inventory[i] = (player.inventory[i][0], player.inventory[i][1]+1)
                                break
            if self.life > self.max_life:
                self.life = self.max_life
            if self.focus <= 0:
                if self.damage_couldown <= 0:
                    self.life += self.game.get_dt()/60
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
            if not (self.fairy and self.seen) and not (self.aggressive and self.seen) and self.move_by_itself:
                self.basic_ai(self.speed, *self.randomness)
            self.get_image_from_dir()
            if self.fairy and self.seen and (self.rect().centerx <= 10 or self.rect().centery <= 10):
                self.kill()
                self.swimmer.kill()
            if self.seen:
                if self.stay == False:
                    if self.fairy:
                        self.goto(player.rect().center, True)
                    if self.aggressive:
                        if self.focus > 0:
                            self.goto([player.rect().centerx-20, player.rect().centery-20])
                            self.focus -= (1/60) * self.game.get_dt()
            if self.rect().colliderect(player.attack_rect) or self.stay:  
                self.aggressive = True
                if self.stay == False:
                    self.toggle_player = player.rect().center  
                if player.attack != -1:
                    self.stay_goto(self.toggle_player, True, min(self.game.items[player.attack]["knockback"]*(20/max(self.level, 10))*(player.level/50)*(0.75 if self.id in [60, 59, 58, 57, 56, 55] else 1), 10))
                    if self.rect().colliderect(player.attack_rect) and self.damage_couldown < 0:
                        self.damage_couldown = 0.3
                        self.life -= self.deal_damage(self.game.items[player.attack]["damage"], player)
            if self.damage_couldown > 0:
                self.damage_couldown -= self.game.get_dt()/60
            if distance(player.rect().center, self.rect().center) <= self.get_stat("Attack")/3:
                player.life -= (self.get_stat("Attack")*(self.level))/(player.level*200)
            if self.vel != [0, 0]:
                self.dir = direction(self.vel)
            else:
                self.dir = direction(pygame.Vector2(player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]))
        if self.on_screen():
            self.render()
        elif self.fairy and self.seen:
            self.kill()
            self.swimmer.kill()
        self.render_label()
    
        
    def render_label(self):
        self.game.render(self.game.labels[self.level], [self.pos[0]+5, self.pos[1] - min(float(self.get_data()["profile"]["height"].split(" ")[0])*15 + 10, 40)])
        if not self.id in [55, 56, 57, 58, 59, 60]:
            life_pos = [self.pos[0]+5, self.pos[1] - min(float(self.get_data()["profile"]["height"].split(" ")[0])*15 - 10, 40)]
            self.game.render_rect(pygame.rect.Rect(life_pos, (29, 6)), (0, 0, 0))
            self.game.render_rect(pygame.rect.Rect((life_pos[0]+1, life_pos[1]+1), ((30*(self.life/self.max_life)-3), 3)), (255, 0, 0))
        else:
            life_pos = [self.pos[0]-30, self.pos[1] - min(float(self.get_data()["profile"]["height"].split(" ")[0])*15 - 10, 40)]
            self.game.render_rect(pygame.rect.Rect(life_pos, (99, 6)), (0, 0, 0))
            self.game.render_rect(pygame.rect.Rect((life_pos[0]+1, life_pos[1]+1), ((100*(self.life/self.max_life)-3), 3)), (255, 0, 0))
        

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
        