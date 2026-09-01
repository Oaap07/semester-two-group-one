# Guía de Trabajos Prácticos - Programación I

**Facultad de Ingeniería Informática**

---

## Unidad 2: Algoritmos y Transformación de Datos

### PROG_21

Un satélite en órbita necesita enviar fotos a la Tierra, pero la velocidad de conexión es extremadamente lenta. Para solucionar esto, el equipo de ingeniería diseñó un algoritmo de dos pasos para reducir el peso de las imágenes antes de enviarlas:

1. **Submuestreo:** Reduce el tamaño de la imagen a la mitad recortando píxeles.
2. **Binarización:** Simplifica los colores a solo dos tonos (Blanco y Negro) usando un umbral de brillo. Las imágenes se representan como matrices de enteros entre 0 (Negro) y 9 (Blanco).

**Consignas:**

1. **La Imagen Original:** Crear una matriz de $8 \times 8$ que represente una foto en escala de grises. (Podemos usar IA para trabajar con una imagen prefijada con una forma reconocible, como una carita o un corazón, o generarla con `random.randint(0, 9)`).
2. **Paso 1 - Reducción de Tamaño (Slicing):** Crear una nueva matriz `imagen_reducida` de $4 \times 4$ tomando solo 1 de cada 2 píxeles (las filas y columnas pares).
* **Requisito:** Utilizar slicing con paso 2 (`::2`) dentro de una lista por comprensión:
```python
imagen_reducida = [fila[::2] for fila in imagen_original[::2]]

```




3. **Paso 2 - Simplificación de Color (Listas por Comprensión con condición):** Generar una matriz `imagen_binaria` a partir de la reducida. Si el valor del píxel es mayor o igual a 5, se convierte en 1 (Luz), de lo contrario en 0 (Sombra).
* **Requisito:** Utilizar una lista por comprensión con expresión `if-else`.


4. **Visualización en Pantalla (Bonus Visual):** Muestra la imagen original y la comprimida en la consola reemplazando los números 0 y 1 por caracteres visuales (por ejemplo `"  "` para 0 y `"██"` para 1).

**Código de ayuda:**

```python
# ==========================================
# 4. Renderizado Visual (ASCII / Emojis)
# ==========================================
print("--- RESULTADO VISUAL EN CONSOLA ---")
for fila in imagen_binaria:
    # Convertimos 1 a cuadro blanco y 0 a cuadro negro
    linea_visual = "".join([" " if pixel == 1 else " " for pixel in fila])
    print(linea_visual)

```

---

### PROG_22

El departamento de ciberseguridad necesita enviar mensajes encriptados a los agentes en campo. Tu tarea será construir el algoritmo de encriptado utilizando herramientas nativas de Python y luego utilizar Inteligencia Artificial (ChatGPT, Gemini, etc.) como asistente para desarrollar el desencriptador, documentando todo el proceso.

#### Parte 1: El Encriptador (Programación en Python)

Escriban un script en Python que tome el siguiente mensaje base:

* **Mensaje:** `"Hola James Bond, deberás ir a Cabildo y Juramento. Fin del Mensaje"`
* **Resultado:** `"101j97sn101m l101d n105f .111tn101m97r117j y 111dl105b97c 97 r105 sár101b101d ,dn111b s101m97j 97l111h"`

**Pasos de transformación:**

1. **Inversión y Normalización:** Invierte el texto completo y conviértelo a minúsculas. Es obligatorio utilizar slicing.
2. **Sustitución por ASCII:** Genera el mensaje cifrado final reemplazando cada vocal (`a, e, i, o, u`) por su correspondiente código ASCII (convertido a texto). Es obligatorio utilizar una Lista por Comprensión y `.join()`.
3. Muestra por pantalla el mensaje encriptado resultante.

#### Parte 2: El Desafío de Desencriptación con IA

Una vez que tengan el mensaje encriptado:

1. Utilizar una herramienta de Inteligencia Artificial para solicitarle que cree una función en Python capaz de desencriptar el texto y recuperar la frase original.
2. Ejecutar el código proporcionado por la IA y verificar si recupera el texto exactamente como era al principio.
3. Documentar el resultado final:
* ¿Cómo resolvió la IA el problema de devolver los códigos ASCII (como `'101'` o `'97'`) a sus vocales originales?
* ¿En qué parte del código de la IA se utilizó slicing para volver a dar vuelta la cadena?



