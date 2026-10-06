"""
PROG_28: Vamos a simular un juego de lotería utilizando diccionarios,
conjuntos y el módulo random.
1. Se parte de un diccionario de apuestas donde las claves son los
nombres de los jugadores y los valores son conjuntos (set) con los 6
números que cada uno jugó (números del 1 al 40).
2. Simular el sorteo generando un conjunto de 6 números aleatorios
únicos entre 1 y 40 (random.randint o random.sample).
3. Mediante operaciones de conjuntos (intersección), determinar la
cantidad de aciertos de cada jugador.
4. Imprimir los resultados e indicar el o los ganadores (quien o quienes
hayan obtenido la mayor cantidad de aciertos).
"""
import random as rd

# Jugadores y sus números apostados (cada jugador eligió 6 números)
jugadores = {
"Carlos": {4, 8, 15, 16, 23, 42},
"Ana": {1, 5, 12, 20, 25, 30},
"Beatriz": {4, 12, 18, 23, 33, 40},
"Diego": {7, 14, 21, 28, 35, 39}
}
# 1. Se Generan 6 números ganadores del sorteo (sin repetición)
numeros_sorteados = set()
[numeros_sorteados.add(i) for i in rd.sample(range(1, 41), k=6)] #  Se añade a numeros_sorteados 6 números de valores aleatorios dentro de un rango de entre 1 y 40 inclusive.
print(f"\nNúmeros sorteados hoy: {numeros_sorteados}\n")

# 2. Se recorre nombres, calculo aciertos con len() e intersección e imprimo aciertos.
aciertos = {}
for i in jugadores:
    aciertos[i] = len(jugadores[i] & numeros_sorteados)
    print(f"-- {i} tuvo: [{aciertos[i]}]")

# 3. Se determina el ganador o empates.
ganadores = [i for i in aciertos if aciertos[i] == max(aciertos.values())] #  Crea una lista con los nombres con mayores aciertos

if sum(aciertos.values()) == 0:
    print("\n----Nadie Ganó----\n")
elif len(ganadores) == 1:
    print(f"\nGanó: {ganadores[0]}\n")
elif len(ganadores) > 1:
    print(f"\nGanaron: " + ", ".join(ganadores[:-1]) + " y " + ganadores[-1] + "\n") #  Separación de valores con join() para crear una oración correctamente
