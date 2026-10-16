import usuarios as us
import json
import menu as m
with open("usuarios.json", 'r', encoding="utf-8") as archivo:
    lista = json.load(archivo)
usu_info = us.ingresa_usuario(lista)

print(usu_info)
print(type(usu_info))