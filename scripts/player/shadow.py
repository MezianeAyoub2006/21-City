from engine import *

class Shadow(GameObject):
    def __init__(self, game, obj, z_pos, offset=(0,0)):
        GameObject.__init__(self, game, z_pos)
        self.following_object = obj
        self.offset = offset
        self.image = self.game.assets["shadow"]
    def update(self, scene):
        self.game.render(self.image, (self.following_object.pos[0] + self.offset[0] + self.following_object.vel[0], self.following_object.pos[1] + self.offset[1]))
