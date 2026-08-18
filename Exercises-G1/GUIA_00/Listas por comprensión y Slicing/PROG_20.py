import random
mapa = [[random.randint(1,4) for i in range(10)]for i in range(10)]
valor_valido = True

while valor_valido:
    x = int(input("Ingrese coordenada x: "))
    y = int(input("Ingrese coordenada y: "))
    if x > 7 or y > 7 :
        print("Esta fuera de rango del telescopio")
    else:
        valor_valido = False
        sub_mapa = [fila[x:x+3] for fila in mapa[y:y+3]]
        for fila in mapa: print(fila)
        print()
        for fila in sub_mapa: print(fila)
        contador_asteroides = 0
        for fila in sub_mapa:
            for valor in fila:
                if valor == 3:
                    contador_asteroides += 1
        if contador_asteroides > 0:
            print(f"Se encontraron {contador_asteroides} asteroides.")
        else:
            print("No se encontraron asteroides.")
