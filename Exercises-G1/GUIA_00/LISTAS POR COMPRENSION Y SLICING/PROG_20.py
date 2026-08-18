"""
PROG_20: La estación aeroespacial necesita registrar la presencia de
asteroides en el sector galáctico asignado. Para simular el sensor,
contamos con una grilla de 10 × 10 donde cada celda representa un
elemento espacial según la siguiente simbología:

• 1: Planeta
• 2: Espacio vacío
• 3: Asteroide
• 4: Estrella

Debido a limitaciones de alcance, el telescopio solo puede enfocar un
cuadrante de 3 × 3 a partir de una coordenada inicial (X, Y) ingresada por
el operador. Funcionalidad del programa:

1. Generación del Mapa Espacial (Listas por Comprensión): Crea el
mapa de 10 × 10 inicializado con valores aleatorios entre 1 y 4.
Debe implementarse obligatoriamente utilizando listas por
comprensión y el módulo random.

2. Ingreso y Validación de Coordenadas: Solicita al operador que
ingrese las coordenadas X e Y (columna y fila) de la esquina
superior izquierda donde apuntará el telescopio. Validación:
Asumiendo entradas enteras, valida que los valores estén dentro
del rango permitido para que un cuadrante de 3 × 3 no exceda los
límites de la matriz (es decir, entre 0 y 7 usando índices 0-
based, o entre 1 y 8 en formato 1-based).

3. Captura del Telescopio (Slicing): Muestra por pantalla
únicamente la submatriz de 3 × 3 enfocada por el telescopio.
Utiliza slicing de Python para seleccionar las filas y columnas
correspondientes.

4. Detección de Asteroides (Listas por Comprensión): Analiza el
área capturada por el telescopio e informa al usuario si hay
asteroides (id: 3) presentes y cuántos se detectaron. Utiliza
listas por comprensión para el filtrado/conteo.
Tip: El siguiente código les orientará a entender cómo se pueden
utilizar listas por comprensión en matrices. La primera parte
construye una matriz de 10x10 y la segunda “recorta” en las
coordenadas x (de 1 a 3 inclusive) e y (de 2 a 4 inclusive)

import random
mapa = [[random.randint(1,4) for i in range(10)]for i in range(10)]
sub_mapa = [fila[1:4] for fila in mapa[2:5]]
for fila in mapa: print(fila)
for fila in sub_mapa: print(fila)
"""
import random
mapa = [[random.randint(1,4) for i in range(10)]for i in range(10)]

Valor_valido = True

while Valor_valido:
    x = int(input("Ingrese coordenada x: "))
    y = int(input("Ingrese coordenada y: "))
    if x > 7 or  y > 7:
        print("Esta fuera de rango")
    else:
        Valor_valido = False
        sub_mapa = [fila[x:x+3] for fila in mapa[y:y+3]]
        for fila in mapa: print(fila)
        print()
        for fila in sub_mapa: print(fila)
        contador_asteroides = 0
        for fila in sub_mapa:
            for valor in fila:
                if valor == 3:
                    contador_asteroides += 1
        if contador_asteroides > 0:
            print(f"Se encontraron {contador_asteroides} asteroides.")
        else:
            print("No se encontraron asteroides.")


