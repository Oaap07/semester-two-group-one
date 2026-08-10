

def matriz_equis(n):
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n):
            if i == j or i + j == n - 1:
                fila.append("1")
            else:
                fila.append("0")
        matriz.append(fila)
    for i in matriz:
        print(" ".join(i))
    return matriz

n = int(input("Ingrese el tamaño de la matriz: "))
matriz_equis(n)