from engine import *
from math import sin

class Menu:
    def __init__(self, game):
        self.game = game
        self.count = 0
        self.y = -40
        self.counter = 0
    def update(self):
        self.count += 0.3 * self.game.get_dt()
        self.counter += self.game.get_dt()/60
        self.y += (sin(self.counter)/2.5)*self.game.get_dt()
        try: 
            self.game.render(self.game.assets["darkrai"].subsurface(pygame.Rect(int(self.count)*500, 0, 500, 448)), (180, self.y))
        except ValueError: 
            self.count = 0
            self.game.render(self.game.assets["darkrai"].subsurface(pygame.Rect(int(self.count)*500, 0, 500, 448)), (180, self.y))
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            self.game.state = 0
        self.game.draw(self.game.assets["logo"], (10, 5))
        if sin(self.counter*7) >= 0:
            self.game.draw(self.game.assets["press_enter"], (50, 220))
