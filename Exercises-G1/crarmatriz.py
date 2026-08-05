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


