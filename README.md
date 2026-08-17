# semester-two-group-one

# EJERCICIOS PENDIENTES

## UNIDAD 0: REPASO - MATRICES

### PROG_02 - MODULO DE MATRICES (PARCIAL)

Deberas implementar un modulo en Python que contenga 9 funciones. Cada funcion debe recibir como parametro un numero entero N (que representa el tamano de una matriz cuadrada de N x N) y retornar una lista de listas que represente la matriz resultante. Ya estan realizados los niveles 1 al 6. Faltan:

**NIVEL 3: ALGORITMOS DE RECORRIDO AVANZADO**

**7. MATRIZ CARACOL (matriz_caracol)**
Escribe la funcion matriz_caracol(n) que devuelva la matriz llena con los numeros del 1 al N al cuadrado siguiendo un recorrido en espiral (sentido horario), comenzando en [0][0] y avanzando hacia el centro.

Ejemplo para N = 3:

```
1 2 3
8 9 4
7 6 5
```

**8. CAPAS CONCENTRICAS (matriz_capas_concentricas)**
Escribe la funcion matriz_capas_concentricas(n) que llene la matriz por "anillos". El borde mas exterior se llena con 1, el siguiente anillo interior con 2, el siguiente con 3, y asi sucesivamente.

Ejemplo para N = 3:

```
1 1 1
1 2 1
1 1 1
```

Ejemplo para N = 5:

```
1 1 1 1 1
1 2 2 2 1
1 2 3 2 1
1 2 2 2 1
1 1 1 1 1
```

**9. LA ESPIRAL CUADRADA (matriz_laberinto)**
Escribe la funcion matriz_laberinto(n) que dibuje un trazo continuo con 1s simulando una espiral que da vueltas hacia el centro sin colisionar ni pegarse a si misma, dejando canales de 0s.

Ejemplo para N = 3:

```
1 1 1
0 0 1
1 1 1
```

Ejemplo para N = 5:

```
1 1 1 1 1
0 0 0 0 1
1 1 1 0 1
1 0 1 0 1
1 1 1 0 1
```

## UNIDAD 1: PILAS & COLAS

### PROG_19 - HELADERA DE LACTEOS

Un minimarket necesita un sistema para administrar la heladera de lacteos. Para evitar perdidas por vencimiento, los productos que ingresan deben gestionarse con logica de cola. El cajero/repositor puede vender el producto al frente, comprar stock nuevo o rotar los productos de la gondola para exponer los que vencen antes.

**LISTAS SINCRONIZADAS:** se manejaran 3 listas donde el mismo indice representa al mismo producto:
- nombres: Nombre del producto (ej: "Leche", "Yogur").
- dias_vencimiento: Dias restantes antes de que venza (un numero entero).
- precios: Precio de venta del producto.

**ACCIONES DEL MENU:**
- Vender producto: Se atiende al cliente vendiendo el producto que esta al frente de la cola (indice 0). Se desencola de las 3 listas, se cobra el precio y transcurre 1 dia en el local (se resta 1 dia a la fecha de vencimiento de todos los demas productos en stock).
- Comprar / Reponer stock: El usuario ingresa el nombre y precio de un nuevo producto. El sistema le asigna automaticamente dias de vencimiento aleatorios (entre 15 y 30 dias) y lo encola al final.
- Rotar gondola (Reordenar): Quita el producto del frente (indice 0) y lo vuelve a encolar al final de las 3 listas. Esto permite mover un producto que todavia tiene muchos dias por delante para dar paso a otros mas urgentes.
- Salir: Muestra el resumen de ventas.

**REGLA ADICIONAL:** cada vez que transcurre un dia (al vender), si el producto del frente tiene dias_vencimiento <= 0, el sistema no permite venderlo: debe descartarse automaticamente (desencolarse sin sumar dinero) avisando al usuario.
