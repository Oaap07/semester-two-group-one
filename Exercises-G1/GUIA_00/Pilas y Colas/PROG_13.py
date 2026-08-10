"""
PROG_13: En la bodega de un avión, las valijas se apilan en dos filas
paralelas (Pila A y Pila B). Cada valija tiene un código de etiqueta
único. Cuando un pasajero reclama una valija por su código, el operario
debe retirarla. Sin embargo, como están apiladas, para sacar una valija
que está abajo, primero se deben desapilar temporalmente las que están
arriba. Función a desarrollar

- buscar_y_extraer_maleta(pila_a, pila_b, etiqueta_buscada):

Entrada: Dos listas (pila_a y pila_b) y la etiqueta
(string/int) de la maleta buscada.

Proceso: Busca la maleta en la pila_a. Si no está, busca en
la pila_b. Utiliza una pila auxiliar para guardar
temporalmente las maletas que están encima de la buscada.
Una vez extraída la maleta solicitada, se devuelven las
demás a su pila original en el orden correcto.

Retorno: True si la maleta fue encontrada y extraída, False
si no existía en ninguna de las dos filas.
"""

#  Creación de listas (pilas)
pila_a = ["#05", "#04", "#09", "#07"]
pila_b = ["#01", "#06", "#02", "#03", "#08"]


def buscar_y_extraer_maleta(pila_a, pila_b, etiqueta): #  Función que resibe las 2 pilas y etiqueta.
    pila_aux = []

    for i in range(len(pila_a)): #  for que analiza, las veces de la longitud de la pila 'a', si el último valor es igual a la etiqueta.
        if pila_a[-1] == etiqueta:
            pila_a.pop() #  Extrae maleta con la etiqueta.
            for i in range(len(pila_aux)): #  Proceso de reposición de maletas.
                    pila_a.append(pila_aux.pop()) 
            return "TRUE. Etiqueta extraída con éxito!"
        else:
            pila_aux.append(pila_a.pop())

    for i in range(len(pila_aux)): #  Proceso de reposición de maletas si la pila 'a' no tiene la etiqueta
        pila_a.append(pila_aux.pop())

    for i in range(len(pila_b)): #  for que analiza, las veces de la longitud de la pila 'b', si el último valor es igual a la etiqueta.
        if pila_b[-1] == etiqueta:
            pila_b.pop() #  Extrae maleta con la etiqueta.
            for i in range(len(pila_aux)): #  Proceso de reposición de maletas.
                    pila_b.append(pila_aux.pop()) 
            return "TRUE. Etiqueta extraída con éxito!"
        else:
            pila_aux.append(pila_b.pop())

    for i in range(len(pila_aux)): #  Proceso de reposición de maletas si la pila 'a' no tiene la etiqueta
        pila_b.append(pila_aux.pop())

    return "FALSE. Etiqueta inexistente"

print(f"\nPila 'A' {pila_a}\nPila 'B' {pila_b}\n") #  Muestro las pilas
resultado = buscar_y_extraer_maleta(pila_a, pila_b, etiqueta=input("Ingrese la etiqueta a buscar: ")) #  Lo que devuelva la función se guarda en resultado.
print(f"\n{resultado}\nPila 'A' {pila_a}\nPila 'B' {pila_b}")  #  Imprimo el resultado general.