"""esta en la compu de la facu pero incompleto xd"""

imagen_original = [
    [0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 0, 7, 8, 5, 0, 0],
    [0, 0, 7, 9, 5, 8, 0, 0],
    [0, 0, 8, 5, 9, 7, 0, 0],
    [0, 0, 5, 8, 7, 0, 0, 0],
    [0, 5, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0]
]

imagen_reducida = [fila[::2] for fila in imagen_original[::2]]

imagen_binaria = [[1 if fila >= 5 else 0 for fila in fila] for fila in imagen_reducida]

print("--- RESULTADO VISUAL EN CONSOLA ---")
for fila in imagen_binaria:
# Convertimos 1 a cuadro blanco y 0 a cuadro negro
    linea_visual = "".join(["█" if pixel == 1 else "░"
for pixel in fila])
    print(linea_visual)
