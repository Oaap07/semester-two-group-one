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

def informe_autos(
    ruta_archivo : str = "autos.json", cant_autos : int = 10    
):
    listado = {}
    cant_autos = 10
    for i in range(1, cant_autos + 1):
        clave = str(i)
        marca = random.choice(MARCAS)
        listado[clave] = {
            "marca" : marca,
            "modelo" : random.choice(AUTOS[marca]),
            "estado" : random.choice(ESTADO),
            "año" : random.randint(ANIO[0],ANIO[1]) 
        }
    with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(listado, f, indent=4, ensure_ascii=False)
    print(
            f"[alumnos_json.py] Archivo '{ruta_archivo}' generado con éxito con {cant_autos} alumnos.\n"
        )

if __name__ == "__main__":
    informe_autos()




