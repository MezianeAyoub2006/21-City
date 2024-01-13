from engine import *

class Shadow(GameObject):
    def __init__(self, game, obj, z_pos, offset=(0,0)):
        GameObject.__init__(self, game, z_pos)
        self.following_object = obj
        self.offset = offset
        self.tags.append("@shadow")
        self.image = self.game.assets["shadow"]
    def update(self, scene):
        self.game.render(self.image, (self.following_object.pos[0] + self.offset[0] + self.following_object.vel[0], self.following_object.pos[1] + self.offset[1]))

class Swim(GameObject):
    def __init__(self, game, obj, z_pos, offset=(0,0)):
        GameObject.__init__(self, game, z_pos)
        self.following_object = obj
        self.offset = offset
        self.assets = self.game.assets["swimming_sprite"]
        self.tags.append("@swim")
    def update(self, scene):
        water = False
        for layer in scene.get_objects_by_tag("@tilemap"):
            for tiles in layer.get_tiles_around(self.following_object.rect().center):
                if tiles[1] == 338:
                    water = True
                elif tiles[1] in [4124]:
                    water = False
        if water and not "water" in self.following_object.types:
            self.images = self.assets.copy()
            if self.following_object.dir in ["right", "up-right", "down-right"]:
                self.images[1] = pygame.transform.flip(self.images[1], True, False)
            self.game.render(self.images[0 if self.following_object.dir == "down" else (1 if self.following_object.dir in ["left", "right", "up-left", "down-left", "up-right", "down-right"] else 2)], (self.following_object.pos[0] + self.offset[0] + self.following_object.vel[0], self.following_object.pos[1] + self.offset[1]))

