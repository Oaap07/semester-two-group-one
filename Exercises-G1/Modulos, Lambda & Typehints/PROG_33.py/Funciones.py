"""
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

def obtener_catalogo_inicial() -> list[dict]:
 """Retorna el catalogo por defecto de plantas en el vivero."""
 return [
 {"id": 1, "nombre": "Albahaca", "precio": 1200.0, "dias_sin_regar": 3, "frecuencia_riego_dias": 2},
 {"id": 2, "nombre": "Menta", "precio": 1500.0, "dias_sin_regar": 1, "frecuencia_riego_dias": 2},
 {"id": 3, "nombre": "Lavanda", "precio": 2800.0, "dias_sin_regar": 5, "frecuencia_riego_dias": 4},
 {"id": 4, "nombre": "Romero", "precio": 2100.0, "dias_sin_regar": 2, "frecuencia_riego_dias": 5},
 {"id": 5, "nombre": "Manzanilla", "precio": 1100.0, "dias_sin_regar": 4, "frecuencia_riego_dias": 3},
 ]

def aplicar_aumento_precios(catalogo: list[dict], porcentaje: float) -> list[dict]:
    """Aplica un incremento porcentual al precio de cada planta."""
    # TODO: Recorrer el catalogo y actualizar el campo 'precio' aumentando un 'porcentaje' %
    for planta in catalogo:
        planta["precio"] += planta["precio"] * (porcentaje/100)
    return catalogo

def obtener_plantas_para_regar(catalogo: list[dict]) -> list[dict]:
    """Retorna aquellas plantas que superaron o igualaron sus dias de riego limite."""
    # TODO: Filtrar las plantas donde dias_sin_regar >= frecuencia_riego_dias
    return [planta for planta in catalogo if planta["dias_sin_regar"] >= planta["frecuencia_riego_dias"]]
