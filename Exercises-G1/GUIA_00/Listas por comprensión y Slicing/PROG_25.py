"""
Se nos ha solicitado crear un programa que mediante el uso de
un conjunto de tuplas podamos identificar la posición de unas oficinas en
un mapa. El usuario podrá ingresar una nueva oficina cuyos valores son
ingresados por teclado como coordenada X e Y. Se almacenarán como una
tupla dentro del conjunto. Se deberá validar que no está dentro del
conjunto y de ser así se avisará al usuario que ese local ya fue
ingresado. Luego, mediante una función se avisará al usuario cuántas
oficinas se encuentran en la región norte, cuántas en la región este
cuántas en la región oeste, y cuántas en la región sur; para ello, tener
en cuenta que las coordenadas, cuando son ingresadas, son números
enteros naturales que van del 0 al 100. La coordenada X = 50, y = 50 es
el punto que divide norte de sur y este de oeste.
"""

def peticion_coordenadas():
    x = int(input("Ingrese coordenada 'x' (nums del 0 al 100): "))
    y = int(input("Ingrese coordenada 'y' (nums del 0 al 100): "))
    return (x, y)

def muestreo(oficinas):
    resultados = [0, 0, 0, 0] #  [norte, sur, este, oeste]
    for i in oficinas:
        if i[1] >= 50:
            resultados[0] += 1
        elif i[1] < 50:
            resultados[1] += 1
        if i[0] >= 50:
            resultados[2] += 1
        elif i[0] <= 50:
            resultados[3] += 1
    return resultados
        
oficinas = []
respuestas_si = ['Y', 'y']
respuestas_no = ['N', 'n']
flag = True 

while flag:
    respuesta = input("\nMenú de oficinas:\n-- ¿Quiere ingresar una nueva oficina? Y [si] / N [salir y mostrar]: ")
    if respuesta in respuestas_si:
        nueva_oficina = peticion_coordenadas()
        if nueva_oficina[0] in range(101) and nueva_oficina[1] in range(101) and nueva_oficina not in oficinas:
            oficinas.append(nueva_oficina)
        elif nueva_oficina in oficinas: print("Posición ocupada, vuelva a intentar...")
        else: print("¡Oficina fuera de rango! vuelva a intentar...")

    elif respuesta in respuestas_no:
        resultados = muestreo(oficinas)
        print(f"\nTotal de oficinas: {sum(resultados)//2}\n-- Región Norte: {resultados[0]}\n-- Región Sur: {resultados[1]}\n-- Región Este: {resultados[2]}\n-- Región Oeste: {resultados[3]}\n")
        flag = False
