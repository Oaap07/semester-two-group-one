import json


with open("autos.json", 'r', encoding="utf-8") as archivo:
        lista = json.load(archivo)
for k in lista.keys():
    dicts = lista[k]
    for k,v in dicts.items():
          print(k, v)