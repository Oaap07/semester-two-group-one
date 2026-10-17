"""
Modulo: informe.py - Generacion de datos (precarga) e informes.

Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).
Reune constantes compartidas (marcas, categorias, rutas y campos permitidos) y
las funciones que generan el catalogo de autos y el archivo de usuarios.
"""

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
# Marcas disponibles: claves del diccionario AUTOS.
MARCAS: tuple = tuple(AUTOS.keys())
# Calidades permitidas de un auto.
# NOTA (dato desactualizado): los autos ya cargados en autos.json usan la
# calidad "como nuevo", que ya no figura aqui; validar con esta tupla rechaza
# ese valor.
CALIDADES: tuple = ("nuevo", "cuidado", "usado")
# Valores permitidos para el estado, como texto.
# NOTA (mezcla de tipos): informe_autos guarda "estado" como booleano (True),
# mientras que esta tupla (usada por el CRUD) usa los textos "true"/"false".
DISPONIBLE:tuple = ("true", "false")
# Rango de anios permitidos (inclusive).
ANIOS: tuple = (2000, 2026)
# Categorias internas de los autos.
CATEGORIAS: tuple = ("sedan_hatchback", "suv_crossover", "pickup", "monovolumen_mpv")
# Prefijos de patente que corresponden a cada anio (para anios >= 2016).
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

# Categoria -> modelos que pertenecen a esa categoria.
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

# Rutas de los archivos de persistencia (autos y usuarios).
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
    # NOTA (parametro ignorado): se fuerza la cantidad a 25, sin usar 'cant_autos'.
    cant_autos = 25
    # Genera cada auto: patente, precio y atributos aleatorios.
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
        # Precio base de 90 u$d, con descuento por antiguedad.
        precio = 90

        if anio < 2026:
            a = 2026 - anio
            # Baja 2.5 u$d por cada anio de antiguedad (la doc tecnica menciona 2).
            precio = precio - (a*2.5)
        marca = random.choice(MARCAS)
        modelo = random.choice(AUTOS[marca])

        listado[patente] = {
            "marca": marca,
            "modelo": modelo,
            "calidad": random.choice(CALIDADES),
            "año": anio,
            "precio": precio,
            # Lista por comprension: busca la categoria a la que pertenece el modelo.
            "categoria": [i for i in categorias_modelos if modelo in categorias_modelos[i]][0],
            # Estado inicial: disponible (True).
            "estado": True
        }
    
    try:
        # Si el archivo ya existe, no se regenera: solo se avisa.
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            print(f"___ Archivo [{ruta_archivo}] ya existente ___")
    except FileNotFoundError:
        # Si no existe, se crea con el listado generado.
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(listado, f, indent=4, ensure_ascii=False)
            print(f"||| Archivo [{ruta_archivo}] creado exitosamente |||")

    try: input("[Enter] ")
    except: pass

    return


def informe_usuarios(
    ruta_archivo: str) -> dict:
    """
    Hace un conjunto vacio y lo guarda en un JSON

    Args:
        ruta_archivo: Direccion donde se guardara el diccionario

    Returns:
        dict: Diccionario sin usuarios
    """

    # NOTA (docstring desactualizado): no crea un diccionario vacio; si el
    # archivo no existe, deja un usuario de ejemplo precargado.
    listado = {}
    
    try:
        # Si el archivo ya existe, no se toca.
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            print(f"___ Archivo [{ruta_archivo}] ya existente ___")
    except FileNotFoundError:
        # Usuario de ejemplo (dni 10101010) para poder probar INGRESAR.
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