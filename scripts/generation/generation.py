from engine import *
from scripts.pokemons.spawn import *
import random

BACKGROUND_ID = 1
GRASS_ID = 13
ANIM_FLOWERS = [3608, 3616]
WATER = [338, 346, 354, 362, 370, 394]

def generate_biome_collection(game, scene, size, tile_size, id, config):
    collection = TilemapCollection(game, tile_size)
    biome = game.biomes_data[id]["name"]
    spawned = False
    while not spawned:
        for i in range(1):
            for group in game.spawn_data["group"]:
                if biome in group["biome"]:
                    if random.random() < group["biome"][biome]:
                        spawn_group(scene, group["id"], (12*32, 12*32), 2)
                        spawned = True

    collection.add_tilemaps(
            Tilemap(game, tile_size, 0),    # Background Layer
            Tilemap(game, tile_size, 1),    # Middle Layer
            Tilemap(game, tile_size, 1.01), # Middle Up Layer
            Tilemap(game, tile_size, 2),    # Collision Layer
            Tilemap(game, tile_size, 3),    # Up Layer
            Tilemap(game, tile_size, 4)     # Upper Layer
        )

    collection[2].tags.append("#solid") 

    for tilemap in collection.tilemaps.values():
        tilemap.tileset = game.assets["main_tileset"]
        for flower in ANIM_FLOWERS:
            tilemap.set_animation_tile(flower, 0.15, [i for i in range(flower, flower+8)])
        tilemap.set_animation_tile(338, 0.15, WATER)
        

    forbiden_positions = []
    tree_range = [10, 20]
    path_way = random.randint(0, 3)

    """
    ---------------------------
    |  ID = 0 ; BIOME PLAINE  |
    ---------------------------
    """
    if id == 0:     
        tree_pattern = tiled_to_pattern("data/maps/structures/other/basic_tree.json")
        if id == 0: 
            collection[0].place_pattern([[BACKGROUND_ID for x in range(size[0])] for y in range(size[1])], (0, 0))
            for i in range(random.randint(10, 30)):
                collection[1.01].place_tile(random.choice(ANIM_FLOWERS), (random.randint(0, size[0]), random.randint(0, size[1])))
            
            if not config in [0, 1]:
                center_x, center_y = size[0] // 2, size[1] // 2  
                max_radius = min(size[0] // 2, size[1] // 2) 
                for i in range(5, size[0]-5):
                    for j in range(5, size[1]-5):
                        distance_to_center = ((i - center_x) ** 2 + (j - center_y) ** 2) ** 0.5
                        probability = 1.0 - min(1.0, distance_to_center / max_radius)  
                        if random.random() < probability:
                            collection[1.01].place_tile(GRASS_ID, (i, j))
                forbiden_positions += [(x, y) for x in range(6, size[0]-6) for y in range(6, size[1]-6)] 

            if config == 0: # LEFT & RIGHT
                collection.place_multidim_pattern(tiled_to_pattern(f"data/maps/structures/plain/horizontal/{path_way}.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
                probs = [1, 1, 0.9, 0.7, 0.5, 0.3, 0.1]
                for i, prob in enumerate(probs):
                    collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None for j in range(size[0]-2)]], (1, i+1)) 
                    collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None for j in range(size[0]-2)]], (1, size[1]-i-1)) 
                forbiden_positions += [(x, y) for x in range(size[0]) for y in range(10, size[1]-10)]

            if config == 1: # UP & DOWN
                collection.place_multidim_pattern(tiled_to_pattern(f"data/maps/structures/plain/vertical/{path_way}.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
                probs = [1, 1, 0.9, 0.7, 0.5, 0.3, 0.1]
                for i, prob in enumerate(probs):
                    collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None] for j in range(size[1]-2)], (i+1, 1))
                    collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None] for j in range(size[1]-2)], (size[0]-i-2, 1)) 
                forbiden_positions += [(x, y) for x in range(10, size[0]-10) for y in range(size[1])]
            
            if config == 2: # UP & DOWN & LEFT & RIGHT
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)
           
            if config == 3: # LEFT
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
            
            if config == 4: # RIGHT
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)       

            if config == 5: # UP
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
                 
            if config == 6: # DOWN
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
            
            if config == 7: # DOWN & LEFT
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
            
            if config == 8: # DOWN & RIGHT
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)
            
            if config == 9: # UP & LEFT
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
            
            if config == 10: # UP & RIGHT
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)

            forbiden = get_pattern_overlap_offsets(tree_pattern[0]) 
            for i in range(random.randint(*tree_range)):
                pos = (random.randint(1, size[0]-3), random.randint(1, size[1]-4)) 
                if not pos in forbiden_positions: 
                    collection.place_multidim_pattern(tree_pattern, pos, 2) 
                    collection.place_pattern(tree_pattern[0], pos, 1.01)
                for pos_ in apply_offsets(pos, forbiden):
                    forbiden_positions.append(pos_) 

    """
    ---------------------------------
    |  ID = 1 ; BIOME PLAINE DENSE  |
    ---------------------------------
    """
    
    if id == 1: 
        tree_range = [20, 30]
        tree_pattern = tiled_to_pattern("data/maps/structures/other/dense_tree.json")
        collection[0].place_pattern([[28 for x in range(size[0])] for y in range(size[1])], (0, 0))
        path_way = random.randint(0, 3)
        for i in range(random.randint(10, 30)):
            collection[1.01].place_tile(random.choice(ANIM_FLOWERS), (random.randint(0, size[0]), random.randint(0, size[1])))
        
        if not config in [0, 1]:
            center_x, center_y = size[0] // 2, size[1] // 2  
            max_radius = min(size[0] // 2, size[1] // 2) 
            for i in range(5, size[0]-5):
                for j in range(5, size[1]-5):
                    distance_to_center = ((i - center_x) ** 2 + (j - center_y) ** 2) ** 0.5
                    probability = 1.0 - min(1.0, distance_to_center / max_radius)  
                    if random.random()*0.8 < probability:
                        collection[1.01].place_tile(GRASS_ID, (i, j))
            forbiden_positions += [(x, y) for x in range(6, size[0]-6) for y in range(6, size[1]-6)] 

        if config == 0: # LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern(f"data/maps/structures/plain/horizontal/{path_way}.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            probs = [1, 1, 0.9, 0.7, 0.5, 0.3, 0.1]
            for i, prob in enumerate(probs):
                collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None for j in range(size[0]-2)]], (1, i+1)) 
                collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None for j in range(size[0]-2)]], (1, size[1]-i-1)) 
            forbiden_positions += [(x, y) for x in range(size[0]) for y in range(8, size[1]-8)]

        if config == 1: # UP & DOWN
            collection.place_multidim_pattern(tiled_to_pattern(f"data/maps/structures/plain/vertical/{path_way}.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            probs = [1, 1, 0.9, 0.7, 0.5, 0.3, 0.1]
            for i, prob in enumerate(probs):
                collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None] for j in range(size[1]-2)], (i+1, 1))
                collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None] for j in range(size[1]-2)], (size[0]-i-2, 1)) 
            forbiden_positions += [(x, y) for x in range(8, size[0]-8) for y in range(size[1])]
        
        if config == 2: # UP & DOWN & LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)
        
        if config == 3: # LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
        
        if config == 4: # RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)       

        if config == 5: # UP
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
                
        if config == 6: # DOWN
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
        
        if config == 7: # DOWN & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
        
        if config == 8: # DOWN & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)
        
        if config == 9: # UP & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
        
        if config == 10: # UP & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)

        forbiden = get_pattern_overlap_offsets(tree_pattern[0]) 
        for i in range(random.randint(*tree_range)):
            pos = (random.randint(1, size[0]-3), random.randint(1, size[1]-4)) 
            if not pos in forbiden_positions: 
                collection.place_multidim_pattern(tree_pattern, pos, 2) 
                collection.place_pattern(tree_pattern[0], pos, 1.01)
            for pos_ in apply_offsets(pos, forbiden):
                forbiden_positions.append(pos_) 

    """
    -----------------------------
    |  ID = 2 ; BIOME MARECAGE  |
    -----------------------------
    """
    
    if id == 2: 
        tree_range = [30, 40]
        tree_pattern = tiled_to_pattern("data/maps/structures/other/forest_tree.json")
        collection[0].place_pattern([[2225 for x in range(size[0])] for y in range(size[1])], (0, 0))
        path_way = random.randint(0, 3)
        for i in range(random.randint(10, 30)):
            collection[1.01].place_tile(random.choice(ANIM_FLOWERS), (random.randint(0, size[0]), random.randint(0, size[1])))
        
        if not config in [0, 1]:
            center_x, center_y = size[0] // 2, size[1] // 2  
            max_radius = min(size[0] // 2, size[1] // 2) 
            for i in range(5, size[0]-5):
                for j in range(5, size[1]-5):
                    distance_to_center = ((i - center_x) ** 2 + (j - center_y) ** 2) ** 0.5
                    probability = 1.0 - min(1.0, distance_to_center / max_radius)  
                    if random.random()*0.8 < probability:
                        collection[1.01].place_tile(GRASS_ID, (i, j))
            forbiden_positions += [(x, y) for x in range(6, size[0]-6) for y in range(6, size[1]-6)] 

        if config == 0: # LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern(f"data/maps/structures/plain/horizontal/{path_way}.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            probs = [1, 1, 0.9, 0.7, 0.5, 0.3, 0.1]
            for i, prob in enumerate(probs):
                collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None for j in range(size[0]-2)]], (1, i+1)) 
                collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None for j in range(size[0]-2)]], (1, size[1]-i-1)) 
            forbiden_positions += [(x, y) for x in range(size[0]) for y in range(8, size[1]-8)]

        if config == 1: # UP & DOWN
            collection.place_multidim_pattern(tiled_to_pattern(f"data/maps/structures/plain/vertical/{path_way}.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            probs = [1, 1, 0.9, 0.7, 0.5, 0.3, 0.1]
            for i, prob in enumerate(probs):
                collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None] for j in range(size[1]-2)], (i+1, 1))
                collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None] for j in range(size[1]-2)], (size[0]-i-2, 1)) 
            forbiden_positions += [(x, y) for x in range(8, size[0]-8) for y in range(size[1])]
        
        if config == 2: # UP & DOWN & LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)
        
        if config == 3: # LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
        
        if config == 4: # RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)       

        if config == 5: # UP
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
                
        if config == 6: # DOWN
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
        
        if config == 7: # DOWN & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
        
        if config == 8: # DOWN & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)
        
        if config == 9: # UP & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
        
        if config == 10: # UP & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)

        forbiden = get_pattern_overlap_offsets(tree_pattern[0]) 
        for i in range(random.randint(*tree_range)):
            pos = (random.randint(1, size[0]-3), random.randint(1, size[1]-4)) 
            if not pos in forbiden_positions: 
                collection.place_multidim_pattern(tree_pattern, pos, 2) 
                collection.place_pattern(tree_pattern[0], pos, 1.01)
            for pos_ in apply_offsets(pos, forbiden):
                forbiden_positions.append(pos_) 
    
    """
    --------------------------
    |  ID = 3 ; BIOME PLAGE  |
    --------------------------
    """

    if id == 3:
        tree_range = [5, 7]
        collection[0].place_pattern([[289 for x in range(size[0])] for y in range(size[1])], (0, 0))
        tree_pattern = tiled_to_pattern("data/maps/structures/other/parasol.json")
        if config == 0: # LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern(f"data/maps/structures/plain/horizontal/{path_way}.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)

        if config == 1: # UP & DOWN
            collection.place_multidim_pattern(tiled_to_pattern(f"data/maps/structures/plain/vertical/{path_way}.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 2: # UP & DOWN & LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)
        
        if config == 3: # LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
        
        if config == 4: # RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)       

        if config == 5: # UP
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
                
        if config == 6: # DOWN
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
        
        if config == 7: # DOWN & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
        
        if config == 8: # DOWN & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)
        
        if config == 9: # UP & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
        
        if config == 10: # UP & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)
        
        forbiden = get_pattern_overlap_offsets(tree_pattern[0]) 
        for i in range(random.randint(*tree_range)):
            pos = (random.randint(1, size[0]-3), random.randint(1, size[1]-4)) 
            if not pos in forbiden_positions: 
                collection.place_multidim_pattern(tree_pattern, pos, 2) 
                collection.place_pattern(tree_pattern[0], pos, 1.01)
            for pos_ in apply_offsets(pos, forbiden):
                forbiden_positions.append(pos_) 
        tree_pattern = tiled_to_pattern('data/maps/structures/other/rock1.json')
        forbiden = get_pattern_overlap_offsets(tree_pattern[0]) 
        for i in range(random.randint(*tree_range)):
            pos = (random.randint(1, size[0]-3), random.randint(1, size[1]-4)) 
            if not pos in forbiden_positions: 
                collection.place_multidim_pattern(tree_pattern, pos, 2) 
                collection.place_pattern(tree_pattern[0], pos, 1.01)
            for pos_ in apply_offsets(pos, forbiden):
                forbiden_positions.append(pos_) 
        for i in range(random.randint(8, 12)):
            pos = (random.randint(1, size[0]-2), random.randint(1, size[1]-2)) 
            if not pos in forbiden_positions:
                collection.place_tile(1927, pos, 2)
    
    """
    ------------------------
    |  ID = 4 ; BIOME CAVE |
    ------------------------
    """
    
    if id == 4:
        tree_range = [5, 7]
        collection[0].place_pattern([[2046 for x in range(size[0])] for y in range(size[1])], (0, 0))
        tree_pattern = tiled_to_pattern("data/maps/structures/other/parasol.json")

        if config == 0: # LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)

        if config == 1: # UP & DOWN
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 2: # UP & DOWN & LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
        
        if config == 3: # LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 4: # RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)     

        if config == 5: # UP
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                
        if config == 6: # DOWN
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
        
        if config == 7: # DOWN & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 8: # DOWN & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
        
        if config == 9: # UP & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 10: # UP & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
        
        tree_pattern = tiled_to_pattern('data/maps/structures/other/rock1.json')
        forbiden = get_pattern_overlap_offsets(tree_pattern[0]) 
        for i in range(random.randint(*tree_range)):
            pos = (random.randint(1, size[0]-3), random.randint(1, size[1]-4)) 
            if not pos in forbiden_positions: 
                collection.place_multidim_pattern(tree_pattern, pos, 2) 
                collection.place_pattern(tree_pattern[0], pos, 1.01)
            for pos_ in apply_offsets(pos, forbiden):
                forbiden_positions.append(pos_) 
        for i in range(random.randint(8, 12)):
            pos = (random.randint(1, size[0]-2), random.randint(1, size[1]-2)) 
            if not pos in forbiden_positions:
                collection.place_tile(random.choice((2035, 2036)), pos, 2)
    
    """
    --------------------------------
    |  ID = 5 ; BIOME CAVE ARDENTE |
    --------------------------------
    """

    if id == 5:
        tree_range = [5, 7]
        collection[0].place_pattern([[3904 for x in range(size[0])] for y in range(size[1])], (0, 0))
        tree_pattern = tiled_to_pattern("data/maps/structures/other/parasol.json")

        if config == 0: # LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)

        if config == 1: # UP & DOWN
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 2: # UP & DOWN & LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
        
        if config == 3: # LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 4: # RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)     

        if config == 5: # UP
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                
        if config == 6: # DOWN
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
        
        if config == 7: # DOWN & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 8: # DOWN & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
        
        if config == 9: # UP & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 10: # UP & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
        
        tree_pattern = tiled_to_pattern('data/maps/structures/other/rock2.json')
        forbiden = get_pattern_overlap_offsets(tree_pattern[0]) 
        for i in range(random.randint(*tree_range)):
            pos = (random.randint(1, size[0]-3), random.randint(1, size[1]-4)) 
            if not pos in forbiden_positions: 
                collection.place_multidim_pattern(tree_pattern, pos, 2) 
                collection.place_pattern(tree_pattern[0], pos, 1.01)
            for pos_ in apply_offsets(pos, forbiden):
                forbiden_positions.append(pos_) 
        for i in range(random.randint(8, 12)):
            pos = (random.randint(1, size[0]-2), random.randint(1, size[1]-2)) 
            if not pos in forbiden_positions:
                collection.place_tile(3909, pos, 2)

    """
    -----------------------------
    |  ID = 6 ; BIOME AQUATIQUE |
    -----------------------------
    """

    if id == 6:
        tree_range = [5, 7]
        collection[0].place_pattern([[338 for x in range(size[0])] for y in range(size[1])], (0, 0))
        tree_pattern = tiled_to_pattern("data/maps/structures/other/parasol.json")
        collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/other/sea_rock.json"), (10, 10), 1)
        for x in range(8, 15):
            for y in range(10, 15):
                forbiden_positions.append((x, y))

        if config == 0: # LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)

        if config == 1: # UP & DOWN
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 2: # UP & DOWN & LEFT & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
        
        if config == 3: # LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 4: # RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)     

        if config == 5: # UP
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                
        if config == 6: # DOWN
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
        
        if config == 7: # DOWN & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 8: # DOWN & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
        
        if config == 9: # UP & LEFT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
        
        if config == 10: # UP & RIGHT
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
            collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
        
        tree_pattern = tiled_to_pattern('data/maps/structures/other/rock1.json')
        forbiden = get_pattern_overlap_offsets(tree_pattern[0]) 
        for i in range(random.randint(*tree_range)):
            pos = (random.randint(1, size[0]-3), random.randint(1, size[1]-4)) 
            if not pos in forbiden_positions: 
                collection.place_multidim_pattern(tree_pattern, pos, 2) 
                collection.place_pattern(tree_pattern[0], pos, 1.01)
            for pos_ in apply_offsets(pos, forbiden):
                forbiden_positions.append(pos_) 

    return collection


# 0 LEFT & RIGHT
# 1 UP & DOWN
# 2 LEFT & RIGHT & UP & DOWN
# 3 LEFT
# 4 RIGHT
# 5 UP
# 6 DOWN
# 7 LEFT & DOWN
# 8 RIGHT & DOWN
# 9 LEFT & UP
# 10 RIGHT & UP

def get_biome_type(p, r, n):
    for i in range(2):
        if i == 0:
            previous = p
            room = r
            next = n
        else:
            previous = n
            room = r
            next = p
        if previous == None:
            if next[0] > room[0]:
                return 4
            if room[0] > next[0]:
                return 3
            if next[1] < room[1]:
                return 5
            if room[1] < next[1]:
                return 6
        elif next == None:
            if previous[0] > room[0]:
                return 4
            if room[0] > previous[0]:
                return 3
            if previous[1] < room[1]:
                return 5
            if room[1] < previous[1]:
                return 6
        else:
            if next[1] == previous[1] == room[1]:
                return 0
            if next[0] == previous[0] == room[0]:
                return 1
            if next[1] > room[1]:
                if previous[0] < room[0]:
                    return 7
                if previous[0] > room[0]:
                    return 8
            if next[1] < room[1]:
                if previous[0] < room[0]:
                    return 9
                if previous[0] > room[0]:
                    return 10
            
        
def generate_room(game, biome):
    path = generate_room_path()
    print(path)
    room = {}
    for index, pos in enumerate(path):
        room[pos] = Scene(game)
        if index == 0: previous = None
        else: previous = path[index-1]
        if index == len(path)-1: next = None
        else: next = path[index + 1]
        print(f"({previous}, {pos}, {next}) ; {get_biome_type(previous, pos, next)}")
        room[pos].link(*generate_biome_collection(game, room[pos], game.size, 32, biome, get_biome_type(previous, pos, next)).tilemaps.values())
    return room