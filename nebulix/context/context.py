import pygame, sys, os
from typing import *

class Context:

    def __init__(self, resolution:Tuple[int, int], flags:int=0, vsync:bool=False):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution, flags, vsync=vsync)
        self.clock = pygame.time.Clock()
        icon_path = os.path.join(__file__[:-10], "logo.png")
        
        pygame.display.set_caption("Nebulix Project", icon_path)
        pygame.display.set_icon(pygame.image.load(icon_path).convert_alpha())

    def run(self, game_loop):
        while 1:
            game_loop()
            pygame.display.flip()
            self.clock.tick(10000)

    def quit(self):
        pygame.quit()
        sys.exit()