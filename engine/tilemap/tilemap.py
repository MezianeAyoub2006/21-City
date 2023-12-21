from engine.core.game_object import *
from engine.other.utils import generate_screen_positions
from engine.tilemap.tilemap_error import *
import pygame

class Tilemap(GameObject):
    def __init__(self, game, tile_size, z_pos, offset=(0, 0)):
        self.tile_size = tile_size
        GameObject.__init__(self, game, z_pos)
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255), (127, 127, 127), (255, 150, 150), (150, 255, 150), (150, 150, 255), (255, 255, 150), (255, 150, 255), (150, 255, 255)]
        self.tilemap = {}
        self.neighboor_offsets = [(i, j) for i in range(-1, 2, 1) for j in range(-1, 2, 1)]
        self.neighboor_offsets.remove((0, 0))
        self.tileset = []
        self.offset = offset
        self.content = []
        self.tags.append("@tile_map")

    def place_tile(self, id, location, rotation=0, flip_x=False, flip_y=False):
        try:
            self.tilemap[(location[0]+self.offset[0], location[1]+self.offset[1])] = {"pos" : [self.tile_size*location[0] + self.tile_size*self.offset[0], self.tile_size*location[1] + self.tile_size*self.offset[1]], "id":id, "rotation":rotation, "flip_x":flip_x, "flip_y":flip_y}
        except KeyError:
            raise TilemapError("Missing Tile", location)
        
    def place_pattern(self, pattern, location, rotation=0, flip_x=False, flip_y=False):
        steps = (len(pattern[0]), len(pattern))
        for x in range(steps[0]):
            for y in range(steps[1]):
                try:
                    self.place_tile(pattern[y][x], (location[0]+x, location[1]+y), rotation, flip_x, flip_y)
                except TilemapError:
                    raise
        
    def update(self, scene):
        for loc in generate_screen_positions(self.tile_size, self.game.camera, self.game.get_display_size()):
            try:
                tile = self.tilemap[loc]
                if tile != None:
                    surface = self.tileset[tile["id"]] 
                    if tile["rotation"] != 0:
                        surface = pygame.transform.rotate(surface, tile["rotation"])
                    if tile["flip_x"] or tile["flip_y"]:
                        surface = pygame.transform.flip(surface, tile["flip_x"], tile["flip_y"])
                    self.game.render(surface, tile["pos"])
                else:
                    del self.tilemap[loc]
            except KeyError:
                pass