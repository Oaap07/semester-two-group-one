import json

with open("autos.json", 'r', encoding="utf-8") as archivo:
            lista = json.load(archivo)

print(type(lista["ZOB165"]["estado"]))
print(lista["ZOB165"]["estado"] == True)