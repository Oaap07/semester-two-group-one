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

### PROG_13 - BUSCAR Y EXTRAER MALETA

En la bodega de un avion, las valijas se apilan en dos filas paralelas (Pila A y Pila B). Cada valija tiene un codigo de etiqueta unico. Cuando un pasajero reclama una valija por su codigo, el operario debe retirarla. Sin embargo, como estan apiladas, para sacar una valija que esta abajo, primero se deben desapilar temporalmente las que estan arriba.

**FUNCION A DESARROLLAR:**
- buscar_y_extraer_maleta(pila_a, pila_b, etiqueta_buscada):
  - Entrada: Dos listas (pila_a y pila_b) y la etiqueta (string/int) de la maleta buscada.
  - Proceso: Busca la maleta en la pila_a. Si no esta, busca en la pila_b. Utiliza una pila auxiliar para guardar temporalmente las maletas que estan encima de la buscada. Una vez extraida la maleta solicitada, se devuelven las demas a su pila original en el orden correcto.
  - Retorno: True si la maleta fue encontrada y extraida, False si no existia en ninguna de las dos filas.

### PROG_14 - CLASIFICAR PRODUCTOS

Un centro de logistica recibe productos desde la linea de produccion. Algunos productos estan en optimo estado y otros presentan fallas ("roto"). El sistema cuenta con dos camiones de transporte (Pila Camion Sano y Pila Camion Defectuoso).

**FUNCIONES A DESARROLLAR:**
- clasificar_productos(pila_recepcion, camion_envio, defectuosos):
  - Entrada: Una Pila de recepcion con tuplas del tipo (id_producto, estado).
  - Proceso: Vacia la pila de recepcion desapilando elemento por elemento. Si el producto tiene estado "roto" o "defectuoso", lo apila en defectuosos. En caso contrario, lo apila en camion_envio.
  - Retorno: Un resumen con la cantidad total de productos clasificados.

### PROG_15 - TREN DE MERCANCIAS

Un tren de mercancias esta compuesto por una lista de vagones. Cada vagon funciona como una pila con una capacidad maxima de peso (en kg). A medida que llegan paquetes con pesos aleatorios, se deben apilar en el vagon actual. Cuando el siguiente paquete supere la capacidad restante del vagon, ese vagon se "sella" y se debe pasar al siguiente vagon (siguiente pila).

**FUNCIONES A DESARROLLAR:**
- generar_paquete(peso_min, peso_max): Funcion que retorna aleatoriamente el peso de un paquete a cargar. Recomendacion: los paquetes pesan entre 10 y 40.
- cargar_vagon(tren, vagon_numero, paquete): Funcion que retorna la informacion del tren una vez terminada la carga del vagon. Recibe como parametro la "matriz" (dado que el tren representa la matriz y cada fila los vagones del tren), la posicion actual para la carga y una tupla compuesta de informacion del paquete y el peso. El vagon tiene un limite de 150.
- mostrar(tren): Mostrar informe de carga.

### PROG_16 - GESTION DE TURNOS DE PACIENTES

Un centro de salud necesita un sistema en consola para gestionar el turno de atencion de los pacientes a medida que van arribando a la sala de espera. Deberemos implementar una estructura de datos de tipo Cola (Queue) simulado con listas para gestionar la recepcion y atencion de pacientes siguiendo un orden estrictamente secuencial (Primero en Llegar, Primero en Ser Atendido). Trabajaremos con tres listas sincronizadas, cada posicion es un paciente unico. La primer lista almacena el dni, la segunda el primer nombre y la tercera el apellido.

**FUNCIONES A GENERAR:**
- mostrar_lista_espera: Muestra los pacientes en sala de espera pendientes en el orden en que seran atendidos.
- cargar_paciente: Carga un paciente al final de la cola.
- atender_paciente: Se anuncia el paciente que sera atendido y se lo elimina de la lista.

**IMPORTANTE:** si no hay pacientes, no podemos eliminar de la lista, por lo que debemos validar que haya pacientes para que no interrumpa el programa.

### PROG_17 - COLA DE PACIENTES PRIORITARIOS

El centro de salud ha decidido implementar un protocolo de atencion rapida para pacientes prioritarios (embarazadas, personas con movilidad reducida o adultos mayores). Al programa anterior, le haremos la siguiente mejora: al registrar un paciente, el sistema preguntara si se trata de un caso Prioritario.

**COMPORTAMIENTO EN LA COLA (DIFICULTAD INTERMEDIA):**
- Si la cola esta vacia, el paciente prioritario ingresa normalmente.
- Si ya hay personas esperando, el paciente prioritario se ubica inmediatamente en el segundo puesto de la cola (es decir, justo detras de la persona que esta a punto de ser llamada, respetando la atencion de quien ya estaba esperando al frente).

**DIFICULTAD AVANZADA (OPCIONAL):**
- Si ingresa un nuevo paciente prioritario y ya hay otro en el segundo puesto, el nuevo se ubica detras de los prioritarios existentes, pero delante de la lista general.

### PROG_18 - ESTACION DE PEAJE

El sistema central de la autopista te ha encargado desarrollar el modulo de control para una estacion con 3 cabinas de peaje. Tu objetivo es procesar la atencion de los vehiculos fila por fila, cobrando las tarifas correspondientes y administrando el flujo de autos que van llegando a la estacion.

**REGLAS DE LA SIMULACION:**
- Estructura del Peaje: El peaje cuenta con 3 colas (cola_1, cola_2, cola_3). Las 3 colas estan agrupadas dentro de una lista principal llamada peaje.
- Cobro y Tarifas: Cada vez que se atiende (desencolado) a un vehiculo de la cabina elegida, se cobra una tarifa segun el tipo: Moto: $1500, Auto: $2000, Camion: $5000.
- Flujo de Arribo (El Turno): Cada vez que se atiende a un vehiculo con exito, hay un 60% de probabilidad de que ingrese un nuevo vehiculo a la estacion. Este nuevo vehiculo (Moto, Auto o Camion) se asignara automaticamente a una de las 3 colas de forma aleatoria.
- Validacion: No se puede atender una cola que este vacia. Si el usuario elige una cola vacia, el programa debe mostrar un mensaje de advertencia y solicitar de nuevo la opcion sin perder el turno.
- Se debe mostrar la recaudacion total.

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
