import manzanas
def main():
    cosecha = manzanas.generar_cosecha(int(input("Ingrese la cantidad de manzanas que quiere cosechar: ")))
    totales = manzanas.calcular_cosecha(cosecha)
    cantidad,peso = totales
    print(totales)
    print(f"Generando {cantidad} registros de cosecha...")
    print(f"Peso total cosechado: {peso:.2f} kg")
main()

