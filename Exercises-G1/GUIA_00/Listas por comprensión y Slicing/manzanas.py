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
- id_arbol: Entero aleatorio de 1 a 100 (representa los 100
árboles del campo).
- mes: Entero aleatorio entre 1 y 12.
- dia: Entero aleatorio entre 1 y la cantidad máxima de días
de ese mes.

3. calcular_totales(cosecha: list[dict]) -> dict: Retorna un
diccionario con el peso total en kg cosechados y la cantidad total
de registros procesados.
"""
import random 
def obtener_dia_mes(numero):
    if numero == 2:
        dias = 28
    elif numero == 4 or numero == 6 or numero == 9 or numero == 11:
        dias = 30
    else:
        dias = 31
    return dias

def generar_cosecha(cantidad_registros):
    cosecha = []
    for i in range(cantidad_registros):
        mes = random.randint(1,12)
        dias = obtener_dia_mes(mes)

        manzana = {
            "Peso": random.randint(100,600),
            "id_arbol": random.randint(1,100),
            "mes": mes,
            "dia": random.randint(1,dias)
        }
        cosecha.append(manzana)
    return cosecha
def calcular_cosecha(cosecha):
    peso_total = 0
    cantidad_registros = 0
    for manzana in cosecha:
        peso_total += manzana["Peso"]
        cantidad_registros += 1
    return cantidad_registros,peso_total/1000