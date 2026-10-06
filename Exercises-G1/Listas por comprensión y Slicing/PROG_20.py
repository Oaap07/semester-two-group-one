import random
mapa = [[random.randint(1,4) for i in range(10)]for i in range(10)] #  Genero los valores dentro de cada posición de ma Matriz, [3] = asteroides
valor_valido = True # flag

while valor_valido:
    x = int(input("Ingrese coordenada x: ")) #  Pido coordenadas
    y = int(input("Ingrese coordenada y: "))
    if x > 7 or y > 7 : # Evalúo si se sale de rango
        print("Está fuera del rango del telescopio")
    else:
        valor_valido = False
        sub_mapa = [fila[x:x+3] for fila in mapa[y:y+3]] #  Genero la sub-matriz con agarrando las filas a partir de las columnas
        for fila in sub_mapa: print(fila) #  Muestro sub-matriz
        contador_asteroides = 0
        for fila in sub_mapa: #  Cuento asteroides
            for valor in fila:
                if valor == 3:
                    contador_asteroides += 1

        if contador_asteroides > 0: #  Muestro asteroides
            print(f"Se encontraron {contador_asteroides} asteroides.")
        else:
            print("No se encontraron asteroides.")
