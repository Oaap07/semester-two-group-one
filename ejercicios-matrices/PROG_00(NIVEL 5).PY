

def matriz_tablero(n):
    matriz = []
    contador = 1
    for i in range(n):
        matriz.append([])
        for j in range(n):
            if (i + j) % 2 == 0:
                matriz[i].append(contador)
            else:
                matriz[i].append(0)
                contador += 1
    
    for i in matriz:
        for j in i:
            print(j, end=" ")
        print()


n = int(input("Ingrese el tamaño de la matriz: "))
matriz_tablero(n)