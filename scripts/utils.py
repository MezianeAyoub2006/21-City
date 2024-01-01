import random, math, heapq

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
    angle += 360 if angle < 0 else 0  # Ensure the angle is positive
    directions = ["right", "down", "left","up"]
    index = round(angle / 90) % 4  
    return directions[index]

