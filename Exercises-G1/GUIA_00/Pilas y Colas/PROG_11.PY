"""Escribir una función que utilizando que reciba una pila de
enteros y retorne dos pilas una con los números pares y otra con los
impares."""
import random

def separar_pares_impares(numeros):
    pila_pares = []
    pila_impares = []
    while len(numeros) > 0:
        numero = numeros.pop()
        if numero % 2 == 0:
            pila_pares.append(numero)
        else:
            pila_impares.append(numero)
    return pila_pares, pila_impares

numeros = [random.randint(1, 10) for i in range(10)]
print(f"Pila original: {numeros}")
pila_pares, pila_impares = separar_pares_impares(numeros)
print(f"Pila de números pares: {pila_pares}")
print(f"Pila de números impares: {pila_impares}")