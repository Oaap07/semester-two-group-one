"""
PROG_01: Desarrollar un juego de mapa del tesoro. El jugador debe encontrar un
tesoro escondido en una matriz, con pistas limitadas Requisitos del
juego:
- Crear una matriz de tamaño n x n con números o símbolos (n es
ingresado por el usuario, se debe validar sea un entero).
- Colocar un “tesoro” al azar usando random.
- Dar al jugador una cantidad limitada de intentos para adivinar la
posición.
- En cada intento, el jugador ingresa coordenadas (fila, columna),
y se le dice si acertó o no. (validar enteros y que esté dentro
del rango de la matriz)
- Cuando el jugador acierte, debe mostrar por pantalla la matriz
con intentos y la cantidad de intentos realizados. El jugador debe
poder abandonar la partida.

"""

import random 

def crear_matriz():

    #  Creación de matrices
    matriz = []
    size = int(input("Ingrese los indices de la matriz: "))

    for i in range(size):
        matriz.append([])

    #  Colocación de carácteres de territorio en mapa: "+" = arena, "~" = agua
    for lista in matriz:
        for valor in range(len(matriz)):
            numero_aleatorio = random.randint(0, 2)
            if numero_aleatorio == 0:
                lista.append("~")
            elif numero_aleatorio > 0:
                lista.append("+")
    return matriz

def juego():
    coordenadas = [0, 0]
    aux = True
    #  Colocar el tesoro
    while aux:
        for i in range(len(coordenadas)):
            coordenadas[i] = random.randint(0, len(matriz)-1)

        if matriz[coordenadas[0]][coordenadas[1]] == "+":
            aux = False
        else:
            aux = True

    #  Jugador: Muestreo de matriz, petición de coordenadas y comparación
    print("\n¡Búsqueda del Tesoro!\n")
    for lista in matriz: 
        for valor in range(len(matriz)): 
            print(lista[valor], end=" ")
        print("")

    aux = len(matriz)
    while aux > 0:
        respuesta_usu = [int(i) for i in input(f"\nEncuentra el Tesoro, tienes {aux} intentos.\n--Ingrese las coordenadas: ").split()]
        if respuesta_usu == coordenadas:
            return "\n¡Felicidades! Tesoro encontrado 🪙\n"
        elif aux == 1 and coordenadas != respuesta_usu:
            return f"\n¡Perdiste! Respuesta: Suerte la próxima\n"
        else:
            print("Posición equivocada!")
            aux -= 1
        
matriz = crear_matriz()
print(juego())