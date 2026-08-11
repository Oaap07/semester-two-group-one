

import random 

def generar_paquete():
    paquete = random.randint(10,41)
    return paquete

def cargar_vagon(n):
    tren = []
    for i in range(n):
        tren.append([])
    peso = 0
    while peso < 150:
        paquete = generar_paquete()
        peso += paquete
        if peso < 150:
            tren[i].append(paquete)

    return tren

tren = cargar_vagon(3)
print(tren)
