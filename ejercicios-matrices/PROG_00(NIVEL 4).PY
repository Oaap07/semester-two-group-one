

def matriz_serpiente(n):
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n):
            if i % 2 == 0:
                fila.append(i * n + j + 1)
            else:
                fila.append(i * n + (n - j))
        matriz.append(fila)
    for i in range(n):
        for j in range(n):
            print(matriz[i][j], end=" ")
        print()
    return matriz   



n = int(input("Ingrese el tamaño de la matriz: "))
matriz_serpiente(n)