"""
PROG_23: Un crear un programa que utilizando que, utilizando dos
conjuntos, uno para números impares y otro para números pares, permita
al usuario:
- Ingresar un número a uno de estos conjuntos (se deberá validar
mediante función si el número ingresado debe ir al conjunto par o
al conjunto impar; dado que solo se permiten números enteros
naturales utilizar la función de validar número del template)
- Crear una función que pueda ser llamada por la opción dos del menú
y que verifique si un número se encuentra en el conjunto par. El
número será ingresado por el usuario utilizando como validación
la función de validar número

- Ingresando un valor numérico al igual que en el caso anterior, se
informará al usuario si el número se encuentra en el conjunto
impar.

Keyword arguments:
argument -- description
Return: return_description
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
aux = True

while aux:
    print()
    print("---------------------------")
    print("CONJUNTO DE PARES E IMPARES")
    print("---------------------------")
    print("""Opcciones:
        [0]:Cerrar
        [1]: Agregar un numero
        [2]: Ver donde esta el numero
        """)
    Opccion = input("Eleccion: ")

    if Opccion == "0": aux = False
    elif Opccion == "1":validar(int(input("Que numero quiere meter?: ")))
    elif Opccion == "2": Ver(int(input("Que numero quiere ver?: ")))