---

## Unidad 3.1: Conjuntos

### PROG_23

Crear un programa que, utilizando dos conjuntos (uno para números impares y otro para números pares), permita al usuario:

* Ingresar un número a uno de estos conjuntos (se deberá validar mediante función si el número ingresado debe ir al conjunto par o al conjunto impar; dado que solo se permiten números enteros naturales utilizar la función de validar número del template).
* Crear una función que pueda ser llamada por la opción dos del menú y que verifique si un número se encuentra en el conjunto par. El número será ingresado por el usuario utilizando como validación la función de validar número.
* Ingresando un valor numérico al igual que en el caso anterior, se informará al usuario si el número se encuentra en el conjunto impar.

---

### PROG_24

Tomando como referencia el programa anterior, construir un programa similar que tenga las siguientes características:

* Ingresar números enteros naturales a un primer conjunto llamado `A`.
* Ingresar números en un conjunto `B`.
* Ver la Unión de los conjuntos ($A \cup B$).
* Ver la Intersección de los conjuntos ($A \cap B$).
* Ver la Diferencia Simétrica.
* Eliminar un elemento del conjunto `A`.
* Eliminar un elemento del conjunto `B`.
* Se debe validar para la eliminación previamente que el conjunto no esté vacío para proceder; caso contrario se avisará por pantalla.

---

### PROG_25

Se nos ha solicitado crear un programa que mediante el uso de un conjunto de tuplas podamos identificar la posición de unas oficinas en un mapa. El usuario podrá ingresar una nueva oficina cuyos valores son ingresados por teclado como coordenada $X$ e $Y$. Se almacenarán como una tupla dentro del conjunto. Se deberá validar que no está dentro del conjunto y de ser así se avisará al usuario que ese local ya fue ingresado.

Luego, mediante una función se avisará al usuario cuántas oficinas se encuentran en la región norte, cuántas en la región este, cuántas en la región oeste y cuántas en la región sur; para ello, tener en cuenta que las coordenadas son números enteros naturales que van del $0$ al $100$. La coordenada $(50, 50)$ es el punto que divide norte de sur y este de oeste.

---

### PROG_26

Utilizando listas, tuplas y conjuntos, crear un programa que genere todas las fichas de un dominó. Cada ficha individual será una tupla contenida dentro de un conjunto que es el total de las fichas. Crear un método que seleccione aleatoriamente dos fichas, las imprima y mediante una validación imprima por pantalla si esas dos fichas "encajan".

*Ejemplo:* La ficha `(1, 2)` encaja con `(3, 2)` pero no con `(3, 3)`.

---

## Unidad 3.2: Diccionarios

### PROG_27

Una perfumería necesita un sistema básico para gestionar sus productos sin usar estructuras complejas. Para ello, se utilizarán tres diccionarios paralelos sincronizados mediante el código de producto (string de 6 caracteres):

* `nombres`: relaciona el código con la descripción del producto.
* `precios`: relaciona el código con el precio unitario (float).
* `stock`: relaciona el código con la cantidad disponible (int).

Escribir un programa con un menú interactivo que permita:

1. **Consultar catálogo:** Mostrar código, nombre, precio y stock de todos los productos.
2. **Agregar producto:** Pedir datos e insertarlos en los tres diccionarios (validar que el código no exista previa ni posteriormente).
3. **Eliminar producto:** Eliminar la clave indicada de los tres diccionarios.
4. **Modificar precio:** Actualizar el valor en el diccionario de precios.
5. **Registrar Compra / Venta (Modificar Stock):** Sumar stock si es compra o restar si es venta (validando que no quede stock negativo).
6. **Salir.**

**Código Base:**

```python
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

opcion = ""
while opcion != "6":
    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        # TODO: Recorrer uno de los diccionarios y mostrar la información combinada
        pass
    elif opcion == "2":
        # TODO: Pedir codigo, nombre, precio y stock.
        # Verificar que el código NO exista antes de agregar.
        pass
    elif opcion == "3":
        # TODO: Pedir código a eliminar y quitarlo de los 3 diccionarios.
        pass
    elif opcion == "4":
        # TODO: Pedir código y nuevo precio. Actualizar el diccionario correspondiente.
        pass
    elif opcion == "5":
        # TODO: Pedir código, tipo de operación (C: compra / V: venta) y cantidad.
        # Ajustar el stock validando que haya unidades suficientes si es venta.
        pass
    elif opcion == "6":
        print("Saliendo del sistema...")
    else:
        print("Opción inválida. Intente nuevamente.")

```

