from engine import *
from math import sin

class Menu:
    def __init__(self, game):
        self.game = game
        self.count = 0
        self.y = 360
        self.other_count = 0
        self.counter = 0
    def update(self):
        self.game.draw(self.game.assets["bg"], (0, 0))
        self.count += 0.3 * self.game.get_dt()
        self.other_count += 0.2 * self.game.get_dt()
        self.counter += self.game.get_dt()/60
        self.y += (sin(self.counter)/2.5)*self.game.get_dt()
        try: 
            self.game.render(self.game.assets["darkrai"].subsurface(pygame.Rect(int(self.count)*250, 0, 250, 224)), (300, self.y))
        except ValueError: 
            self.count = 0
            self.game.render(self.game.assets["darkrai"].subsurface(pygame.Rect(int(self.count)*250, 0, 250, 224)), (300, self.y))
        if pygame.key.get_pressed()[pygame.K_RETURN] and self.game.transition_count == 0:
            self.game.transition_count = 0.1
            self.game.transition_data = (0, 0, 5, [[0, 1], None, None])
        try: 
            self.game.render(self.game.assets["logo"].subsurface(pygame.Rect(int(self.other_count)*500, 0, 500, 213)), (160, 190))
        except ValueError: 
            self.other_count = 0
            self.game.render(self.game.assets["logo"].subsurface(pygame.Rect(int(self.other_count)*500, 0, 500, 213)), (160, 190))
