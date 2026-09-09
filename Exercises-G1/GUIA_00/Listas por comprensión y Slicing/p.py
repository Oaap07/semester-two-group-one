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
            print(f"Stock disponible para {nombres[producto_compra]} : {stock[producto_compra]}")
        else:
            print("No se ha podido encontrar el producto.")
    else:
        producto_compra = input("Ingrese el codigo de el producto que quiere vender: ")
        if producto_compra in nombres:
            print(f"Stock disponible para {nombres[producto_compra]} : {stock[producto_compra]}")
            restar = int(input("Cuanto stock quiere vender? "))
            if restar <= stock[producto_compra]:
                stock[producto_compra] -= restar
                print(f"Stock disponible para {nombres[producto_compra]} : {stock[producto_compra]}")
            else:
                print("No hay suficiente stock.")
        else:
            print("No se ha podido encontrar el producto.")




