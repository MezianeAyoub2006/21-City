def generate_screen_positions(tile_size, camera, screen_size):
    for x in range(int(camera[0] // tile_size), int((camera[0] + screen_size[0]) // tile_size + 1)):
        for y in range(int(camera[1] // tile_size), int((camera[1] + screen_size[1]) // tile_size + 1)):
            yield (x, y)

def apply_offset(first_collection, second_collection):
    if len(first_collection) == len(second_collection):
        cp = list(first_collection)
        for idx, i in enumerate(second_collection):
            cp[idx] += i
        return tuple(cp)
    else:
        return first_collection
    
def apply_mul_offset(first_collection, second_collection):
    if len(first_collection) == len(second_collection):
        cp = list(first_collection)
        for idx, i in enumerate(second_collection):
            cp[idx] *= i
        return tuple(cp)
    else:
        return first_collection
    
