"""PROG_41: Implementar un sistema CRUD para gestionar el archivo cosecha.json.
1. Crear (Agregar): Solicitar la clave única del registro (ej.REG_011). Validar que la clave NO exista antes de agregar.
Pedir datos numéricos validando con try-except (ValueError) y guardaren el archivo JSON.

2. Leer (Ver todos): Cargar el archivo con try-except (FileNotFoundError) y mostrar los registros en pantalla

3. Editar (Actualizar peso): Pedir la clave del registro.
Validar que la clave SÍ exista. Si existe, solicitar el nuevo peso y actualizar el archivo.

4. Eliminar: Pedir la clave del registro.
Validar que la clave SÍ exista, eliminarla del diccionario y guardar los cambios."""

import json
import random

def obtener_dias_mes(mes: int) -> int:
    if mes == 2:
        return 28
    elif mes in (4, 6, 9, 11):
        return 30
    return 31

def generar_cosecha_json(ruta_archivo: str = "cosecha.json", cantidad_registros: int= 10) -> None:
    cosecha_dict = {}
    for i in range(1, cantidad_registros + 1):
        clave = f"REG_{i:03d}"
        mes = random.randint(1, 12)
        cosecha_dict[clave] = {
        "id_arbol": random.randint(1, 100),
        "mes": mes,
        "dia": random.randint(1, obtener_dias_mes(mes)),
        "peso": random.randint(100, 600)
        }
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(cosecha_dict, f, indent=4)
print(f"[manzanas_json.py] Archivo '{ruta_archivo}' generado con éxito.\n")
