pila_desordenada = [42, 815, 17 ,934 ,63 ,208 ,51 ,7 ,392 ,114]
pila_aux = []
pila_ordenada = []

while (len(pila_desordenada) + len(pila_aux)) != 0:

    pila_ordenada.append(pila_desordenada.pop())

    while len(pila_desordenada) > 0:
        if pila_ordenada[-1] > pila_desordenada[-1]:
            pila_aux.append(pila_desordenada.pop())
        else:
            pila_aux.append(pila_ordenada.pop())
            pila_ordenada.append(pila_desordenada.pop())

    for i in range(len(pila_aux)):
        pila_desordenada.append(pila_aux.pop())

print(pila_desordenada)
print(pila_aux)
print(pila_ordenada)