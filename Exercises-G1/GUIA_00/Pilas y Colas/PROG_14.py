"""
PROG_14: Un centro de logística recibe productos desde la línea de
producción. Algunos productos están en óptimo estado y otros presentan
fallas ("roto"). El sistema cuenta con dos camiones de transporte (Pila
Camión Sano y Pila Camión Defectuoso). Funciones a desarrollar:

    - clasificar_productos(pila_recepcion,camion_envio, defectuosos):

        1. Entrada: Una Pila de recepción con tuplas del tipo (id_producto, estado).

        2. Proceso: Vacía la pila de recepción desapilando elemento por elemento. Si el producto tiene estado "roto" o
            "defectuoso", lo apila en defectuosos. En caso contrario, lo apila en camion_envio.

        3. Retorno: Un resumen con la cantidad total de productos clasificados.
"""

def clasificar_productos(pila_recepcion):

    camion_envio = []
    camion_defectuoso = []

    while len(pila_recepcion) > 0:

        if pila_recepcion[0][1] == "correcto":
            camion_envio.append(pila_recepcion.pop(0)) #  Sacamos el siguiente elemento con la etiqueta "correcto"

        elif pila_recepcion[0][1] == "defectuoso":
            camion_defectuoso.append(pila_recepcion.pop(0)) #  Sacamos el siguiente elemento con la etiqueta "defectuoso"

    return camion_envio, camion_defectuoso #  Envío las dos listas juntas.

pila_recepcion = [
        (1, "correcto"),
        (2, "defectuoso"),
        (3, "defectuoso"),
        (4, "correcto"),
        (5, "defectuoso"),
        (6, "correcto"),
        (7, "correcto"),
        (8, "defectuoso"),
]

resultado = clasificar_productos(pila_recepcion) #  Regresa una tupla con las dos listas como elementos. 

print(f"\nProductos dentro del Camión Envío: {[i[0] for i in resultado[0]]}") #  Muestro los productos en buen estado.
print(f"Productos dentro del Camión Defectuoso: {[i[0] for i in resultado[1]]}\n") #  Muestro los productos defectuosos.