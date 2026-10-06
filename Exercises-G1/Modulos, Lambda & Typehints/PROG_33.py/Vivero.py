"""
PROG_33: Un vivero necesita un sistema para administrar el catálogo de
sus plantas aromáticas y ornamentales, permitiendo actualizar precios
por inflación y detectar qué especies requieren riego inmediato.

1. obtener_catalogo_inicial() -> list[dict]: Devuelve una lista base con al menos 5 plantas. Cada planta se representa como:
    o id: Entero identificador.
    o nombre: Cadena (ej. "Albahaca", "Menta", "Lavanda").
    o precio: Float.
    o dias_sin_regar: Entero.
    o frecuencia_riego_dias: Entero (cada cuántos días debe regarse).

2. aplicar_aumento_precios(catalogo: list[dict], porcentaje: float)
-> list[dict]: Modifica o genera un catálogo actualizado donde el
precio de cada planta se incrementa según el porcentaje indicado.

3. obtener_plantas_para_regar(catalogo: list[dict]) -> list[dict]:
Filtra y retorna las plantas cuyo dias_sin_regar sea igual o mayor
a su frecuencia_riego_dias.
"""

import Funciones as f

def __main__():

    catalogo = f.obtener_catalogo_inicial()


if __name__ == "__main__":
    __main__()

