import manzanas

cosecha = manzanas.generar_cosecha(int(input("Ingrese la cantidad de manzanas que quiere cosechar: ")))
totales = manzanas.calcular_cosecha(cosecha)
cantidad,peso = totales

print(f"Cantidad de registros: {cantidad}")
print(f"Peso total: {peso}")