---

### PROG_28

Vamos a simular un juego de lotería utilizando diccionarios, conjuntos y el módulo `random`.

1. Se parte de un diccionario de apuestas donde las claves son los nombres de los jugadores y los valores son conjuntos (`set`) con los 6 números que cada uno jugó (números del 1 al 40).
2. Simular el sorteo generando un conjunto de 6 números aleatorios únicos entre 1 y 40 (`random.randint` o `random.sample`).
3. Mediante operaciones de conjuntos (intersección), determinar la cantidad de aciertos de cada jugador.
4. Imprimir los resultados e indicar el o los ganadores (quien o quienes hayan obtenido la mayor cantidad de aciertos).

*Nota:* Dado que los conjuntos no aceptan repeticiones, tener en cuenta que, al generar el sorteo, puede repetirse un número. Debemos asegurarnos de que el tamaño del conjunto SIEMPRE sea de 6.

**Código Base:**

```python
import random

# Jugadores y sus números apostados (cada jugador eligió 6 números)
jugadores = {
    "Carlos": {4, 8, 15, 16, 23, 42},
    "Ana": {1, 5, 12, 20, 25, 30},
    "Beatriz": {4, 12, 18, 23, 33, 40},
    "Diego": {7, 14, 21, 28, 35, 39}
}

# 1. Generar los 6 números ganadores del sorteo (sin repetidos)
# TODO: Usar random o un conjunto con un bucle while para obtener 6 números entre 1 y 40.
numeros_sorteados = set()
print(f"Números sorteados hoy: {numeros_sorteados}")

# 2. Evaluar aciertos de cada jugador
# TODO: Recorrer el diccionario de jugadores.
# TODO: Calcular los aciertos de cada uno usando la INTERSECCIÓN de conjuntos (& o .intersection()).
# TODO: Guardar o imprimir cuántos aciertos tuvo cada uno.

# 3. Determinar el ganador
# TODO: Indicar quién obtuvo el máximo de aciertos (atención: puede haber empates).

```

---

### PROG_29

Una tienda de electrónica desea analizar sus ventas del mes. Se dispone de dos diccionarios iniciales:

* `precios`: clave = nombre del producto, valor = precio unitario.
* `ventas`: clave = nombre del producto, valor = cantidad de unidades vendidas.

Escribir un programa en Python que:

1. Construya un tercer diccionario llamado `ganancias`, donde cada clave sea el producto y su valor sea el dinero total generado ($\text{precio} \times \text{unidades vendidas}$).
2. Muestre un reporte con el detalle de ganancias por producto.
3. Imprima el total general recaudado por el comercio.
4. Muestre cuál fue el producto más vendido en unidades y cuál fue el producto que aportó más ingresos.

**Código Base:**

```python
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

# TODO 1: Crear el diccionario 'ganancias' recorriendo los diccionarios anteriores
ganancias = {}

# TODO 2: Imprimir el detalle por producto y calcular la recaudación total acumulada

# TODO 3: Determinar el producto con mayor cantidad de unidades vendidas
# y el producto con mayor ganancia en dinero.

```

---

### PROG_30

La Agencia de Administración Gubernamental de Ingresos Públicos (AGIP) nos solicita procesar parcelas representadas en una matriz de $5 \times 5$ píxeles. Cada celda de la imagen representa un tipo de terreno o edificación:

* `'CH'`: Hogares con techo de chapa (ABL mensual: $2.000)
* `'TE'`: Hogares con techo de tejas (ABL mensual: $2.500)
* `'LO'`: Hogares con techo de losa/cemento (ABL mensual: $3.500)
* `'AV'`: Vía pública / Avenidas (No paga impuesto)

A partir del mapa satelital provisto:

1. Recorrer la imagen e ir contabilizando en un diccionario `conteo_hogares` la cantidad de parcelas pertenecientes a cada categoría de construcción.
2. Calcular el subtotal acumulado a cobrar en un diccionario `recaudacion_subtotal` multiplicando el conteo por el impuesto correspondiente.
3. Calcular e imprimir el Total General Recaudado por mes en dicha zona.

*Tip:* predefinir las tarifas en un diccionario base de consulta:
`tarifas = {'CH': 2000, 'TE': 2500, 'LO': 3500}`

