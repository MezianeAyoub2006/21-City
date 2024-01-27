from engine import *

TILESETS = {
    "main_tileset" : load_sprite("tilesets/main.png", (32, 32))
}

SPRITES = {
    "player_walk_cycle" :  scale_animations(load_animation('player/walk_sprite.png', (32, 32), 3), (64, 64)),
    "pokemons" : scale_image_list(load_sprite("pokemons/overworld.png", (64, 128)), (128, 256)),
    "swimming_sprite" : scale_image_list(load_sprite("player/swimm.png", (32, 32)), (64, 64))
}

OTHER = {
    "shadow" : pygame.transform.scale(load_image("player/shadow.png"), (64, 64)),
    "portal" : scale_image_list(load_sprite("other/portal.png", (89, 98)), (89*2, 98*2))
}

MENU = {
    "darkrai" : pygame.transform.scale(load_image("menu/darkrai.png"), (250*35, 224)),
    "play_button" : load_sprite("menu/play_button.png", (197, 68)),
    "logo" : load_image("menu/logo.png"),
    "press_enter" : load_image("menu/press_enter.png"),
    "slot" : load_sprite("menu/slot.png", (44, 44)),
    "items" : load_sprite("items/items.png", (32, 32)),
    "bg" : load_image("menu/bg.png")
}

ATTACKS = {
    "wooden_stick_attack" : scale_image_list(load_sprite("attacks/wood_stick.png", (64, 64)), (128, 128)),
    "iron_sword_attack" : scale_image_list(load_sprite("attacks/iron_sword.png", (64, 64)), (128, 128)),
    "fire_sword_attack" : scale_image_list(load_sprite("attacks/fire_sword.png", (64, 64)), (128, 128)),
    "club_attack" : scale_image_list(load_sprite("attacks/club.png", (64, 64)), (128, 128)),
    "push_wand_attack" : scale_image_list(load_sprite("attacks/push_wand.png", (64, 64)), (128, 128)),
    "trident_attack" : scale_image_list(load_sprite("attacks/trident.png", (64, 64)), (128, 128)),
    "pokemon_attack0" : scale_image_list(load_sprite("attacks/pokemon_range0.png", (8, 8)), (16, 16)),
    "pokemon_attack1" : scale_image_list(load_sprite("attacks/pokemon_range1.png", (16, 16)), (32, 32)),
}