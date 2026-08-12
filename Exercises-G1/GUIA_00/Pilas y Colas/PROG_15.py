"""
PROG_15: Un tren de mercancías está compuesto por una lista de vagones.
Cada vagón funciona como una pila con una capacidad máxima de peso (en kg). 
A medida que llegan paquetes con pesos aleatorios, se deben apilar
en el vagón actual. Cuando el siguiente paquete supere la capacidad
restante del vagón, ese vagón se "sella" y se debe pasar al siguiente
vagón (siguiente pila). Funciones a desarrollar:

    1. generar_paquete(peso_min, peso_max): Función que retorna
    aleatoriamente el peso de un paquete a cargar. Recomendación: 
    Los paquetes pesan entre 10 y 40.

    2. cargar_vagon(tren, vagón_numero, paquete): Función que retorna la
    información del tren una vez terminada la carga del vagón.
    Recibe como parámetro la “matriz”
    (dado que el tren representa la matriz y cada fila los vagones del tren), 
    la posición actual para la carga 
    (como recomendación, siempre se puede trabajar con la última posición dependiendo de como se construya el programa principal)
    y una tupla compuesta de información del paquete y el peso. El vagón tiene un límite de 150.

    3. Mostrar(tren): Mostrar informe de carga
"""
import random 

def generar_paquete(min, max):
    paquete = (id_producto, random.randint(min, max))
    return paquete

def cargar_vagon(tren, n, paquete):

    for i in matriz:
        peso_vagon = 0
        for j in i:
            peso_vagon += j[1]
        
    if len(tren) == 0 or ((peso_vagon + paquete[1]) >= 150 and len(matriz) < vagones):
        tren.append([])
    elif len(matriz) == vagones and (peso_vagon + paquete[1]) >= 150:
        return tren, -1
    
    tren[n].append(paquete)

    return tren, id_producto

vagones = int(input("Ingrese la cantidad de vagones: "))
matriz = []
id_producto = 0

while id_producto != -1: #  id_producto se usa como índice de productos y como flag

    id_producto += 1
    paquete = generar_paquete(10, 41) #  Se llama a la función generar_paquete con los límites de peso de los paquetes
    matriz, id_producto = cargar_vagon(matriz, -1, paquete) #  Mandamos una matriz vacía (tren) y un número ingresado para la cantidad de "vagones" (n).


#  Sección únicamente de Muestro
print()
for i in matriz:
    print(f"Vagón[{matriz.index(i)+1}] | Pesa: {sum([j[1] for j in i])} kg")
print()
[print(i) for i in matriz]