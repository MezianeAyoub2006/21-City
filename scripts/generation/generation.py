from engine import *
import random

BACKGROUND_ID = 1
GRASS_ID = 13
ANIM_FLOWERS = [3608, 3616]
def generate_biome_collection(game, size, tile_size, id, config):
    collection = TilemapCollection(game, tile_size)
    """
    ---------------------------
    |  ID = 0 ; BIOME PLAINE  |
    ---------------------------
    """
    if id == 0: 
        collection.add_tilemaps(
            Tilemap(game, tile_size, 0),    # Background Layer
            Tilemap(game, tile_size, 1),    # Middle Layer
            Tilemap(game, tile_size, 1.01), # Middle Up Layer
            Tilemap(game, tile_size, 2),    # Collision Layer
            Tilemap(game, tile_size, 3),    # Up Layer
            Tilemap(game, tile_size, 4)     # Upper Layer
        )

        collection[2].tags.append("#solid") # attribution de la propriété à être solide pour la couche 2

        for tilemap in collection.tilemaps.values():
            # défnition du jeu de tuiles (tileset) pour chaque couche 
            tilemap.tileset = game.assets["main_tileset"]
            # définition de l'animation des fleurs
            for flower in ANIM_FLOWERS:
                tilemap.set_animation_tile(flower, 0.15, [i for i in range(flower, flower+8)])

        tree_pattern = tiled_to_pattern("data/maps/structures/other/basic_tree.json") # chargement du modèle de l'arbre
        forbiden_positions = [] # liste des positions bannies de placement d'arbres
        tree_range = [10, 20]
        
        if id == 0: #Génération de la plaine
            # Eléments commun à toutes les variantes de plaines
            collection[0].place_pattern([[BACKGROUND_ID for x in range(size[0])] for y in range(size[1])], (0, 0))

            # choix de la variante de chemin parmi quatres
            path_way = random.randint(0, 3)

            # placement des fleurs
            for i in range(random.randint(10, 30)):
                collection[1.01].place_tile(random.choice(ANIM_FLOWERS), (random.randint(0, size[0]), random.randint(0, size[1])))
            
            if config in [2, 3, 4, 5, 6]:
                # Génération d'un cercle d'hautes herbes
                center_x, center_y = size[0] // 2, size[1] // 2  # Centre de la salle
                max_radius = min(size[0] // 2, size[1] // 2)  # Rayon du cercle d'hautes herbes
                for i in range(5, size[0]-5):
                    for j in range(5, size[1]-5):
                        distance_to_center = ((i - center_x) ** 2 + (j - center_y) ** 2) ** 0.5
                        probability = 1.0 - min(1.0, distance_to_center / max_radius)  
                        if random.random() < probability:
                            collection[1.01].place_tile(GRASS_ID, (i, j))
                forbiden_positions += [(x, y) for x in range(6, size[0]-6) for y in range(6, size[1]-6)] # Empécher les arbres d'aparaitre dans le cercle

            if config == 0: # Variante horizontale 
                collection.place_multidim_pattern(tiled_to_pattern(f"data/maps/structures/plain/horizontal/{path_way}.json"), (0, 0), 1) # chargement du modèle de chemin
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
                probs = [1, 1, 0.9, 0.7, 0.5, 0.3, 0.1] # probabilitées de contenir des hautes herbes
                for i, prob in enumerate(probs):
                    collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None for j in range(size[0]-2)]], (1, i+1)) # placement de la ligne d'hautes herbes en haut
                    collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None for j in range(size[0]-2)]], (1, size[1]-i-1)) # placement de la ligne d'hautes herbes en bas
                forbiden_positions += [(x, y) for x in range(size[0]) for y in range(10, size[1]-10)]

            if config == 1: # Variante verticale
                collection.place_multidim_pattern(tiled_to_pattern(f"data/maps/structures/plain/vertical/{path_way}.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
                probs = [1, 1, 0.9, 0.7, 0.5, 0.3, 0.1]
                for i, prob in enumerate(probs):
                    collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None] for j in range(size[1]-2)], (i+1, 1)) # placement cette fois-ci à gauche
                    collection[1.01].place_pattern([[GRASS_ID if random.random() < prob else None] for j in range(size[1]-2)], (size[0]-i-2, 1)) # puis à droite
                forbiden_positions += [(x, y) for x in range(10, size[0]-10) for y in range(size[1])]
            
            if config == 2: # Variante 4-directions
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)
           
            if config == 3: # variante entrée à gauche sans sortie
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/left.json"), (0, 0), 1)
            
            if config == 4:
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/right.json"), (0, 0), 1)       

            if config == 5:
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/down.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/up.json"), (0, 0), 1)
                 
            if config == 6:
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/border.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/up.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/right.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/borders/left.json"), (0, 0), 2)
                collection.place_multidim_pattern(tiled_to_pattern("data/maps/structures/plain/grass/down.json"), (0, 0), 1)

            # Génération des arbres
            forbiden = get_pattern_overlap_offsets(tree_pattern[0]) # liste des positions autours de l'arbre dans lesquelles on ne peut pas placer d'arbre
            for i in range(random.randint(*tree_range)):
                pos = (random.randint(1, size[0]-3), random.randint(1, size[1]-4)) #on choisit une position aléatoire dans le terrain
                if not pos in forbiden_positions: # on vérifie qu'elle n'est pas occupée
                    collection.place_multidim_pattern(tree_pattern, pos, 2) # on place l'arbre
                    collection.place_pattern(tree_pattern[0], pos, 1.01)
                for pos_ in apply_offsets(pos, forbiden):
                    forbiden_positions.append(pos_) # on ajoute les positions bannies à la liste

    return collection
