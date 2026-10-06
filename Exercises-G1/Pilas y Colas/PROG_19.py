"""
PROG_19: Un minimarket necesita un sistema para administrar la heladera
de lacteos. Para evitar pérdidas por vencimiento, los productos que
ingresan deben gestionarse con lógica de cola. El cajero/repositor puede
vender el producto al frente, comprar stock nuevo o rotar los productos
de la góndola para exponer los que vencen antes. Reglas:
- Listas Sincronizadas: Manejaremos 3 listas donde el mismo índice
representa al mismo producto:
o nombres: Nombre del producto (ej: "Leche", "Yogur").
o dias_vencimiento: Días restantes antes de que venza (un
número entero).
o precios: Precio de venta del producto.
- Acciones del Menú:

1. Vender producto: Se atiende al cliente vendiendo el producto
que está al frente de la cola (índice 0). Se desencola de
las 3 listas, se cobra el precio y transcurre 1 día en el
local (se resta 1 día a la fecha de vencimiento de todos
los demás productos en stock).

2. Comprar / Reponer stock: El usuario ingresa el nombre y
precio de un nuevo producto. El sistema le asigna
automáticamente días de vencimiento aleatorios (entre 15 y
30 días) y lo encola al final.

3. Rotar góndola (Reordenar): Quita el producto del frente
(índice 0) y lo vuelve a encolar al final de las 3 listas.
Esto permite mover un producto que todavía tiene muchos días
por delante para dar paso a otros más urgentes.

4. Salir: Muestra el resumen de ventas.
- Cada vez que transcurre un día (al vender), si el producto del
frente tiene dias_vencimiento <= 0, el sistema no permite
venderlo: debe descartarse automáticamente (desencolarse sin
sumar dinero) avisando al usuario.
"""

import random

# Listas sincronizadas con stock inicial (frente de la cola = índice 0)
nombres = ["Leche", "Yogur", "Queso"]
dias_vencimiento = [2, 18, 25]  # La leche está a punto de vencer
precios = [1200, 1500, 3500]

recaudacion_total = 0
productos_vendidos = 0


def mostrar_estado_stock():
    print("\n" + "=" * 55)
    print("ESTADO ACTUAL DE LA GÓNDOLA (FRENTE -> FINAL)")
    print("=" * 55)
    
    if not nombres:
        print(" ⚠️ La góndola está completamente vacía.")
    else:
        for i in range(len(nombres)):
            marca = " 🛒 [SIGUIENTE A VENDER]" if i == 0 else ""
            print(f"{i+1}. {nombres[i]} | Precio: ${precios[i]} | Vence en: {dias_vencimiento[i]} días{marca}")
    
    print("-" * 55)
    print(f"Recaudación acumulada: ${recaudacion_total}")
    print("=" * 55)


def pasar_dia():
    """Resta 1 día de vencimiento a todos los productos del stock."""
    for i in range(len(dias_vencimiento)):
        dias_vencimiento[i] -= 1
    print("\n ⏰ Transcurrió 1 día en el minimarket. Se actualizaron los vencimientos.")


# BUCLE PRINCIPAL DEL PROGRAMA
ejecutando = True

while ejecutando:
    mostrar_estado_stock()
    
    print("\nMenú de Opciones:")
    print("1. Vender producto del frente")
    print("2. Comprar / Ingresar nuevo producto")
    print("3. Rotar góndola (Mover el primero al final)")
    print("4. Salir")
    
    opcion = input("Elegí una opción (1-4): ")
    
    if opcion == "1":
        if nombres:
            if dias_vencimiento[0] <= 0:
                print(f"El producto {nombres[0]} ya fue descartado")
                nombres.pop(0)
                dias_vencimiento.pop(0)
                precios.pop(0)
            else:
                recaudacion_total += precios[0]
                productos_vendidos += 1
                print(f"Se vendio el/la {nombres[0]} ")
                pasar_dia()
                nombres.pop(0)
                dias_vencimiento.pop(0)
                precios.pop(0)
        else:
            print("ERROR")

            

    elif opcion == "2":
        producto_nuevo = input("Ingrese el nombre del producto deseado: ")
        precio_producto_nuevo = int(input("Ingrese el precio del producto: "))
        dia_vencimiento_nuevo = random.randint(15,30)
        precios.append(precio_producto_nuevo)
        nombres.append(producto_nuevo)
        dias_vencimiento.append(dia_vencimiento_nuevo)
        print(f"El producto {producto_nuevo} fue agregado.")

    elif opcion == "3":
        if nombres:
            pick_producto = nombres[0]
            nombres.pop(0)
            nombres.append(pick_producto)
            pick_producto = precios[0]
            precios.pop(0) 
            precios.append(pick_producto)
            pick_producto = dias_vencimiento[0]
            dias_vencimiento.pop(0)
            dias_vencimiento.append(pick_producto)


    elif opcion == "4":
        ejecutando = False
        print("\nCerrando sistema del minimarket...")

    else:
        print("\nOpción inválida. Intente nuevamente.")

# RESUMEN FINAL
print("\n" + "*" * 45)
print("RESUMEN DE LA JORNADA")
print(f"Productos vendidos: {productos_vendidos}")
print(f"Recaudación total: ${recaudacion_total}")
print("*" * 45)