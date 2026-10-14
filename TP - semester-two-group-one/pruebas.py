import json

with open("autos.json", "r", encoding="utf-8") as archivo:
    dic = json.load(archivo)

for i in dic:
    print(dic[i]["marca"])
