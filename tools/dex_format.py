"""
Outil chargé de re-formater le fichier dex.json en y 
modifiant les valeurs pour le rendre traitable par le
jeu.
"""


import json

PATH = "pokemon_data/dex.json"

with open(PATH, "r", encoding="utf-8") as file:
    dex = json.load(file)

for i in range(len(dex)):
    dex[i]["id"] = i + 1
    for j in range(len(dex[i]["type"])):
        dex[i]["type"][j] = dex[i]["type"][j].lower()
    try:
        del dex[i]["name"]["japanese"]
        del dex[i]["name"]["chinese"]
    except KeyError:
        pass

with open(PATH, "w", encoding="utf-8") as file:
    json.dump(dex, file, indent=4)

