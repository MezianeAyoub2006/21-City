from engine import *
import pygame

ctx = Context((1280, 720))

def game_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctx.quit()

ctx.run(game_loop=game_loop)
