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
    ruta_archivo : str = "autos.json", cant_autos : int = 10                 
):
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
    
    listado = {}
    cant_autos = 25
    for _ in range(1, cant_autos + 1):
        marca = random.choice(MARCAS)
        anio = random.randint(ANIO[0],ANIO[1])
        patente = ""
        #patentes mayores= a 2016
        if anio >= 2016:
            patente += random.choice(preset[anio])
            for i in range(5):
                if i <= 2:
                    patente += random.choice(numeros)
                else:
                    patente += random.choice(letras)
            patente = patente.upper()
        #patentes menores a 2016
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
        
        listado[patente] = {
            "marca" : marca,
            "modelo" : random.choice(AUTOS[marca]),
            "calidad" : random.choice(CALIDAD),
            "año" : anio,
            "precio": precio
        }
    with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(listado, f, indent=4, ensure_ascii=False)
    print(
            f"[alumnos_json.py] Archivo '{ruta_archivo}' generado con éxito con {cant_autos} alumnos.\n"
        )
    return listado

if __name__ == "__main__":
    informe_autos()




