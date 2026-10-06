precios = {
"Auriculares": 12000.0,
"Teclado": 25000.0,
"Mouse": 8500.0,
"Monitor": 140000.0,
"Webcam": 18000.0
}
ventas = {
"Auriculares": 15,
"Teclado": 8,
"Mouse": 22,
"Monitor": 3,
"Webcam": 10
}

ganancias = {}
for p in precios:
    final = ventas.get(p) * precios.get(p)
    ganancias[p] = final

total = 0
for g in ganancias:
    print(f"el producto: {g} vendio: {ganancias[g]}")
    print(50*"=")
    total += ganancias[g]
print(f"el total de las ventas es: {total}")

for v   in ventas:
    mayor_producto = max(ventas.values())
    if ventas[v] == mayor_producto:
        mayor_producto_nombre = v

print(50*"=")
print(f"el producro que mas se vendio es: {mayor_producto_nombre}: {mayor_producto}")
for g in ganancias:
    mayor_precio = max(ganancias.values())
    if ganancias[g] == mayor_precio:
        mayor_precio_nombre = g
print(50*"=")
print(f"el producro que mas genero es: {mayor_precio_nombre}: {mayor_precio}")
