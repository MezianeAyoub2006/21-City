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
        solid_tilemaps = scene.get_objects_by_tag("#solid")
        self.pos[0] += self.vel[0] * self.game.get_dt()
        rect = self.rect()
        if self.collide:
            for tilemap in solid_tilemaps:
                for tile in tilemap.get_tiles_around(self.rect().center):
                    if tile[0].colliderect(rect):
                        if self.vel[0] > 0:
                            rect.right = tile[0].left
                        if self.vel[0] < 0:
                            rect.left = tile[0].right
                        self.pos[0] = rect.x
        self.pos[1] += self.vel[1] * self.game.get_dt()
        rect = self.rect()
        if self.collide:
            for tilemap in solid_tilemaps:
                for tile in tilemap.get_tiles_around(self.rect().center):
                    if tile[0].colliderect(rect):
                        if self.vel[1] > 0:
                            rect.bottom = tile[0].top
                        if self.vel[1] < 0:
                            rect.top = tile[0].bottom
                        self.pos[1] = rect.y

    def rect(self):
        return pygame.Rect(self.pos, self.size)
    
    def debug_rect(self, color=(255,0,0)):
        self.game.render_rect(self.rect(), color)