**Código Base:**

```python
# Mapa satelital de 5x5 parcelas
mapa_satelital = [
    ['TE', 'TE', 'AV', 'LO', 'LO'],
    ['LO', 'TE', 'AV', 'TE', 'CH'],
    ['AV', 'AV', 'AV', 'AV', 'AV'],
    ['TE', 'LO', 'AV', 'LO', 'TE'],
    ['TE', 'LO', 'AV', 'TE', 'LO']
]

# Diccionario de tarifas ABL por tipo de edificación
tarifas_abl = {
    'CH': 2000,
    'TE': 2500,
    'LO': 3500
}

# Diccionario para contar los tipos de parcelas
conteo_hogares = {
    'CH': 0,
    'TE': 0,
    'LO': 0,
    'AV': 0
}

# TODO 1: Recorrer la matriz mapa_satelital (bucle anidado para filas y celdas)
# e ir incrementando los contadores en conteo_hogares.

# TODO 2: Crear el diccionario recaudacion_subtotal calculando (conteo * tarifa)
# para las categorías imponibles ('CH', 'TE', 'LO').

# TODO 3: Mostrar el reporte final:
# - Cantidad de construcciones por tipo
# - Subtotal a cobrar por cada tipo
# - Suma total general recaudada por la zona

```

---

## Unidad 4: Módulos, Lambda & Typehints

### PROG_31

Una empresa frutícola nos solicita crear un simulador de cosecha de manzanas en memoria. Debemos construir un módulo llamado `manzanas.py` que contenga la lógica de generación de datos y cálculo de métricas, y un programa principal `main.py` que lo invoque y muestre un informe por pantalla.

**Requerimientos del módulo `manzanas.py`:**

1. `obtener_dias_mes(mes: int) -> int`: Función auxiliar que retorne la cantidad máxima de días de un mes (Febrero = 28; Abril, Junio, Septiembre, Noviembre = 30; el resto = 31).
2. `generar_cosecha(cantidad_registros: int) -> list[dict]`: Genera una lista de diccionarios que simulan manzanas cosechadas. Cada diccionario tendrá la estructura:
* `peso`: Entero aleatorio entre 100 y 600 gramos.
* `id_arbol`: Entero aleatorio de 1 a 100 (representa los 100 árboles del campo).
* `mes`: Entero aleatorio entre 1 y 12.
* `dia`: Entero aleatorio entre 1 y la cantidad máxima de días de ese mes.


3. `calcular_totales(cosecha: list[dict]) -> dict`: Retorna un diccionario con el peso total en kg cosechados y la cantidad total de registros procesados.

#### Plantilla Base - `manzanas.py`

```python
import random

def obtener_dias_mes(mes: int) -> int:
    """Retorna la cantidad máxima de días correspondientes a un mes (1 a 12)."""
    # TODO: Implementar la lógica para retornar 28, 30 o 31 según el mes.
    pass

def generar_cosecha(cantidad_registros: int = 10000) -> list[dict]:
    """Genera una lista de diccionarios con datos aleatorios de cosecha."""
    cosecha = []
    for _ in range(cantidad_registros):
        mes_rand = random.randint(1, 12)
        dias_max = obtener_dias_mes(mes_rand)
        registro = {
            "peso": 0,      # TODO: Valor aleatorio entre 100 y 600
            "id_arbol": 0,  # TODO: Valor aleatorio entre 1 y 100
            "mes": mes_rand,
            "dia": 0        # TODO: Valor aleatorio entre 1 y dias_max
        }
        cosecha.append(registro)
    return cosecha

def calcular_totales(cosecha: list[dict]) -> dict:
    """Calcula el peso total en kilogramos y el total de registros de la cosecha."""
    # TODO: Recorrer la lista, sumar los pesos en gramos y convertir a kg
    return {
        "total_registros": 0,
        "peso_total_kg": 0.0
    }

```

#### Plantilla Base - `main.py`

```python
# TODO: Importar el módulo manzanas adecuadamente

def main() -> None:
    print("=== SIMULADOR DE COSECHA DE MANZANAS ===")
    # 1. Generar la cosecha
    CANTIDAD = 10000
    print(f"Generando {CANTIDAD} registros de cosecha...")
    registros = manzanas.generar_cosecha(CANTIDAD)
    
    # 2. Calcular y mostrar totales
    totales = manzanas.calcular_totales(registros)
    print(f"\nRegistros generados: {totales['total_registros']}")
    print(f"Peso total cosechado: {totales['peso_total_kg']:.2f} kg")

if __name__ == "__main__":
    main()

```

