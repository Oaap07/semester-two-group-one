
import sys
# 1.	Calcular el factorial de un número n.
sys.set_int_max_str_digits(0)


def factorial(n):

    if n == 1:
        return n
    else:
        n *= factorial(n-1)
    return n

def suma(n):
    if n == 1:
        return n
    else:
        return (n + suma(n-1))
    

# 3.	Mostrar los números del 1 al n.

def mostrar_asc(n):
    if n == 0:
        return
    else:
        mostrar_asc(n-1)
        print(n)

# 4.	Mostrar los números del n al 1.

def mostrar_des(n):
    if n == 0:
        return
    else:
        print(n)
        mostrar_des(n-1)

def potencia(n,m):
    if m == 0:
        return 1
    else:
        return n * potencia(n, m-1)
    

while True:
    res = int(input("\nIngrese una opción: \n \
    1. Factorial\n \
    2. Suma\n \
    3. Ascendente\n \
    4. Descendente\n \
    5. Potencia (base y exponente)\n \
    [0] Exit \
    \n\n \
    --- "))
    print("")

    if res==0: print("-- Saliendo --\n"); break
    elif res==1: print(factorial(int(input("Ingrese un número: ")))); input(),
    elif res==2: print(suma(int(input("Ingrese un número: ")))); input(),
    elif res==3:mostrar_asc(int(input("Ingrese un número: "))); input(),
    elif res==4:mostrar_des(int(input("Ingrese un número: "))); input(),
    elif res==5: print(potencia(int(input("Ingrese un número: ")),int(input("ingrese el exponente: ")))); input()