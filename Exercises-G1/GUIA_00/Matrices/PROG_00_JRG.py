"""
Un cuadrado mágico es una matriz cuadrada en la que la suma de
los números en todas las filas, todas las columnas y la diagonal
principal es siempre la misma.
"""
def crear_matriz():
    matriz = []
    tamaño = int(input("Ingrese el tamaño de su matriz: "))

    #  Creación de matriz
    for i in range(tamaño):
        matriz.append([])
        matriz[i] = (input(f"Ingrese los {tamaño} numeros de la fila n°{i}: ").split())

    #  Completo los valores faltantes con 0
    for i in matriz:
        if len(i) < len(matriz):
            faltante = len(matriz) - len(i)
            for j in range(faltante):
                i.append(0)

    #  Conversión a enteros y muertreo de matriz
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz[i][j] = int(matriz[i][j])
            print(matriz[i][j], end=" ")
        print("")
    return matriz



def sumas():
    comprobatoria = []
    aux = 0

    for i in range(len(matriz)):
    #Suma de filas
        comprobatoria.append(sum(matriz[i]))

    #Suma de columnas
        for j in range(len(matriz[i])):
            aux += matriz[j][i]
        comprobatoria.append(aux)
        aux = 0

    #Suma de diagonales
    #  1ra diagonal
    for i in range(len(matriz)):
        aux += matriz[i][i]
    comprobatoria.append(aux)
    aux = 0

    #  2da diagonal
    for i in range(len(matriz[i])):
        for j in range(len(matriz[i])):
            if (i + j) == (len(matriz[i])-1):
                aux += matriz[i][-1]
    comprobatoria.append(aux)
    aux = 0
    
    print(comprobatoria)
    for i in comprobatoria:
        if i != aux and aux != 0:
            return "No es mágica"
        aux = i
    return "Es mágica"

matriz = crear_matriz()
print(sumas())