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
CALIDAD = ("nuevo","como nuevo","usado")
ANIO = (2000,2026)

def informe_autos(
    ruta_archivo : str, cant_autos : int
) -> dict[dict]:
    letras = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
    numeros = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

    preset = {
        2016: ["AA"],
        2017: ["AB"],
        2018: ["AC", "AD"],
        2019: ["AD","AE"],
        2020: ["AE"],
        2021: ["AE", "AF"],
        2022: ["AF"],
        2023: ["AG"],
        2024: ["AG", "AH"],
        2025: ["AH"],
        2026: ["AI"]
    }
    categorías = {
                    "sedan_hatchback" : ["etios", "yaris", "corolla", "clio", "sandero", 
                                        "argo", "cronos", "206", "208", "408", "onix", "cruze"],
                    "suv_crossover" : ["rav4", "kardian", "duster", "pulse",
                                    "fastback", "2008", "3008", "tracker"],
                    "pickup" : ["hilux", "toro", "montana"],
            
                    "monovolumen_mpv" : ["kangoo", "spin"]
                }
    listado = {}
    cant_autos = 25
    for _ in range(1, cant_autos + 1):
        
        anio = random.randint(ANIO[0],ANIO[1])
        patente = ""
        #  Patentes mayores o iguales a 2016
        if anio >= 2016:
            patente += random.choice(preset[anio])
            for i in range(5):
                if i <= 2:
                    patente += random.choice(numeros)
                else:
                    patente += random.choice(letras)
            patente = patente.upper()
        #  Patentes menores a 2016
        else:
            patente = ""
            contador = 1
            for _ in range(6):
                if contador <= 3:
                    patente += (random.choice(letras))
                    contador += 1
                elif contador > 3 :
                    patente += (random.choice(numeros))
                    contador += 1
            patente = patente.upper()
        precio = 90
        if anio < 2026:
            a = 2026 - anio
            precio = precio -(a*2)
        marca = random.choice(MARCAS)
        modelo = random.choice(AUTOS[marca])        
        listado[patente] = {
            "marca" : marca,
            "modelo" : modelo,
            "calidad" : random.choice(CALIDAD),
            "año" : anio,
            "precio": precio,
            "categoria": [i for i in categorías if modelo in categorías[i]][0]
        }
    with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(listado, f, indent=4, ensure_ascii=False)
    print(
            f"\n/// Archivo '{ruta_archivo}' generado con éxito con {cant_autos} autos ///"
        )
    input("[Enter] ")
    return listado