import json

DEX_PATH = "C:/Users/Karima Meziane/Desktop/Black Jack/pokemon_data/dex.json"
SPAWN_PATH = "C:/Users/Karima Meziane/Desktop/Black Jack/pokemon_data/spawn.json"

def load_dex():
    with open(DEX_PATH, "r") as file:
        return json.load(file)
    
def load_spawn():
    with open(SPAWN_PATH, "r") as file:
        return json.load(file)