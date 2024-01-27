import random, math

def range_list(list_):
    l = []
    for i in list_:
        l += list(range(i[0], i[1]+1))
    return l

def get_prob_value(values, probabilities):
    cumulative_prob = 0
    random_value = random.random()
    for value, prob in zip(values, probabilities):
        cumulative_prob += prob
        if random_value <= cumulative_prob:
            return value

def random_position_inside_circle(radius, center=(0, 0)):
    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(0, radius)
    x = center[0] + radius * math.cos(angle)
    y = center[1] + radius * math.sin(angle)
    return [x, y]

def direction(vector):
    angle = math.degrees(math.atan2(vector[1], vector[0]))
    angle += 360 if angle < 0 else 0
    directions = ["right", "down-right", "down", "down-left", "left", "up-left", "up", "up-right"]
    index = round(angle / 45) % 8 
    try:
        return directions[index]
    except:
        return "down"

def generate_room_path(line_count = 2):
    neighboors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    line_count = line_count
    positions = [(0, 0), (1, 0)]
    for i in range(line_count):
        random.shuffle(neighboors)
        for offset in neighboors:
            if not (positions[-1][0] + offset[0], positions[-1][1] + offset[1]) in positions:
                positions.append((positions[-1][0] + offset[0], positions[-1][1] + offset[1]))
    return positions 
