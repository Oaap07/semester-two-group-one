

import random

# =====================================================================
# CÓDIGO PREARMADO PARA EL ALUMNO (NO MODIFICAR)
# =====================================================================

def generar_sonar_6x6():
    """Genera una matriz de 6x6 con un perfil marino aleatorio."""
    matriz = []
    for i in range(6):
        fila = []
        for j in range(6):
            fila.append(0)
        matriz.append(fila)

    for col in range(6):
        inicio_fondo = random.randint(1, 5)
        for f in range(inicio_fondo, 6):
            matriz[f][col] = random.choice([1, 1, 2, 9])

    return matriz

def obtener_simbolo(valor):
    """Convierte el código numérico en su representación visual mediante condicionales simples."""
    if valor == 0:
        return " ~ "  # Agua
    elif valor == 1:
        return " . "  # Arena
    elif valor == 2:
        return " # "  # Roca
    elif valor == 9:
        return " X "  # Estructura / Naufragio
    else:
        return " ? "


def mostrar_sonar(matriz):
    """Muestra el barrido del sonar formateado en consola."""
    print("\n================ BARRIDO DEL SONAR (6x6) ================")
    print("Columnas (Camino) ->   0   1   2   3   4   5")
    print("---------------------------------------------------------")

    for i in range(6):
        linea = ""
        for j in range(6):
            val = matriz[i][j]
            simbolo = obtener_simbolo(val)
            linea = linea + simbolo
        print("Fila " + str(i) + " (Prof) | " + linea)

    print("---------------------------------------------------------")
    print("Simbología: [ ~ Agua ]  [ . Arena ]  [ # Roca ]  [ X Estructura ]\n")



def evaluar_recorrido_seguro(matriz, columna_destino, pos = 0, profundidad = 0):
    """Evalúa si el barco puede navegar de manera segura desde la columna 0
    
    hasta la columna_destino.

    Condición: TODAS las columnas del trayecto (0 a columna_destino) deben
    tener al menos 2 unidades de profundidad libre (celdas con 0).
    """
    camino_seguro = False
    fila = len(matriz)
    orilla = False
    if columna_destino == 0:
        camino_seguro = True
        orilla = True
    while pos != columna_destino and orilla == False:
        for i in range(fila):
            if(matriz[i][pos] == 0):
                profundidad += 1
            else:
                break
        if profundidad >= 2:
            pos += 1
            if(pos == columna_destino):
                camino_seguro = True
        else:
            camino_seguro = False
            break
        profundidad = 0

    if camino_seguro:
        print("se puede llegar")
    else:
        print("no se puede llegar")
    return camino_seguro


# =====================================================================
# PROGRAMA PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    navegando = True

    print("⚓ SISTEMA DE NAVEGACIÓN Y CONTROL DE SONAR INICIADO ⚓")

    while navegando:
        # Generamos y mostramos la lectura del sonar
        matriz = generar_sonar_6x6()
        mostrar_sonar(matriz)
        columna_destino = int(input("Hasta que columna desea avanzar: "))
        evaluar_recorrido_seguro(matriz, columna_destino)
        # TODO:
        # 1. Definir la función evaluar_recorrido_seguro(matriz, columna_destino)
        #    que verifique que TODAS las columnas desde la 0 hasta la columna_destino
        #    tengan al menos 2 celdas de agua (0) en la superficie.
        #
        # 2. Armar el programa principal con el bucle para pedir la columna destino.