---

### PROG_32

Un tambo automatizado requiere un módulo para registrar las sesiones de ordeñe diarias y monitorear la cadena de frío de la leche en los tanques de recolección.

1. `simular_ordeñe(cantidad_vacas: int, turno: str) -> list[dict]`: Genera una lista de eventos de ordeñe. Cada registro contiene:
* `vaca_id`: Identificador único (1 a cantidad_vacas).
* `litros`: Número aleatorio entre 8.0 y 25.0 litros.
* `temperatura_tanque`: Float aleatorio entre 3.0 °C y 7.0 °C.
* `turno`: Cadena indicando 'Mañana' o 'Tarde'.


2. `filtrar_alertas_cadena_frio(ordeñes: list[dict], temp_limite: float = 4.5) -> list[dict]`: Retorna una lista con únicamente los eventos de ordeñe donde la temperatura del tanque superó el límite de seguridad de conservación.
3. `calcular_promedio_litros(ordeñes: list[dict]) -> float`: Calcula la producción promedio de leche por vaca en el ordeñe.

#### Plantilla Base - `tambo.py`

```python
import random

def simular_ordeñe(cantidad_vacas: int, turno: str) -> list[dict]:
    """Genera registros de ordeñe para un lote de vacas en un turno dado."""
    eventos = []
    for vaca_id in range(1, cantidad_vacas + 1):
        evento = {
            "vaca_id": vaca_id,
            "litros": 0.0,              # TODO: aleatorio entre 8.0 y 25.0
            "temperatura_tanque": 0.0,  # TODO: aleatorio entre 3.0 y 6.5
            "turno": turno
        }
        eventos.append(evento)
    return eventos

def filtrar_alertas_cadena_frio(ordeñes: list[dict], temp_limite: float = 4.5) -> list[dict]:
    """Filtra y retorna aquellos ordeñes cuya temperatura supere la máxima permitida."""
    # TODO: Retornar sublista con eventos cuya temperatura sea mayor a temp_limite
    pass

def calcular_promedio_litros(ordeñes: list[dict]) -> float:
    """Calcula la media de litros recolectados por evento de ordeñe."""
    # TODO: Calcular y retornar el promedio de litros
    pass

```

#### Plantilla Base - `main.py`

```python
import tambo

def main() -> None:
    print("=== SISTEMA DE MONITOREO DE TAMBO ===")
    VACAS = 50
    print(f"Simulando ordeñe de la mañana para {VACAS} vacas...")
    ordeñe_manana = tambo.simular_ordeñe(VACAS, "Mañana")
    
    # Promedio de litros
    promedio = tambo.calcular_promedio_litros(ordeñe_manana)
    print(f"Producción promedio por vaca: {promedio:.2f} litros")
    
    # Control de calidad de temperatura
    alertas = tambo.filtrar_alertas_cadena_frio(ordeñe_manana, temp_limite=4.5)
    print(f"\n[ALERTA DE SEGURIDAD] Se detectaron {len(alertas)} ordeñes fuera de temperatura (< 4.5°C).")

if __name__ == "__main__":
    main()

```

---

### PROG_33

Un vivero necesita un sistema para administrar el catálogo de sus plantas aromáticas y ornamentales, permitiendo actualizar precios por inflación y detectar qué especies requieren riego inmediato.

1. `obtener_catalogo_inicial() -> list[dict]`: Devuelve una lista base con al menos 5 plantas. Cada planta se representa como:
* `id`: Entero identificador.
* `nombre`: Cadena (ej. "Albahaca", "Menta", "Lavanda").
* `precio`: Float.
* `dias_sin_regar`: Entero.
* `frecuencia_riego_dias`: Entero (cada cuántos días debe regarse).


2. `aplicar_aumento_precios(catalogo: list[dict], porcentaje: float) -> list[dict]`: Modifica o genera un catálogo actualizado donde el precio de cada planta se incrementa según el porcentaje indicado.
3. `obtener_plantas_para_regar(catalogo: list[dict]) -> list[dict]`: Filtra y retorna las plantas cuyo `dias_sin_regar` sea igual o mayor a su `frecuencia_riego_dias`.

