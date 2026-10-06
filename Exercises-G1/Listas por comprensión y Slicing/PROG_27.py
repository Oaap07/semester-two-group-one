"""
PROG_27: Una perfumería necesita un sistema básico para gestionar sus
productos sin usar estructuras complejas. Para ello, se utilizarán tres
diccionarios paralelos sincronizados mediante el código de producto
(string de 6 caracteres):

- nombres: relaciona el código con la descripción del producto.
- precios: relaciona el código con el precio unitario (float).
- stock: relaciona el código con la cantidad disponible (int).

Escribir un programa con un menú interactivo que permita:

1.Consultar catálogo: Mostrar código, nombre, precio y stock de todos
los productos.

2.Agregar producto: Pedir datos e insertarlos en los tres diccionarios
(validar que el código no exista previa ni posteriormente).

3.Eliminar producto: Eliminar la clave indicada de los tres
diccionarios.

4.Modificar precio: Actualizar el valor en el diccionario de precios.

5. Registrar Compra / Venta (Modificar Stock): Sumar stock si es compra
o restar si es venta (validando que no quede stock negativo).

6. Salir.
"""
nombres = {
"SHAM01": "Shampoo Neutro 500ml",
"ENJU01": "Acondicionador Brillo",
"JABO01": "Jabón de Glicerina",
"DESO01": "Desodorante Roll-On"
}
precios = {
"SHAM01": 4500.50,
"ENJU01": 4800.00,
"JABO01": 1200.00,
"DESO01": 3100.25
}
stock = {
"SHAM01": 15,
"ENJU01": 10,
"JABO01": 40,
"DESO01": 25
}
def mostrar_menu():
    print("\n--- SISTEMA DE GESTIÓN DE PERFUMERÍA ---")
    print("1. Consultar catálogo y stock")
    print("2. Agregar nuevo producto")
    print("3. Eliminar producto")
    print("4. Modificar precio")
    print("5. Actualizar stock (Compra/Venta)")
    print("6. Salir")
def catalogo_stock():
    for i in nombres:
        print("----")
        print(f"Codigo: {i} ")
        print(f"Nombre: {nombres[i]}")
        print(f"Precio: {precios[i]}")
        print(f"Stock: {stock[i]}")

def agregar_producto():
    nuevo_codigo = input("ingrese el codigo del producto nuevo: ")
    if nuevo_codigo not in nombres:
        nuevo_nombre = input("ingrese el nombre del producto nuevo: ")
        nuevo_precio = int(input("ingrese el precio del prodcuto nuevo: "))
        nuevo_stock = int(input("ingrese cuanto stock hay del producto nuevo: "))
        nombres[nuevo_codigo] = nuevo_nombre
        precios[nuevo_codigo] = nuevo_precio
        stock[nuevo_codigo] = nuevo_stock
        print("Producto agregado exitosamente...")
    else:
        print("Producto ya existente...") 

def eliminar_producto():
    eliminar = input("Que producto desea eliminar? (ingrese el codigo del producto): ")
    if eliminar in nombres:
        del nombres[eliminar]
        del precios[eliminar]
        del stock[eliminar]
        print("Producto eliminado exitosamente...")
    else: 
        print("No se ha encontrado el prodcuto ingresado.")

def modificar_precio():
    codigo = input("Ingrese el codigo del producto que desea modificar el precio: ")
    if codigo in nombres:
        nuevo_precio = int(input("Ingrese el nuevo precio del prodcuto: "))
        precios[codigo] = nuevo_precio
        for i in nombres:
                print("----")
                print(f"Codigo: {i} ")
                print(f"Nombre: {nombres[i]}")
                print(f"Precio: {precios[i]}")
                print(f"Stock: {stock[i]}")
    else:
        print("No se ha podido encontrar el producto. ")

def comprar_vender():
    compra_venta = int(input("Quiere registrar una compra(1) o una venta(2): "))
    while compra_venta != 1 and compra_venta != 2:
        print("Opcion invalida. Intentelo de nuevo")
        compra_venta = int(input("Quiere registrar una compra(1) o una venta(2): "))
    else:
        if compra_venta == 1:
            producto_compra = input("Ingrese el codigo de el producto que quiere comprar: ")
            if producto_compra in nombres:
                print(f"Stock disponible para {nombres[producto_compra]} : {stock[producto_compra]}")
                stock[producto_compra] += int(input("Cuanto stock quiere comprar? "))
                print('Producto comprado..')
                print(f" Stock disponible para {nombres[producto_compra]} : {stock[producto_compra]}")
            else:
                print("No se ha podido encontrar el producto.")
        else:
            producto_compra = input("Ingrese el codigo de el producto que quiere vender: ")
            if producto_compra in nombres:
                print(f"Stock disponible para {nombres[producto_compra]} : {stock[producto_compra]}")
                restar = int(input("Cuanto stock quiere vender? "))
                if restar <= stock[producto_compra]:
                    stock[producto_compra] -= restar
                    print('Producto vendido..')
                    print(f"Stock disponible para {nombres[producto_compra]} : {stock[producto_compra]}")
                else:
                    print("No hay suficiente stock.")
            else:
                print("No se ha podido encontrar el producto.")
opcion = ""
while opcion != "6":
    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        catalogo_stock()
    elif opcion == "2":
        agregar_producto()
    elif opcion == "3":
        eliminar_producto()
    elif opcion == "4":
        modificar_precio()
    elif opcion == "5":
        comprar_vender()
    elif opcion == "6":
        print("Saliendo del sistema...")
else:
    print("Opción inválida. Intente nuevamente.")