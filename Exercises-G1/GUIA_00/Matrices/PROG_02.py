import os
os.system("cls")

def matriz_marco(n):

    """
    1. El Marco (matriz_marco)
    Escribe la función matriz_marco(n) que retorne una matriz con 1 en las
    celdas de los bordes exteriores y 0 en el interior.
    """
    #  Creación de matriz
    matriz = []

    #  Ingreso los 1 en los bordes
    for i in range(n):
        matriz.append([])

    for i in range(n):
        matriz[0].append(1)
        matriz[n-1].append(1)
        if i != 0 and i != (n - 1):
            for j in range(n):
                if j == 0:
                    matriz[i].append(1)
                elif j == (n-1):
                    matriz[i].append(1)
                else:
                    matriz[i].append(0)
    return matriz

def matriz_equis(n):

    #  Valido número impar
    while (n % 2) == 0:
        print("--Ingrese un número impar--")
        n = int(input("\nIngrese el valor de la matriz (Solo números impares): "))
    
    #  Creación de matriz
    matriz = []

    #  Ingreso los 1 de las diagonales con la condición de numeros pares
    for i in range(n):
            matriz.append([])
    
    for i in range(n):
        for j in range(n):
            if i == j:
                matriz[i].append(1)
            elif ((i + j) % 2) == 0:
                matriz[i].append(1)
            else:
                matriz[i].append(0)

    return matriz

def matriz_triangulo_superior_izq(n):
    #  Creación de matriz
    matriz = []

    #  Coloco los 1
    contador = n
    for i in range(n):
        matriz = []
        for j in range(contador):
            matriz[i].append(1)
        contador -= 1
            


def matriz_serpiente(n):
    print(n)

def matriz_tablero(n):
    print(n)

def matriz_diagonales(n):
    print(n)

aux = True
while aux:
    usuario = int(input("\nEscoja una opción: \n1- Matriz Marco\n2- Matriz Equis\n" \
    "3- Matriz Triangulo Superior Izquierda\n4- Matriz Tablero\n5- Matriz Diagonales\n0- EXIT\n\n ---Respuesta: "))
    if usuario == 1:
        matriz = matriz_marco(int(input("\nIngrese el valor de la matriz: ")))
    elif usuario == 2:
        matriz = matriz_equis(int(input("\nIngrese el valor de la matriz (Solo números impares): ")))
    elif usuario == 3:
        matriz = matriz_triangulo_superior_izq(int(input("\nIngrese el valor de la matriz: ")))
    elif usuario == 4:
        matriz = matriz_tablero(int(input("\nIngrese el valor de la matriz: ")))
    elif usuario == 5:
        matriz = matriz_diagonales(int(input("\nIngrese el valor de la matriz: ")))
    elif usuario == 0:
        aux = False
    if usuario > 0:
        print()
        for i in matriz:
            for j in i:
                print(j, end=" ")
            print()
        print()
        input("Presione ENTER para continuar ")
    os.system("cls")