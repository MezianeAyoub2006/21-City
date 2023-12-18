import pygame
from typing import *

class Context:

    def __init__(self, resolution:Tuple[int, int], flags:int=0, vsync:bool=False):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution, flags, vsync=vsync)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self, game_loop):
        while self.running:
            game_loop()
            pygame.display.flip()
            self.clock.tick(10000)

    def quit(self):
        pygame.quit()
        self.running = False