import json

def list_to_matrix(list, xcount):
    matrix=[]
    for i in range(len(list)//xcount):
        matrix.append(list[i*xcount: (i+1)*xcount])
    return matrix

def tiled_to_pattern(path):
    pattern = []
    with open(path, "r") as file:
        data = json.load(file)
    for layer in data["layers"]:
        modified_layer = [None if i == 0 else i-1 for i in layer["data"]]
        pattern.append(list_to_matrix(modified_layer, layer["width"]))
    return pattern
