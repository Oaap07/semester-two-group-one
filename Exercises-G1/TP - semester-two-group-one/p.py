import json
import random

AUTOS = {
    "toyota":("etios","yaris","hilux","corolla","rav4"),
    "renault":("kardian","clio","kangoo","sandero","duster"),
    "fiat":("cronos","fastback","argo","pulse","toro"),
    "peugeot":("208","3008","2008","408","206"),
    "chevrloet":("cruze","onix","spin","tracker","montana")
}
MARCAS = tuple(AUTOS.keys())
ESTADO = ("nuevo","como nuevo","usado")
ANIO = (2000,2026)



listado = {}
cant_autos = 3
for i in range(1, cant_autos + 1):
    clave = str(i)
    marca = random.choice(MARCAS)
    listado[clave] = {
        "marca" : marca,
        "modelo" : random.choice(AUTOS[marca]),
        "estado" : random.choice(ESTADO),
        "año" : random.randint(ANIO[0],ANIO[1]) 
    }
print(listado)