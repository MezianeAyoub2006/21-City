from engine.core.game_object import *
import pygame

class Entity(GameObject):

    def __init__(self, game, pos, size, offset, z_pos):
        GameObject.__init__(self, game, z_pos)
        self.pos = pos
        self.size = size
        self.offset = offset
        self.tags.append("@entity")
        self.collide = False
        self.vel = [0, 0]
    
    def update(self, scene):
        self.pos[0] += self.vel[0] * self.game.get_dt()
        self.pos[1] += self.vel[1] * self.game.get_dt()

    def rect(self):
        return pygame.Rect(self.pos, self.size)
    
    def debug_rect(self, color=(255,0,0)):
        self.game.render_rect(self.rect(), color)

