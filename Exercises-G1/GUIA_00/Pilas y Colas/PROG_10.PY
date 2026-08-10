"""
Leer una palabra y verificar si es un palíndromo (se lee igual
al derecho que al revés) usando una pila."""
def esPalindromo(palabra):
    if palabra == palabra[::-1]:
        print("Es un palindromo")
    else:
        print("No es un palindromo")


palabra = input("Ingrese la palabra para verificar si es un palindromo: ")
esPalindromo(palabra)