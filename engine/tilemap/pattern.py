from numpy import array, int64, flip, rot90

def matrixflip(m, d):
    tempm = m.copy()
    if d=='h':
        for i in range(0,len(tempm),1):
                tempm[i].reverse()
    elif d=='v':
        tempm.reverse()
    return(tempm)

def get_pattern_steps(pattern_object):
    return (len(pattern_object[0]), len(pattern_object))

def get_pattern_overlap_offsets(pattern_object):
    overlap_offsets = []
    steps = get_pattern_steps(pattern_object)
    for x in range(-steps[0]+1, steps[0]):
        for y in range(-steps[1]+1, steps[1]):
            overlap_offsets.append((x, y))
    return overlap_offsets

def apply_offsets(position, offsets):
    rtrn = []
    for offset in offsets:
        rtrn.append((position[0]+offset[0], position[1]+offset[1]))
    return rtrn       

def pattern(py_array):
    return array(py_array, dtype=int64)                           

def flip_pattern(pattern_object, axis):
    return flip(pattern_object, {"h" : 1, "v" : 0}[axis])

def rotate_pattern(pattern_object, rotations):
    return rot90(pattern_object, rotations, (0, 1))