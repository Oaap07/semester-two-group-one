import json
import random
import os

AUTOS : dict[tuple] = {
    "toyota": ("etios", "yaris", "hilux", "corolla", "rav4"),
    "renault": ("kardian", "clio", "kangoo", "sandero", "duster"),
    "fiat": ("cronos", "fastback", "argo", "pulse", "toro"),
    "peugeot": ("208", "3008", "2008", "408", "206"),
    "chevrolet": ("cruze", "onix", "spin", "tracker", "montana")
}
MARCAS: tuple = tuple(AUTOS.keys())
CALIDADES: tuple = ("nuevo", "como nuevo", "usado")
DISPONIBLE: tuple = (True, False)
ANIOS: tuple = (2000, 2026)
CATEGORIAS: tuple = ("sedan_hatchback", "suv_crossover", "pickup", "monovolumen_mpv")
preset: dict = {
    2016: ["AA"],
    2017: ["AB"],
    2018: ["AC", "AD"],
    2019: ["AD", "AE"],
    2020: ["AE"],
    2021: ["AE", "AF"],
    2022: ["AF"],
    2023: ["AG"],
    2024: ["AG", "AH"],
    2025: ["AH"],
    2026: ["AI"]
}

categorias_modelos: dict = {
    "sedan_hatchback": [
        "etios", "yaris", "corolla", "clio", "sandero",
        "argo", "cronos", "206", "208", "408", "onix", "cruze"
    ],
    "suv_crossover": [
        "rav4", "kardian", "duster", "pulse",
        "fastback", "2008", "3008", "tracker"
    ],
    "pickup": ["hilux", "toro", "montana"],
    "monovolumen_mpv": ["kangoo", "spin"]
}

RUTA_AUTOS_JSON: str = "autos.json"
RUTA_USUARIOS_JSON : str = "usuarios.json"

letras: tuple = (
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o",
    "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
)
numeros: tuple = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")


def limpiar():
    """
    Limpia la consola segun el sistema operativo.

    En Windows usa 'cls'; en Linux/macOS usa 'clear'. Sirve para mantener la
    interfaz ordenada entre pantallas del menu.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def informe_autos(
    ruta_archivo: str, cant_autos: int
) -> dict:
    """
    Genera un conjunto aleatorio de autos y lo guarda en un archivo JSON.

    Args:
        ruta_archivo (str): Ruta del archivo JSON a generar.
        cant_autos (int): Cantidad de autos a generar.

    Returns:
        dict: Diccionario con el listado de autos generado.
    """
    listado = {}
    cant_autos = 25
    for _ in range(1, cant_autos + 1):
        anio = random.randint(ANIOS[0], ANIOS[1])
        patente = ""
        # Patentes mayores o iguales a 2016
        if anio >= 2016:
            patente += random.choice(preset[anio])
            for i in range(5):
                if i <= 2:
                    patente += random.choice(numeros)
                else:
                    patente += random.choice(letras)
            patente = patente.upper()
        # Patentes menores a 2016
        else:
            patente = ""
            contador = 1
            for _ in range(6):
                if contador <= 3:
                    patente += (random.choice(letras))
                    contador += 1
                elif contador > 3:
                    patente += (random.choice(numeros))
                    contador += 1
            patente = patente.upper()
        precio = 90

        if anio < 2026:
            a = 2026 - anio
            precio = precio - (a*2.5)
        marca = random.choice(MARCAS)
        modelo = random.choice(AUTOS[marca])

        listado[patente] = {
            "marca": marca,
            "modelo": modelo,
            "calidad": random.choice(CALIDADES),
            "año": anio,
            "precio": precio,
            "categoria": [i for i in categorias_modelos if modelo in categorias_modelos[i]][0],
            "estado": DISPONIBLE[0]
        }
    
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            print(f"___ Archivo [{ruta_archivo}] ya existente ___")
    except FileNotFoundError:
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(listado, f, indent=4, ensure_ascii=False)
            print(f"||| Archivo [{ruta_archivo}] creado exitosamente |||")

    try: input("[Enter] ")
    except: pass

    return


def informe_usuarios(
    ruta_archivo: str) -> dict:
    """
    Hace un conjunto vacío y lo guarda en un JSON

    Args:
        ruta_archivo: Dirección donde se guardará el diccionario

    Returns:
        dict: Diccionario sin usuarios
    """

    listado = {}
    
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            print(f"___ Archivo [{ruta_archivo}] ya existente ___")
    except FileNotFoundError:
        listado["10101010"] = {
            "nombre" : "Jorge",
            "clave" : "1010",
            "autos_rentados" : []
        }
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(listado, f, indent=4, ensure_ascii=False)
            print(f"||| Archivo [{ruta_archivo}] creado exitosamente |||")

    try:
        input("[Enter] ")
    except:
        pass
    return


if __name__ == "__main__":
    limpiar()
    try:
        # Intento de generar un informe inicial al arrancar el programa.
        # TODO(TP - Req 1): usar manejo de excepciones especifico
        # (FileNotFoundError, JSONDecodeError) en lugar de 'except' generico.
        informe_autos(RUTA_AUTOS_JSON, 25)
        print()
        informe_usuarios(RUTA_USUARIOS_JSON)
    except:
        # Si falla (archivo faltante, formato invalido, etc.) se continua igual.
        pass
    limpiar()