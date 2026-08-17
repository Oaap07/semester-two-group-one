"""
PROG_18: El sistema central de la autopista te ha encargado desarrollar
    el módulo de control para una estación con 3 cabinas de peaje.
    Tu objetivo es procesar la atención de los vehículos fila por fila, 
    cobrando las tarifas correspondientes y administrando el flujo de autos que van llegando a la estación. Reglas de la Simulación.
    
        - Estructura del Peaje: El peaje cuenta con 3 colas (cola_1, cola_2, cola_3).
        
            Las 3 colas están agrupadas dentro de una lista principal llamada peaje.

        - Cobro y Tarifas: Cada vez que se atiende (desencolado) a un vehículo de la cabina elegida, se cobra una tarifa según el tipo:
            Moto: $1500, Auto: $2000, Camión: $5000

        - Flujo de Arribo (El Turno): Cada vez que se atiende a un vehículo con éxito, 
        hay un 60% de probabilidad de que ingrese un nuevo vehículo a la estación. Este nuevo vehículo (Moto, Auto o Camión)
        se asignará automáticamente a una de las 3 colas de forma aleatoria.
        
        - Validación: No se puede atender una cola que esté vacía. Si el usuario elige una cola vacía,
        el programa debe mostrar un mensaje de advertencia y solicitar de nuevo la opción sin perder el turno.
    
    - Se debe mostrar la recaudación total.
"""

import random

# Tarifas fijas
TARIFA_MOTO = 1500
TARIFA_AUTO = 2000
TARIFA_CAMION = 5000

# Colas iniciales con algunos vehículos cargados previamente
cola_1 = ["Auto", "Moto", "Camión"]
cola_2 = ["Camión", "Auto"]
cola_3 = ["Moto", "Auto", "Auto"]

peaje = [cola_1, cola_2, cola_3]

recaudacion_total = 0
vehiculos_atendidos = 0

def generar_ingreso_aleatorio():
    
    if random.random() < 0.6:
        tipos = ["Moto", "Auto", "Camión"]
        nuevo_vehiculo = random.choice(tipos)
        indice_cola = random.randint(0, 2)
        peaje[indice_cola].append(nuevo_vehiculo)
    
        print(f"\nIngresó un/a {nuevo_vehiculo} a la Cola {indice_cola + 1}.")

def mostrar_estado_peaje():
    
    print("\n" + "=" * 40)
    print("ESTADO ACTUAL DE CABINAS DE PEAJE")
    print("=" * 40)
    for i, cola in enumerate(peaje, start=1):
        print(f"Cabina {i} (Frente -> Fin): {cola}")
    print(f"\nRecaudación acumulada: ${recaudacion_total}")
    print("=" * 40)
    


# BUCLE PRINCIPAL DEL PROGRAMA
mientras_jugando = True

while mientras_jugando:
    mostrar_estado_peaje()
    
    print("\nMenú de Opciones:")
    print("1. Atender Cabina 1")
    print("2. Atender Cabina 2")
    print("3. Atender Cabina 3")
    print("4. Salir del programa")
    
    opcion = input("Elegí una opción (1-4): ")
    
    if opcion in ["1", "2", "3"]:
        indice = int(opcion) - 1  # Convertimos la opción (1, 2, 3) a índice (0, 1, 2)
        print(len(peaje[indice]))
        if len(peaje[indice]) == 0:
            print("La cabina está vacía, no se puede atender")
            pass
        elif len(peaje[indice]) > 0:
            
            vehiculo = peaje[indice][0]
            print(vehiculo)
            if vehiculo == "Moto":
                print("\n" + "=" * 40)
                print(f"Atendiendo Vehiculo de la cabina {(indice + 1)} ")
                print(f"Vehiculo:{vehiculo} | Monto que abono: ${TARIFA_MOTO}")
                print("=" * 40)
                recaudacion_total += TARIFA_MOTO
                generar_ingreso_aleatorio()
                vehiculos_atendidos += 1
                peaje[indice].pop(0)
            elif vehiculo == "Auto":
                print("\n" + "=" * 40)
                print(f"Atendiendo Vehiculo de la cabina {(indice + 1)} ")
                print(f"Vehiculo:{vehiculo} | Monto que abono: ${TARIFA_AUTO}")
                print("=" * 40)
                recaudacion_total += TARIFA_AUTO
                generar_ingreso_aleatorio()
                vehiculos_atendidos += 1
                peaje[indice].pop(0)
            elif vehiculo == "Camión":
                print("\n" + "=" * 40)
                print(f"Atendiendo Vehiculo de la cabina {(indice + 1)} ")
                print(f"Vehiculo:{vehiculo} | Monto que abono: ${TARIFA_CAMION}")
                print("=" * 40)
                recaudacion_total += TARIFA_CAMION
                generar_ingreso_aleatorio()
                vehiculos_atendidos += 1
                peaje[indice].pop(0)

    elif opcion == "4":
        mientras_jugando = False
        print("\nCerrando estación de peaje...")
    else:
        print("\nOpción inválida. Intente nuevamente.")

# Resumen final
print("\n" + "*" * 40)
print("RESUMEN DE LA JORNADA")
print(f"Total vehículos atendidos: {vehiculos_atendidos}")
print(f"Recaudación total: ${recaudacion_total}")
print("*" * 40)