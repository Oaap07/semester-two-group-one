"""
PROG_24: Tomando como referencia el programa anterior construir un
programa similar que tenga las siguientes características:
- Ingresar números enteros naturales a un primer conjunto llamado
conjunto ‘A’
- Ingresar números en un conjunto ‘B’
- Ver la Unión de los conjuntos A - B
- Ver la intersección de los conjuntos A - B
- Ver la diferencia simétrica y
- Eliminar un elemento del conjunto ‘A’
- Eliminar un elemento del conjunto ‘B’ se debe validar (en 6 y 7)
para la eliminación previamente que el conjunto no esté vacío para
proceder con la eliminación caso contrario se avisará por pantalla
"""


pares = set()
impares = set()

def validar(numero):
    if numero %2 == 0:
        pares.add(numero)
    else:
        impares.add(numero)
    print(f"pares: {pares} impares: {impares}")

def Ver(numero):
    int(numero)
    if numero in pares:
        print("El numero esta dentro del conjunto par.")
    elif numero in impares:
            print("El numero esta dentro del conjunto impar.")
    else:
        print("El numero no esta en ningun conjunto")

def union(pares,impares):
    print( pares | impares )

def interseccion(pares,impares):
    print(pares & impares)

def eliminar(pares,impares,numero):
    if numero in pares:
        if len(pares) > 0:
            pares.discard(numero)
            print(f"pares: {pares} impares: {impares}")
        else:
            print("el conjunto esta vacio")
            print(f"pares: {pares} impares: {impares}")
    elif numero in impares:
        if len(impares) > 0:
            impares.discard(numero)
            print(f"pares: {pares} impares: {impares}")
        else:
            print("el conjunto esta vacio")
            print(f"pares: {pares} impares: {impares}")

aux = True

while aux:
    print()
    print("---------------------------")
    print("CONJUNTO DE PARES E IMPARES")
    print("---------------------------")
    print("""Opcciones:
        [0]: Cerrar
        [1]: Agregar un numero
        [2]: Ver la Union de los conjuntos A y B
        [3]: Ver la intersección de los conjuntos A y B
        [4]: Eliminar un Valor
        [5]: Ver donde esta el numero
        """)
    Opccion = input("Eleccion: ")

    if Opccion == "0": aux = False
    elif Opccion == "1":validar(int(input("Que numero quiere meter?: ")))
    elif Opccion == "2":union(pares,impares)
    elif Opccion == "3":interseccion(pares,impares)
    elif Opccion == "4":eliminar(pares,impares,int(input("Que numero desea eliminar?: ")))
    elif Opccion == "5":Ver(int(input("Que numero quiere ver?: ")))