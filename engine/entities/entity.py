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
        self.image = pygame.Surface((0, 0))
    
    def update(self, scene):
        self.collisions = {'up': [], 'down': [], 'right': [], 'left': []}
        solid_tilemaps = scene.get_objects_by_tag("#solid")
        self.pos[0] += self.vel[0] * self.game.get_dt()
        rect = self.rect()
        if self.collide:
            for tilemap in solid_tilemaps:
                for tile in tilemap.get_tiles_around(self.rect().center):
                    if tile[0].colliderect(rect):
                        if self.vel[0] > 0:
                            rect.right = tile[0].left
                            self.collisions['right'].append(tile[1])
                        if self.vel[0] < 0:
                            rect.left = tile[0].right
                            self.collisions['left'].append(tile[1])
                        self.pos[0] = rect.x - self.offset[0]
        self.pos[1] += self.vel[1] * self.game.get_dt()
        rect = self.rect()
        if self.collide:
            for tilemap in solid_tilemaps:
                for tile in tilemap.get_tiles_around(self.rect().center):
                    if tile[0].colliderect(rect):
                        if self.vel[1] > 0:
                            rect.bottom = tile[0].top
                            self.collisions['down'].append(tile[1])
                        if self.vel[1] < 0:
                            rect.top = tile[0].bottom
                            self.collisions['up'].append(tile[1])
                        self.pos[1] = rect.y - self.offset[1]

    def rect(self):
        return pygame.Rect(self.pos[0] + self.offset[0], self.pos[1] + self.offset[1], self.size[0], self.size[1])
    
    def debug_rect(self, color=(255,0,0)):
        image = pygame.Surface((self.size[0], self.size[1]))
        image.fill(color)
        self.game.render(image, [self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]])

    def render(self):
        self.game.render(self.image, (self.pos[0] - self.offset[0], self.pos[1] - self.offset[1]))