#### Plantilla Base - `vivero.py`

```python
def obtener_catalogo_inicial() -> list[dict]:
    """Retorna el catálogo por defecto de plantas en el vivero."""
    return [
        {"id": 1, "nombre": "Albahaca", "precio": 1200.0, "dias_sin_regar": 3, "frecuencia_riego_dias": 2},
        {"id": 2, "nombre": "Menta", "precio": 1500.0, "dias_sin_regar": 1, "frecuencia_riego_dias": 2},
        {"id": 3, "nombre": "Lavanda", "precio": 2800.0, "dias_sin_regar": 5, "frecuencia_riego_dias": 4},
        {"id": 4, "nombre": "Romero", "precio": 2100.0, "dias_sin_regar": 2, "frecuencia_riego_dias": 5},
        {"id": 5, "nombre": "Manzanilla", "precio": 1100.0, "dias_sin_regar": 4, "frecuencia_riego_dias": 3},
    ]

def aplicar_aumento_precios(catalogo: list[dict], porcentaje: float) -> list[dict]:
    """Aplica un incremento porcentual al precio de cada planta."""
    # TODO: Recorrer el catálogo y actualizar el campo 'precio' aumentando un 'porcentaje' %
    pass

def obtener_plantas_para_regar(catalogo: list[dict]) -> list[dict]:
    """Retorna aquellas plantas que superaron o igualaron sus días de riego límite."""
    # TODO: Filtrar las plantas donde dias_sin_regar >= frecuencia_riego_dias
    pass

```

#### Plantilla Base - `main.py`

```python
import vivero

def main() -> None:
    print("=== SISTEMA DE GESTIÓN DE VIVERO ===")
    catalogo = vivero.obtener_catalogo_inicial()
    
    # 1. Revisar plantas con necesidad de riego
    a_regar = vivero.obtener_plantas_para_regar(catalogo)
    print("\nPlantas que requieren riego urgente:")
    for p in a_regar:
        print(f" - {p['nombre']}: Lleva {p['dias_sin_regar']} días sin agua (Max: {p['frecuencia_riego_dias']})")
        
    # 2. Actualizar precios
    AUMENTO = 15.0 # 15%
    print(f"\nAplicando aumento del {AUMENTO}% por inflación...")
    vivero.aplicar_aumento_precios(catalogo, AUMENTO)
    print("\nPrecios actualizados:")
    for p in catalogo:
        print(f" - {p['nombre']}: ${p['precio']:.2f}")

if __name__ == "__main__":
    main()

```

---

### USO_DE_TYPEHINTS

Elige tres programas de tu preferencia que implementen funciones que retornen elementos y se declaren variables. Realiza la refactorización utilizando Typehints. Una vez termines, pídele a una IA de tu preferencia que realice la misma tarea. ¿Qué diferencias identificas? Guarda los programas como `PROG_NN_V2` (donde `NN` sea el número original del ejercicio).

---

### PROG_31_v2

A partir de la lista de diccionarios de manzanas obtenida mediante `manzanas.generar_cosecha(10000)`, resolver las siguientes consignas en `main.py` utilizando `filter()`, `map()` y `lambda`:

* **Filtrado de Manzanas de Calidad Premium (`filter`):** Filtrar la cosecha para conservar únicamente las manzanas cuyo peso sea igual o superior a 450 gramos.
```python
premium = list(filter(lambda diccionario: diccionario["peso"] >= 450, cosecha))

```


* **Conversión de Unidades de Peso (`map`):** A partir de la lista filtrada de manzanas premium, utilizar `map()` con una función lambda para generar una lista de floats que contenga el peso de cada manzana convertido a kilogramos ($\text{kg} = \text{g} / 1000$).
```python
pesos_kg = list(map(lambda diccionario: round(diccionario["peso"] / 1000, 3), premium))

```


* **Clasificación por Temporada (`map` con condicional):** Utilizar `map()` y una lambda con operador ternario (`if/else`) para crear una lista de cadenas que clasifique cada registro según el mes: "Primer Semestre" si el mes es de 1 a 6, "Segundo Semestre" si el mes es de 7 a 12.
```python
semestres = list(map(lambda diccionario: "Primer Semestre" if diccionario["mes"] <= 6 else "Segundo Semestre", cosecha))

```



---

### PROG_32_v2

