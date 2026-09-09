"""
PROG_31: Una empresa frutícola nos solicita crear un simulador de
cosecha de manzanas en memoria. Debemos construir un módulo llamado
manzanas.py que contenga la lógica de generación de datos y cálculo de
métricas, y un programa principal main.py que lo invoque y muestre un
informe por pantalla. Requerimientos del módulo manzanas.py:

1. obtener_dias_mes(mes: int) -> int: Función auxiliar que retorne
la cantidad máxima de días de un mes (Febrero = 28; Abril, Junio,
Septiembre, Noviembre = 30; el resto = 31).

2. generar_cosecha(cantidad_registros: int) -> list[dict]: Genera
una lista de diccionarios que simulan manzanas cosechadas. Cada
diccionario tendrá la estructura:
 - peso: Entero aleatorio entre 100 y 600 gramos.
 - id_arbol: Entero aleatorio de 1 a 100 (representa los 100 árboles del campo).
 - mes: Entero aleatorio entre 1 y 12.
 - dia: Entero aleatorio entre 1 y la cantidad máxima de días
de ese mes.

3. calcular_totales(cosecha: list[dict]) -> dict: Retorna un
diccionario con el peso total en kg cosechados y la cantidad total
de registros procesados.
"""

