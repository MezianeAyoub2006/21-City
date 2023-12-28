"""
Outil chargé de re-formater le fichier dex.json en y 
supprimant les caractères chinois et japonais puis en 
actualisant les "id" de chaque table de donnée.
"""


import json

PATH = "C:/Users/Karima Meziane/Desktop/Black Jack/pokemon_data/dex.json"

with open(PATH, "r", encoding="utf-8") as file:
    dex = json.load(file)

for i in range(len(dex)):
    dex[i]["id"] = i + 1
    try:
        del dex[i]["name"]["japanese"]
        del dex[i]["name"]["chinese"]
    except KeyError:
        pass

with open(PATH, "w", encoding="utf-8") as file:
    json.dump(dex, file, indent=4)