A partir de la lista de eventos de ordeñe obtenida mediante `tambo.simular_ordeñe(100, "Mañana")`, resolver:

* **Hallar el Top 5 Vacas Más Productivas (`sorted` desc):** Ordenar la lista de ordeñes de mayor a menor según la cantidad de litros producidos. Obtener las primeras 5 posiciones (Top 5) e imprimir un reporte con su `vaca_id` y `litros`.
```python
top_5_vacas = sorted(ordeñes, key=lambda o: o["litros"], reverse=True)[:5]

```



---

### PROG_33_v2

A partir del catálogo obtenido mediante `vivero.obtener_catalogo_inicial()`, resolver las siguientes consignas combinando las 3 funciones de orden superior (`filter`, `map`, `sorted`):

* **Ranking por Urgencia de Riego (`sorted`):** Ordenar el catálogo de mayor a menor según la diferencia entre los `dias_sin_regar` y su `frecuencia_riego_dias`.
* *Pista:* `lambda p: p["dias_sin_regar"] - p["frecuencia_riego_dias"]`


* **Simulación de Promoción / Descuento (`map`):** Generar una nueva lista con los precios de las plantas aplicando un 20% de descuento solo a aquellas plantas cuyo precio original sea mayor a $2000.0.
* *Pista:* `lambda p: round(p["precio"] * 0.8, 2) if p["precio"] > 2000 else p["precio"]`


* **Filtrado Complejo de Especies (`filter`):** Filtrar el catálogo para obtener solo las plantas que cumplan dos condiciones simultáneas: que su nombre comience con la letra 'M' o 'L' y que su precio sea menor a $2000.0.
```python
plantas_seleccionadas = list(filter(lambda p: (p["nombre"].startswith("M") or p["nombre"].startswith("L")) and p["precio"] < 2000, catalogo))

```



---

## Unidad 5: Módulos Especiales

*Nota:* Este bloque se realizará íntegramente en un Notebook de Google Colab.

### Álgebra Matricial con NumPy

En computación, el manejo de matrices es la base de los gráficos 3D y la Inteligencia Artificial. Vamos a realizar operaciones fundamentales y comprobar sus propiedades.

**Documentación rápida:**

* `np.array([[a, b], [c, d]])`: Crea una matriz manual.
* `np.linalg.det(A)`: Calcula el determinante.
* `np.linalg.inv(A)`: Calcula la matriz inversa.
* `np.linalg.eigvals(A)`: Obtiene los autovalores (eigenvalues).
* `A @ B` o `np.matmul(A, B)`: Multiplicación de matrices.

**Consigna:**

1. Crea una matriz $A$ de $2 \times 2$ con los valores:

$$\begin{pmatrix} 4 & 7 \\ 2 & 6 \end{pmatrix}$$


2. Calcula su Determinante.
3. Calcula sus Autovalores.
4. Calcula su Matriz Inversa ($A^{-1}$).
5. **Demostración:** Multiplica $A$ por $A^{-1}$ y verifica que el resultado sea la Matriz Identidad $\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$ (puedes usar `np.round()` para limpiar decimales ínfimos).

---

### De Diccionarios a DataFrames con Pandas

Pandas nos permite trabajar con datos como si fueran planillas de Excel, pero con la potencia de Python.

**Guía de pasos sugerida:**

1. **Definir los datos:** Crear un diccionario donde las claves sean los nombres de las columnas (ej: `"Producto"`, `"Ventas"`) y los valores sean listas con los datos.
2. **Crear el DataFrame:** Usar `pd.DataFrame(mi_diccionario)`.
3. **Analizar:** Usa el método `.describe()` para obtener estadísticas rápidas. Podemos ver los datos de cabecera con `.head()`.

**Consigna:**
Registramos la producción de 4 variedades de manzanas. Crear un DataFrame con los siguientes datos:

```python
datos = {
    "Variedad": ["Red Delicious", "Gala", "Granny Smith", "Fuji"],
    "Toneladas": [45, 38, 20, 32],
    "Precio_USD": [1200, 1500, 1300, 1600]
}

```

* **Variedad:** "Red Delicious", "Gala", "Granny Smith", "Fuji".
* **Toneladas:** 45, 38, 20, 32.
* **Precio:** 1200, 1500, 1300, 1600.

**Informe solicitado:**

