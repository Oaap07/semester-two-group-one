"""
PROG_26: Utilizando listas, tuplas y conjuntos, crear un programa que
genere todas las fichas de un dominó. Cada ficha individual será una
tupla contenida dentro de un conjunto que es el total de las fichas.
Crear un método que seleccione aleatoriamente dos fichas, las imprima y
mediante una validación imprima por pantalla si esas dos fichas
“encajan.” Ejemplo: La ficha (1,2) encaja con (3,2) pero no con (3,3).
"""

import random as rd

#  PASO 1: Generar fichas aleatorias y almacenarlas en un conjunto

n = 6
fichas = set()

for i in range(n+1):
    for j in range(n+1):
        if (j, i) not in fichas:
            fichas.add((i, j))

#  PASO 2: Método de obtención aleatoria de 2 fichas e imprimirlas
ficha_1, ficha_2 = 0, 0

while ficha_1 == ficha_2:
    ficha_1 = rd.choice(list(fichas))
    ficha_2 = rd.choice(list(fichas))

print(f"\n- Ficha 1: {ficha_1}\n- Ficha 2: {ficha_2}")

#  PASO 3: Verificar si encajan
for i in ficha_1:
    if i in ficha_2:
        print(f"\n---Estas piezas ENCAJAN en [{i}]---\n")
        n = False
if n: print(f"\n---NO ENCAJAN---\n")