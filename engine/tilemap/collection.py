from engine.tilemap.tilemap_error import *
from engine.tilemap.tilemap import *

class TilemapCollection:
    def __init__(self, game, tile_size):
        self.tilemaps = {}
        self.game = game
        self.tile_size = tile_size

    def add_tilemaps(self, *tilemaps):
        for tilemap in tilemaps:
            self.tilemaps[tilemap.z_pos] = tilemap

    def link(self, scene):
        for tilemap in self.tilemaps:
            scene.link(self.tilemaps[tilemap])
    
    def __getitem__(self, item):
        return self.tilemaps[item]

    def place_tile(self, id, location, z_pos, rotation=0, flip_x=False, flip_y=False):
        try:
            self.tilemaps[z_pos].place_tile(id, location, rotation, flip_x, flip_y)
        except KeyError:
            raise TilemapError("Missing Tile", location)
        
    def place_pattern(self, pattern, location, z_pos, rotation=0, flip_x=False, flip_y=False):
        self.tilemaps[z_pos].place_pattern(pattern, location, rotation, flip_x, flip_y)
    
    def place_multidim_pattern(self, pattern, location, z_pos, step=1, rotation=0, flip_x=False, flip_y=False, tags={}):
        for i in range(z_pos, len(pattern)+z_pos, step):
            if not i in self.tilemaps.keys():
                self.tilemaps[i] = Tilemap(self.game, self.tile_size, i)
                self.tilemaps[i].tileset = self.tilemaps[0].tileset
                if i in tags:
                    for tag in tags[i]:
                        self.tilemaps[i].tags.append(tag)
            self.tilemaps[i].place_pattern(pattern[i-z_pos], location, rotation, flip_x, flip_y)
    
    def get_tiles(self, location):
        tiles = []
        for tilemap in self.tilemaps.values():
            tiles.append((tilemap.tilemap[location], "#solid" in tilemap.tags))
        return tiles
    
    def get_solid_map(self, begin_pos, end_pos):
        matrix = [[0 for j in range(abs(begin_pos[0] - end_pos[0]))] for i in range(abs(begin_pos[1] - end_pos[1]))]
        for x in range(abs(begin_pos[0] - end_pos[0])):
            for y in range(abs(begin_pos[1] - end_pos[1])):
                try:
                    tiles = self.get_tiles((begin_pos[0]+x, begin_pos[1]+y))
                    matrix[y][x] = int(any(tile[1] == True for tile in tiles))
                except:
                    pass
        return matrix


