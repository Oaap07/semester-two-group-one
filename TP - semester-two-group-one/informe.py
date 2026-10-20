"""
(TPO - SPRINT) - Programacion I
Facultad de Ingenieria Informatica

Modulo: informe.py - Constantes compartidas y precarga de datos.

Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).

Reune las constantes que usan los demas modulos (marcas, calidades, categorias,
años, rutas de los JSON) y las funciones que generan la precarga inicial:

- informe_autos() .... genera un catalogo aleatorio de autos en autos.json.
- informe_usuarios() . crea usuarios.json con usuarios de ejemplo.
- limpiar() .......... limpia la consola segun el sistema operativo.

Los catalogos de apoyo (AUTOS, categorias_modelos, preset) relacionan cada marca
con sus modelos y cada año con el prefijo de patente que le corresponde.
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
# Marcas disponibles: las claves del diccionario AUTOS.
MARCAS: tuple = tuple(AUTOS.keys())
# Calidades permitidas de un auto. Coinciden con las que precarga informe_autos().
CALIDADES: tuple = ("nuevo", "cuidado", "usado")
# Valores permitidos para el estado, como texto (los usa el CRUD al pedir el campo).
# Informe_autos guarda "estado" como booleano (True/False); esta tupla es la version
# en texto para las entradas del menu.
DISPONIBLE: tuple = ("true", "false")
# Rango de años permitidos (inclusive).
ANIOS: tuple = (2000, 2026)
# Categorias internas de los autos.
CATEGORIAS: tuple = ("sedan_hatchback", "suv_crossover", "pickup", "monovolumen_mpv")
# Prefijo/s de patente que corresponden a cada año (para años >= 2016).
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

# Rutas de los archivos de persistencia (catalogo de autos y usuarios).
RUTA_AUTOS_JSON: str = "autos.json"
RUTA_USUARIOS_JSON: str = "usuarios.json"

# Recaudacion acumulada de los alquileres (dias x precio diario). La actualiza
# rentar_auto() del menu; arranca en 0.
pozo: float = 0.0

# Alfabeto y digitos para armar las patentes al azar (mayores y menores a 2016).
letras: tuple = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o",
    "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]
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
) -> None:
    """
    Genera un catalogo aleatorio de autos y lo guarda en un archivo JSON.

    Si el archivo ya existe no lo toca: solo avisa por pantalla.

    Args:
        ruta_archivo (str): Ruta del archivo JSON a generar.
        cant_autos (int): Cantidad de autos a generar. La precarga usa un valor
            fijo de 25 registros.

    Returns:
        None
    """
    listado = {}
    # La precarga genera un catalogo fijo de 25 autos.
    cant_autos = 25
    # Se genera cada auto con patente, precio y atributos aleatorios.
    for _ in range(1, cant_autos + 1):
        anio = random.randint(ANIOS[0], ANIOS[1])
        patente = ""
        # Patentes de autos 2016 en adelante: prefijo por año + 3 numeros + 2 letras.
        if anio >= 2016:
            letras.remove("ñ")
            patente += random.choice(preset[anio])
            for i in range(5):
                if i <= 2:
                    patente += random.choice(numeros)
                else:
                    patente += random.choice(letras)
            patente = patente.upper()
            letras.append("ñ")
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
            # Descuenta 2.5 u$d por cada año de antiguedad.
            precio = precio - (a*2.5)
        marca = random.choice(MARCAS)
        modelo = random.choice(AUTOS[marca])

        listado[patente] = {
            "marca": marca,
            "modelo": modelo,
            "calidad": random.choice(CALIDADES),
            "año": anio,
            "precio": precio,
            # Comprension: busca en categorias_modelos la categoria a la
            # que pertenece el modelo elegido.
            "categoria": [i for i in categorias_modelos if modelo in categorias_modelos[i]][0],
            # Estado inicial: disponible (True).
            "estado": True
        }
    
    # Si el archivo ya existe no se regenera: solo se avisa. Si no existe, se crea.
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
    Crea el archivo de usuarios con usuarios de ejemplo precargados.

    Si el archivo ya existe no lo toca: solo avisa por pantalla. La precarga
    permite probar el ingreso y el registro sin crear usuarios a mano.

    Args:
        ruta_archivo (str): Ruta del archivo JSON de usuarios a generar.

    Returns:
        None
    """
    listado = {}

    # Si el archivo ya existe no se toca. Si no existe, se crea con la precarga.
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            print(f"___ Archivo [{ruta_archivo}] ya existente ___")
    except FileNotFoundError:
        # Usuarios de ejemplo (todos con clave "1234") para probar INGRESAR.
        listado["95823279"] = {
            "nombre" : "Jorge Adrian Gonzalez Padron",
            "clave" : "1234",
            "autos_rentados" : []
        }
        listado["4817866"] = {
                    "nombre" : "Benjamin Nahuel Baez",
                    "clave" : "1234",
                    "autos_rentados" : []
                }
        listado["46280291"] = {
                    "nombre" : "Juan Ignacio Cayla",
                    "clave" : "1234",
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
    # Punto de entrada: si se corre este archivo solo, genera la precarga inicial
    # (catalogo de autos y usuarios) y limpia la consola.
    limpiar()
    # Se capturan excepciones especificas; si falla la precarga se continua igual.
    try:
        informe_autos(RUTA_AUTOS_JSON, 25)
        print()
        informe_usuarios(RUTA_USUARIOS_JSON)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    limpiar()