* Mostrar las primeras 2 filas del DataFrame.
* Calcular el promedio de toneladas cosechadas.
* Agregar una nueva columna llamada `"Total_Ingresos"` que sea el resultado de multiplicar `Toneladas * Precio_USD`.
```python
df["Total_Ingresos"] = df["Toneladas"] * df["Precio_USD"]

```



---

### Visualización de Resultados con Matplotlib

Vamos a graficar los datos del ejercicio anterior.

**Consigna:**
Utilizando el DataFrame de las manzanas, generar los siguientes gráficos:

1. **Gráfico de Barras (Comparativo):**
* **Eje X:** Variedad.
* **Eje Y:** Toneladas.
* **Objetivo:** Ver qué variedad produjo más cantidad.


2. **Gráfico de Torta (Proporcional):**
* **Datos:** `"Total_Ingresos"`.
* **Etiquetas:** Variedad.
* **Objetivo:** Ver qué variedad aportó más dinero al total.


3. **Gráfico X-Y / Dispersión (Relacional):**
* **Eje X:** Toneladas.
* **Eje Y:** Precio.
* **Objetivo:** Analizar si a mayor producción, el precio tiende a subir o bajar.



#### Plantilla Base (Colab)

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- EJERCICIO: NUMPY ---
print("--- NumPy: Matriz 2x2 ---")
A = np.array([[4, 7], [2, 6]])
# TODO: Calcular Det, Inv y multiplicar

# --- EJERCICIO: PANDAS ---
print("\n--- Pandas: Diccionario a DataFrame ---")
datos = {
    "Variedad": ["Red Delicious", "Gala", "Granny Smith", "Fuji"],
    "Toneladas": [45, 38, 20, 32],
    "Precio_USD": [1200, 1500, 1300, 1600]
}
df = pd.DataFrame(datos)
# TODO: Realizar cálculos e informes

# --- EJERCICIO: MATPLOTLIB ---
print("\n--- Matplotlib: Gráficos ---")
# Ejemplo Barras:
plt.figure(figsize=(8, 4))
plt.bar(df["Variedad"], df["Toneladas"], color='#0077C1')
plt.title("Producción por Variedad")
plt.xlabel("Variedad")
plt.ylabel("Toneladas")
plt.show()

# TODO: Realizar gráfico de torta y X-Y

```

#### Guía de Referencia Matplotlib

##### Gráfico de Torta:

```python
import matplotlib.pyplot as plt

# 1. Definimos si queremos "despegar" alguna porción (0 = pegada, 0.1 = separada)
desfase = (0.1, 0, 0, 0)
plt.figure(figsize=(6, 6))

# 2. Generamos el gráfico de torta
plt.pie(
    df["Total_Ingresos"],                                 # Los valores numéricos
    labels=df["Variedad"],                                # Las etiquetas
    autopct='%1.1f%%',                                    # Formato porcentaje
    explode=desfase,                                      # Despega la porción
    startangle=140,                                       # Ángulo inicial
    colors=['#0077C1', '#0070C0', '#48dbfb', '#10ac84']   # Colores
)
plt.title("Proporción de Ingresos Totales por Variedad", fontsize=14)
plt.show()

```

##### Gráfico X-Y (Scatter):

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(7, 5))

# 1. Creamos el gráfico de dispersión (X = Toneladas, Y = Precio_USD)
plt.scatter(
    df["Toneladas"],
    df["Precio_USD"],
    color='#C00000',
    s=120,
    alpha=0.8
)

# 2. Agregamos etiquetas a cada punto
for i in range(len(df)):
    plt.annotate(
        df["Variedad"][i],
        (df["Toneladas"][i] + 0.5, df["Precio_USD"][i] + 10)
    )

# 3. Títulos y ejes
plt.title("Relación entre Producción (Toneladas) y Precio (USD)", fontsize=14)
plt.xlabel("Toneladas Cosechadas")
plt.ylabel("Precio por Tonelada (USD)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

```

##### Resumen de Funciones:

| Tipo de Gráfico | Función | ¿Cuándo usarlo? |
| --- | --- | --- |
| **Barras** | `plt.bar(x, y)` | Para comparar cantidades absolutas entre categorías. |
| **Torta** | `plt.pie(valores, labels=...)` | Para ver la participación porcentual sobre un total ($100\%$). |
| **Scatter (X-Y)** | `plt.scatter(x, y)` | Para ver si dos variables numéricas están correlacionadas. |