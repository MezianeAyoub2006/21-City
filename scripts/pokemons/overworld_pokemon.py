from engine import *
import random 

class OverworldPokemon(Entity):

    def __init__(self, game, pos, id, speed, randomness):
        self.id = id
        self.speed = speed
        self.randomness = randomness
        Entity.__init__(self, game, pos, (32, 32), (0, 0), 2)
        self.collide = True
        self.moving = False
        self.dir = "up"

    def update(self, scene):
        Entity.update(self, scene)
        self.debug_rect()

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
        