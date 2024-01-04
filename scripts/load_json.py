import json

DEX_PATH = "pokemon_data/dex.json"
SPAWN_PATH = "pokemon_data/spawn.json"

def load_dex():
    with open(DEX_PATH, "r") as file:
        return json.load(file)
    
def load_spawn():
    with open(SPAWN_PATH, "r") as file:
        return json.load(file)