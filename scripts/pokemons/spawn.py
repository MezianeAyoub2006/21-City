from scripts.pokemons.pokemon import *
from scripts.utils import *
import random

def spawn_pokemon(scene, id, pos, level, z_pos):
    scene.link(Pokemon(scene.game, pos, id, level, z_pos))

def spawn_group(scene, id, center, z_pos, levels):
    group = scene.game.spawn_data["group"][id]
    parts = []
    values = []
    for i in group["composition"]:
        parts.append(scene.game.spawn_data["solo"][i-1]["part"])
        values.append(i)
    for i in range(random.choice(range_list(group["number"]))):
        pokemon_id = get_prob_value(values, parts)
        spawn_pokemon(scene, pokemon_id, random_position_inside_circle(10*32, center), random.randint(levels[0], levels[1]), z_pos)

