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
    print("\n Plantas que requieren riego urgente:")
    for p in a_regar:
        print(f" - {p['nombre']}: Lleva {p['dias_sin_regar']} dias sin agua (Max: {p['frecuencia_riego_dias']})")

    # 2. Actualizar precios
    AUMENTO = 15.0 # 15%
    print(f"\nAplicando aumento del {AUMENTO}% por inflacion...")
    f.aplicar_aumento_precios(catalogo, AUMENTO)

    print("\nPrecios actualizados:")
    
    for p in catalogo:
        print(f" - {p['nombre']}: ${p['precio']:.2f}")

if __name__ == "__main__":
    main()