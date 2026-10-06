tamaño = int(input("ingrese el tamaño de la matriz :"))

matriz = []

for i in range(tamaño):
    matriz.append([])
    for j in range(tamaño):
        matriz[i].append(int(input("numero: ")))
        
for i in matriz:
    for j in i:
        print(j, end=" ")
    print()

def esmagica(matriz):
    for fila in range(len(matriz)):
        contador_filas = 0
        for columna in range(len(matriz)):
            contador_filas += matriz[fila][columna]
            
    for fila in range(len(matriz)):
        contador_columnas = 0
        for columna in range(len(matriz)):
            contador_columnas += matriz[columna][fila]
            
    contador_diagonal = 0
    for fila in range(len(matriz)):
        for columna in range(len(matriz)):
            if columna == fila:
                contador_diagonal += matriz[columna][fila]

    contador_invertida = 0
    for fila in range(len(matriz)):
        for columna in range(len(matriz)):
            if columna+fila == 2:
                contador_invertida += matriz[columna][fila]
                
    if contador_filas == contador_columnas and contador_filas == contador_diagonal and contador_filas == contador_invertida:
        print("es magica")
    else:
        print("no es magica")

esmagica(matriz)