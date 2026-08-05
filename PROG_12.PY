"""
Un bibliotecario necesita apilar una serie de libros que van
llegando a su escritorio. Por cuestiones de estabilidad física, nunca
se puede colocar un libro de mayor tamaño encima de uno más pequeño.
Escribe un algoritmo que reciba una pila de libros desordenados y,
utilizando únicamente una pila auxiliar, devuelva la pila original
ordenada de tal manera que el libro más grande quede en la base y el
más pequeño en el tope (los libros se pueden representar con un número
que indica su tamaño). Funciones a desarrollar:
- ordenar_pila_libros(pila_origen):
o Entrada: Un lista con los tamaños de los libros (enteros).
o Retorno: Una nueva Pila ordenada donde los tamaños van de
mayor (base) a menor (tope).
o Restricción: Solo se permite utilizar métodos de las pilas
(apilar, desapilar, ver tope)
"""

def ordenar_pila_libros(pila_origen):
    

    return pila_final
    




pila_desordenada = [5, 1, 3, 2, 4]
pila_ordenada = ordenar_pila_libros(pila_desordenada)
print(f"Pila desordenada: {pila_desordenada}")
print(f"Pila ordenada: {pila_ordenada}")