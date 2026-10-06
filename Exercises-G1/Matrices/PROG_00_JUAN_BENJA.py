"""tamaño = int(input("ingrese el tamaño de la matriz :"))"""

matriz = []

for i in range(tamaño):
    matriz.append([])
    for j in range(tamaño):
        matriz[i].append(int(input("numero: ")))
        
for i in matriz:
    for j in i:
        print(j, end=" ")
    print()


esmagico = True

for fila in range(len(matriz)):
        target = 0
        contador = 0
        for columna in range(len(matriz)):
            contador += matriz[fila][columna]
        target = contador
        print(target)
        print(esmagico)

        for fila in range(len(matriz)):
            contador = 0
            for columna in range(len(matriz)):
                contador += matriz[columna][fila]
            if contador == target:
                continue
            else:
                esmagico = False 
        print(esmagico)
        contador = 0 
        for fila in range(len(matriz)):
            for columna in range(len(matriz)):
                if columna == fila:
                    contador += matriz[columna][fila]
        if contador == target:
            continue
        else:
            esmagico = False
        print(esmagico)
        
        contador = 0
        for fila in range(len(matriz)):
            for columna in range(len(matriz)):
                if columna+fila == 2:
                    contador += matriz[columna][fila]
        if contador == target:
            continue
        else:
            esmagico = False
        print(esmagico)
        
                
if esmagico == True:
    print("es magico")
else:
    print("no es magico")

