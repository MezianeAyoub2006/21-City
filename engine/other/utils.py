def generate_screen_positions(tile_size, camera, screen_size):
    for x in range(int(camera[0] // tile_size), int((camera[0] + screen_size[0]) // tile_size + 1)):
        for y in range(int(camera[1] // tile_size), int((camera[1] + screen_size[1]) // tile_size + 1)):
            yield (x, y)