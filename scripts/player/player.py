from engine import *
from scripts.generation.generation import *
from scripts.player.shadow import *

class Player(Entity, Animated):
    def __init__(self, game, pos, dir, life=100, level=5, inventory=[(0, 1), None, None, None, None]):
        Entity.__init__(self, game, pos, [24, 16], [10, 24], 2)
        Animated.__init__(self, game.assets["player_walk_cycle"])
        self.collide = True
        self.flip = False
        self.dir = dir
        self.level = level
        self.types = []
        self.speed = 3
        self.tags.append("@player")
        self.transition_data = None
        self.inventory = inventory.copy()
        self.couldown = [0, 0, 0, 0, 0]
        self.item_chosen = 0
        self.life = life
        self.max_life = 100
        self.xp = 0
        self.attack= False
        self.item_anim_cycle = 0
        self.switch = True
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
    
    def update(self, scene):
        xp_c = self.level**(1.35) + 25
        if self.xp > xp_c:
            self.level += self.xp // xp_c
            self.xp = self.xp % xp_c
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
        self.check_transitions()
        self.check_items()
        self.render_label()

    def render_label(self):
        self.game.render(self.game.labels[self.level], [self.pos[0]+8, self.pos[1] - min(float(1.3)*15 + 7, 40)])
        life_pos = [self.pos[0]+8, self.pos[1] - min(float(1.3)*15 - 10, 40)]
        self.game.render_rect(pygame.rect.Rect(life_pos, (29, 6)), (0, 0, 0))
        self.game.render_rect(pygame.rect.Rect((life_pos[0]+1, life_pos[1]+1), ((30*(self.life/self.max_life)-3), 3)), (255, 0, 0))
    
    def inventory_(self):
        for idx, slot in enumerate(self.inventory):
            self.game.draw(self.game.assets["slot"][int(idx == self.item_chosen)], (50*idx + 200, 360-44-5))
            if slot != None:
                self.game.draw(self.game.assets["items"][slot[0]], (50*idx + 200 + 3, 360-44-5 + 3))
                if slot[1] != 1:
                    self.game.draw_text(str(slot[1]), "main15", (50*idx + 200 + 25, 360-44-5 + 25))
    
    def check_items(self):
        self.switch = True
        self.attack = -1
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        if self.inventory[self.item_chosen] != None:
            if self.game.space and self.couldown[self.item_chosen] == 0:
                if self.game.items[self.inventory[self.item_chosen][0]]["type"] == "melee":
                    self.item_anim_cycle = 0.01
                    self.couldown[self.item_chosen] = self.game.items[self.inventory[self.item_chosen][0]]["couldown"]
        if self.item_anim_cycle != 0:
            self.switch = False
            self.attack = self.inventory[self.item_chosen][0]
            try:
                if self.dir in ['left', "down-left", "up-left"]:
                    image = pygame.transform.flip(self.game.assets[self.game.items[self.inventory[self.item_chosen][0]]["animation"]][int(self.item_anim_cycle)], True, False)
                    self.game.render(image, [self.pos[0]+self.game.items[self.inventory[self.item_chosen][0]]["loffset"][0], self.pos[1]+self.game.items[self.inventory[self.item_chosen][0]]["loffset"][1]])
                if self.dir in ['right', "down-right", "up-right"]:
                    image = pygame.transform.flip(self.game.assets[self.game.items[self.inventory[self.item_chosen][0]]["animation"]][int(self.item_anim_cycle)], False, False)
                    self.game.render(image, [self.pos[0]+self.game.items[self.inventory[self.item_chosen][0]]["roffset"][0], self.pos[1]+self.game.items[self.inventory[self.item_chosen][0]]["roffset"][1]])
                if self.dir == "down":
                    image = pygame.transform.rotate(pygame.transform.flip(self.game.assets[self.game.items[self.inventory[self.item_chosen][0]]["animation"]][int(self.item_anim_cycle)], True, False), 90)
                    self.game.render(image, [self.pos[0]+self.game.items[self.inventory[self.item_chosen][0]]["doffset"][0], self.pos[1]+self.game.items[self.inventory[self.item_chosen][0]]["doffset"][1]+65])
                if self.dir == "up":
                    image = pygame.transform.rotate(pygame.transform.flip(self.game.assets[self.game.items[self.inventory[self.item_chosen][0]]["animation"]][int(self.item_anim_cycle)], False, False), 90)
                    self.game.render(image, [self.pos[0]+self.game.items[self.inventory[self.item_chosen][0]]["uoffset"][0] - 65, self.pos[1]+self.game.items[self.inventory[self.item_chosen][0]]["uoffset"][1]])
                self.item_anim_cycle += self.game.items[self.inventory[self.item_chosen][0]]["speed"] * self.game.get_dt()        
            except Exception as e:
                self.item_anim_cycle = 0
        for idx in range(len(self.couldown)):
            if self.couldown[idx] > 0:
                self.couldown[idx] -= self.game.get_dt() * (1/60)
            else:
                self.couldown[idx] = 0
        if self.attack != -1:
            if self.dir in ["left", "up-left", "down-left"]:
                self.attack_rect = self.rect()
                range_ = self.game.items[self.inventory[self.item_chosen][0]]["range"]
                self.attack_rect.w = range_ // 2
                self.attack_rect.h = 60
                self.attack_rect.y -= 20
                self.attack_rect.x -= self.attack_rect.w
                #self.game.render_rect(self.attack_rect, (255, 0, 0))
            if self.dir in ["right", "up-right", "down-right"]:
                self.attack_rect = self.rect()
                w = self.attack_rect.w
                range_ = self.game.items[self.inventory[self.item_chosen][0]]["range"]
                self.attack_rect.w = range_ // 2
                self.attack_rect.x += w 
                self.attack_rect.h = 60
                self.attack_rect.y -= 20
                #self.game.render_rect(self.attack_rect, (255, 0, 0))
            if self.dir == "up":   
                self.attack_rect = self.rect()
                range_ = self.game.items[self.inventory[self.item_chosen][0]]["range"]
                self.attack_rect.h = range_ // 2
                self.attack_rect.w = 60
                self.attack_rect.x -= 15
                self.attack_rect.y += self.attack_rect.h
                self.attack_rect.top = self.attack_rect.top - range_ 
                #self.game.render_rect(self.attack_rect, (255, 0, 0))
            if self.dir == "down":
                self.attack_rect = self.rect()
                h = self.attack_rect.h
                range_ = self.game.items[self.inventory[self.item_chosen][0]]["range"]
                self.attack_rect.h = range_ // 2
                self.attack_rect.y += h
                self.attack_rect.w = 60
                self.attack_rect.x -= 20
                #self.game.render_rect(self.attack_rect, (255, 0, 0))

    def check_transitions(self):
        if self.pos[1] <= -56:
            index = (self.game.index[0], self.game.index[1]-1)
            player = Player(self.game, [11*32, 25*32-1], "down", self.life, self.level, self.inventory)
            for i in range(150): self.game.scroll(player.rect().center, 15)
            if self.game.camera[0] < 0: self.game.camera[0] = 0
            if self.game.camera[1] < 0: self.game.camera[1] = 0
            if self.game.camera[0] + self.game.get_display_size()[0]> self.game.size[0]*32: self.game.camera[0] = self.game.size[0]*32-self.game.get_display_size()[0]
            if self.game.camera[1] + self.game.get_display_size()[1]> self.game.size[1]*32: self.game.camera[1] = self.game.size[1]*32-self.game.get_display_size()[1]
            self.game.scenes[index].link(player, Shadow(self.game, player, 1.1, (-10, -2)), Swim(self.game, player, 1.1, (-10, 3)))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@player" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@swim" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@shadow" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.index = index
        if self.pos[1] >= 25 * 32:
            index = (self.game.index[0], self.game.index[1]+1)
            player = Player(self.game, [11*32, -55], "down", self.life,self.level, self.inventory)
            for i in range(150): self.game.scroll(player.rect().center, 15)
            if self.game.camera[0] < 0: self.game.camera[0] = 0
            if self.game.camera[1] < 0: self.game.camera[1] = 0
            if self.game.camera[0] + self.game.get_display_size()[0]> self.game.size[0]*32: self.game.camera[0] = self.game.size[0]*32-self.game.get_display_size()[0]
            if self.game.camera[1] + self.game.get_display_size()[1]> self.game.size[1]*32: self.game.camera[1] = self.game.size[1]*32-self.game.get_display_size()[1]
            self.game.scenes[index].link(player, Shadow(self.game, player, 1.1, (-10, -2)), Swim(self.game, player, 1.1, (-10, 3)))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@player" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@swim" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@shadow" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.index = index
        if self.pos[0] <= -56:
            index = (self.game.index[0]-1, self.game.index[1])
            player = Player(self.game, [25*32-1, 12*32], "down",self.life, self.level, self.inventory)
            for i in range(150): self.game.scroll(player.rect().center, 15)
            if self.game.camera[0] < 0: self.game.camera[0] = 0
            if self.game.camera[1] < 0: self.game.camera[1] = 0
            if self.game.camera[0] + self.game.get_display_size()[0]> self.game.size[0]*32: self.game.camera[0] = self.game.size[0]*32-self.game.get_display_size()[0]
            if self.game.camera[1] + self.game.get_display_size()[1]> self.game.size[1]*32: self.game.camera[1] = self.game.size[1]*32-self.game.get_display_size()[1]
            self.game.scenes[index].link(player, Shadow(self.game, player, 1.1, (-10, -2)), Swim(self.game, player, 1.1, (-10, 3)))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@player" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@swim" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@shadow" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.index = index
        if self.pos[0] >= 25 * 32:
            index = (self.game.index[0]+1, self.game.index[1])
            player = Player(self.game, [-55, 12*32], "down", self.life,self.level, self.inventory)
            for i in range(150): self.game.scroll(player.rect().center, 15)
            if self.game.camera[0] < 0: self.game.camera[0] = 0
            if self.game.camera[1] < 0: self.game.camera[1] = 0
            if self.game.camera[0] + self.game.get_display_size()[0]> self.game.size[0]*32: self.game.camera[0] = self.game.size[0]*32-self.game.get_display_size()[0]
            if self.game.camera[1] + self.game.get_display_size()[1]> self.game.size[1]*32: self.game.camera[1] = self.game.size[1]*32-self.game.get_display_size()[1]
            self.game.scenes[index].link(player, Shadow(self.game, player, 1.1, (-10, -2)), Swim(self.game, player, 1.1, (-10, 3)))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@player" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@swim" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.scenes[self.game.index].objects = list(filter(lambda x : not "@shadow" in x.tags, self.game.scenes[self.game.index].objects))
            self.game.index = index
    
    def render(self):
        self.flip_image(self.flip, False)
        super().render()