"""
PROG_33: Un vivero necesita un sistema para administrar el catálogo de
sus plantas aromáticas y ornamentales, permitiendo actualizar precios
por inflación y detectar qué especies requieren riego inmediato.
"""

import Funciones as f

def main() -> None:
    print("=== SISTEMA DE GESTION DE VIVERO ===")
    catalogo = f.obtener_catalogo_inicial()

    # 1. Revisar plantas con necesidad de riego
    a_regar = f.obtener_plantas_para_regar(catalogo)

    # Plantas ordenadas de mayor a menor
    ordenados = sorted(a_regar, key=lambda p: p['dias_sin_regar'] - p['frecuencia_riego_dias'], reverse=True)
    print("\n Plantas que requieren riego urgente ordenadas:")
    for p in ordenados:
        print(f" - {p['nombre']}: Lleva {p['dias_sin_regar']} dias sin agua (Max: {p['frecuencia_riego_dias']})")

    # 2. Actualizar precios
    AUMENTO = 15.0 # 15%
    print(f"\nAplicando aumento del {AUMENTO}% por inflacion...")
    f.aplicar_aumento_precios(catalogo, AUMENTO)

    print("\n--- Precios actualizados:")
    for p in catalogo:
        print(f" - {p['nombre']}: ${p['precio']:.2f}")

    # Precios con descuentos arriba de los $2000.0
    print("\n--- Precios arriba de los $2000.0 con descuentos:")
    descuento = list(map(lambda p: round(p['precio'] * 0.8, 2) if p["precio"] > 2000 else p["precio"], catalogo))
    print(descuento)

    # Filtro de plantas empezadas con 'M' o 'L' y con precio menor a $2000.0
    plantas_seleccionadas = list(filter(lambda p: (p["nombre"].startswith("M") or p["nombre"].startswith("L")) and p["precio"] < 2000, catalogo))
    print("\n--- Plantas empezadas con 'M' o 'L' y con precio menor a $2000.0")
    [print(f"{i['nombre']} : ${i['precio']}") for i in plantas_seleccionadas]

if __name__ == "__main__":
    main()