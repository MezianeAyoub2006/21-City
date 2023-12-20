from typing import *

class Context:

    def __init__(self, resolution:Tuple[int, int], flags:int=0, vsync:bool=False):
        """
engine.context.Context

Handle game context object. It wraps all game functionalities. Essential to make every game components work together.

Args:
    resolution (int > 0, int > 0) : resolution of the display 
    flags int                     : flags to apply into the screen
    optional vsync bool           : apply vsyinc or not (default False)
        """
        ...
    
    def run(self, game_loop):
        """
engine.context.Context.run

Initialize the game loop.

Args:
    game_loop function : executed every frame
        """
        ...
    
    def quit(self):
        """
engine.context.Context.quit

Quit and close the game.
        """
        ...