"""
REQUISITOS DEL TRABAJO PRACTICO (TPO – SPRINT) — Programacion I
Facultad de Ingenieria Informatica

Modulo: crud.py — Gestion CRUD del catalogo de autos.
Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).

--------------------------------------------------------------------------------
OBJETIVO DEL TRABAJO
--------------------------------------------------------------------------------
Aplicar los conocimientos vistos en clase sobre archivos/JSON y manejo de
excepciones, ademas de los requisitos minimos del programa.

--------------------------------------------------------------------------------
PAUTAS / REQUISITOS DEL TP
--------------------------------------------------------------------------------
1) MANEJO DE EXCEPCIONES:
Usar manejo de excepciones en todos los metodos que requieran:
- Ingreso de datos.
- Conversion de enteros o flotantes.
- Manipulacion de diccionarios.
- Apertura / cierre de archivos.

2) PERSISTENCIA DE INFORMACION:
Guardar y procesar los datos mediante un archivo JSON (autos.json).
Create, Update y Delete deben SOBREESCRIBIR el archivo con la ultima
version del diccionario; Read puede leer esa ultima version.
(Se valora especialmente implementar las DOS opciones de persistencia).

3) PRECARGA DE INFORMACION:
Los datos ya no se cargan desde la memoria del programa, sino desde un
archivo inicial (autos.json). Se requiere una precarga de al menos 5 registros.

4) TUPLA O CONJUNTO:
Incluir el uso de una tupla o un conjunto como parte de la logica
(por ejemplo, para validaciones o estructuras de datos).
En este modulo: CALIDADES, MARCAS y CATEGORIAS son tuplas.

5) LISTA POR COMPRENSION O LAMBDA:
Incorporar al menos una lista por comprension o una funcion lambda
aplicada a la informacion.
-> TODO(TP - Req 5): Agregar/explicitar al menos un uso de lista por
    comprension o de lambda que procese los datos del catalogo.

6) ENTIDAD PRINCIPAL:
Representar la entidad principal con un DICCIONARIO DE DICCIONARIOS,
con un minimo de 5 atributos por elemento.
En este modulo: autos = {patente: {marca, modelo, calidad, ano, precio, categoria}}.

7) MENU CRUD COMPLETO:
Create (agregar_auto), Read (ver_autos / ver_auto),
Update (modificar_auto), Delete (eliminar_auto).

8) REPORTE MATRICIAL:
Generar al menos un reporte matricial (listas de listas) con informacion
procesada del conjunto. Recomendado: NumPy, Pandas y Matplotlib.
-> TODO(TP - Req 8): Este reporte se implementa en el modulo informe.py.

9) DOCUMENTACION Y ENTREGA:
Uso de docstrings en las funciones, codigo claro y organizado, validacion
de datos mediante funciones y entrega del informe en Word.

--------------------------------------------------------------------------------
CHECKLIST DE CUMPLIMIENTO (crud.py)
--------------------------------------------------------------------------------
[x] Entidad con diccionario de diccionarios y >= 5 atributos.
[x] Tuplas para validaciones (CALIDADES, MARCAS, CATEGORIAS).
[x] CRUD completo y menu en consola.
[x] Docstrings en las funciones.
[x] Persistencia en JSON (leer / escribir).
[ ] Req 1: Manejo de excepciones en carga/guardado y validaciones.
[ ] Req 5: Lista por comprension o lambda aplicada a la informacion.
[ ] Req 3: Garantizar/documentar que autos.json tenga >= 5 registros.
[ ] Req 8: Reporte matricial (ver modulo informe.py).

NOTA: Esta version solo AGREGA documentacion y marcas TODO(TP) para indicar
lo que falta. NO se modifico ninguna linea de logica del programa.
"""

import json, os
import informe as inf


# ==========================================
# CONFIGURACION Y CONSTANTES
# ==========================================

# Ruta del archivo JSON donde se guarda el catalogo de autos.
# (Req 2 y 3 del TP: persistencia y precarga desde archivo).
RUTA_AUTOS = inf.RUTA_AUTOS_JSON

# Tuplas con los valores permitidos para cada campo.
# (Req 4 del TP: uso de tuplas como parte de la logica / validaciones).
CALIDAD = inf.CALIDADES
MARCA = inf.MARCAS
CATEGORIA = inf.CATEGORIAS

# Mapeo entre la opcion numerica del menu de modificacion y el campo del JSON.
# Formato: "clave de menu": ("nombre del campo en el JSON", "nombre para mostrar").
# Se usa para no repetir la lista de campos editables en varios lugares.
CAMPOS = {
    "1": ("marca", "Marca"),
    "2": ("modelo", "Modelo"),
    "3": ("calidad", "Calidad"),
    "4": ("año", "Año"),
    "5": ("precio", "Precio"),
    "6": ("categoria", "Categoría"),
}

def limpiar():
    """
    Limpia la consola segun el sistema operativo.

    En Windows usa 'cls'; en Linux/macOS usa 'clear'. Sirve para mantener la
    interfaz ordenada entre pantallas del menu.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# ---------- Persistencia ----------

def _cargar_autos() -> dict[dict]:
    """
    Carga el catalogo de autos desde el archivo JSON.

    Lee el contenido de `autos.json` y lo convierte a un diccionario de Python,
    donde cada clave es la patente del auto y cada valor es otro diccionario con
    sus atributos (diccionario de diccionarios).

    Returns:
        dict: Estructura {patente: {marca, modelo, calidad, ano, precio, categoria}, ...}.

    Raises:
        FileNotFoundError: Si el archivo autos.json no existe.
        OSError: Si ocurre un problema a nivel operativo
    """
    # TODO(TP - Req 1): envolver en try/except para manejar apertura/lectura
    # del archivo (FileNotFoundError, json.JSONDecodeError, OSError).
    try: 
        with open(RUTA_AUTOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        input("[Enter] ")


def _guardar_autos(autos):
    """
    Escribe el catalogo de autos en el archivo JSON.

    Sobreescribe `autos.json` con la ultima version del diccionario recibido,
    manteniendo un formato legible (indentado) y conservando los acentos.
    (Req 2 del TP: Create/Update/Delete sobreescriben el archivo).

    Args:
        autos (dict): Diccionario con el catalogo a guardar.

    Raises:
        OSError: Si ocurre un error al abrir o escribir el archivo.
        TypeError: Si algun valor no es serializable a JSON.
    """
    # TODO(TP - Req 1): envolver en try/except para el guardado (OSError)
    # y validar que 'autos' sea un diccionario antes de escribir.
    try:
        with open(RUTA_AUTOS, "w", encoding="utf-8") as archivo:
            json.dump(autos, archivo, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        print(f"/// ¡El archivo {RUTA_AUTOS} no existe! ///")
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        input("[Enter] ")


# ---------- Validaciones de entrada ----------

def _pedir_de_tupla(etiqueta, opciones):
    """
    Pide un valor que obligatoriamente debe estar dentro de 'opciones'.

    Repite la solicitud hasta que el usuario ingrese una opcion valida. Se usa
    para campos con valores predefinidos (marca, calidad, categoria).

    Args:
        etiqueta (str): Nombre del campo a pedir (ej. "Marca").
        opciones (tuple): Tupla con los valores validos aceptados.

    Returns:
        str: Valor elegido por el usuario, en minusculas y validado.
    """
    print(f"{etiqueta} (opciones: {', '.join(opciones)}): ")
    valor = input().strip().lower()
    # Bucle de validacion: no se sale hasta que el valor pertenezca a 'opciones'.
    while valor not in opciones:
        print(f"Valor inválido. {etiqueta} debe ser una de: {', '.join(opciones)}")
        valor = input().strip().lower()
    return valor


def _pedir_entero(etiqueta, minimo, maximo):
    """
    Pide un numero entero dentro de un rango.

    Valida que la entrada sea numerica y que este entre `minimo` y `maximo`
    (inclusive), repitiendo la solicitud hasta obtener un valor correcto.

    Args:
        etiqueta (str): Nombre del campo a pedir (ej. "Ano").
        minimo (int): Valor minimo permitido.
        maximo (int): Valor maximo permitido.

    Returns:
        int: Numero entero valido ingresado por el usuario.
    """
    # TODO(TP - Req 1): convertir con try/except (ValueError) en lugar de
    # depender solo de .isdigit(), para un manejo de excepciones mas robusto.
    valor = input(f"{etiqueta} ({minimo}-{maximo}): ").strip()
    # Se repite mientras no sea un digito o este fuera del rango permitido.
    while not valor.isdigit() or not (minimo <= int(valor) <= maximo):
        valor = input(f"Inválido. {etiqueta} debe ser un número entre {minimo} y {maximo}: ").strip()
    return int(valor)


def _pedir_float(etiqueta):
    """
    Pide un numero decimal positivo (acepta coma o punto).

    Reemplaza la coma por punto para aceptar ambas notaciones y repite la
    solicitud hasta que se ingrese un numero convertible a float mayor a 0.

    Args:
        etiqueta (str): Nombre del campo a pedir (ej. "Precio (u$d)").

    Returns:
        float: Valor decimal positivo ingresado por el usuario.
    """
    valor = input(f"{etiqueta}: ").strip().replace(",", ".")
    while True:
        try:
            numero = float(valor)
            # Solo se acepta si el numero es positivo.
            if numero > 0:
                return numero
        except ValueError:
            # Si no se puede convertir a float, se vuelve a pedir el valor.
            pass
        valor = input(f"Inválido. {etiqueta} debe ser un número positivo: ").strip().replace(",", ".")


def _pedir_patente_existente(autos : dict) -> str:
    """
    Pide una patente y valida que ya exista en el catalogo.

    Convierte la patente a mayusculas para mantener coherencia con el formato
    usado en el JSON y repite la solicitud hasta que exista.

    Args:
        autos (dict): Diccionario con el catalogo cargado.

    Returns:
        str: Patente existente, en mayusculas.
    """
    # TODO(TP - Req 1): validar el tipo de 'autos' (dict) para evitar errores
    # al manipular diccionarios si llega un valor inesperado.
    if not autos:
            print("\nNo hay autos en el catálogo.")
            try: input("[Enter] ")
            except: pass
            return
    patente = input("Ingrese la patente del auto: ").strip().upper()
    while patente not in autos:
        patente = input("Patente no encontrada. Ingrese una patente válida: ").strip().upper()
    return patente


# ---------- Mostrar ----------

def _mostrar_auto(patente, datos):
    """
    Muestra por pantalla la informacion completa de un auto.

    Imprime la ficha del auto (patente, marca, modelo, calidad, ano, precio y
    categoria) con un formato legible.

    Args:
        patente (str): Patente del auto (clave del diccionario).
        datos (dict): Diccionario con los atributos del auto.
    """
    # TODO(TP - Req 1): proteger el acceso a claves con try/except (KeyError)
    # por si al auto le falta algun atributo en el JSON.
    print(f"\n[{patente}]")
    print(f"\tMarca: {datos['marca'].capitalize()}")
    print(f"\tModelo: {datos['modelo'].capitalize()}")
    print(f"\tCalidad: {datos['calidad']}")
    print(f"\tAño: {datos['año']}")
    print(f"\tPrecio: u$d {datos['precio']:.1f}")
    print(f"\tCategoría: {datos['categoria']}")


# ---------- READ ----------

def ver_stock():
    """
    Muestra todo el catalogo de autos (lectura general / Read).

    Carga el archivo JSON y, si hay autos, los lista uno por uno usando
    `_mostrar_auto()`. Si el catalogo esta vacio, lo informa.
    """
    autos = _cargar_autos()
    # Si el diccionario esta vacio, no hay nada para mostrar.
    if not autos:
        print("\nNo hay autos en el catálogo.")
        try: input("[Enter] ")
        except: pass
        return
    print("\n--- CATÁLOGO DE AUTOS ---")
    # Recorre cada par (patente, datos) del diccionario de diccionarios.
    # TODO(TP - Req 5): aqui se podria aplicar una lista por comprension
    # o una lambda para generar un resumen del catalogo.
    for patente, datos in autos.items():
        _mostrar_auto(patente, datos)
        try: 
            res = input(" ")
            if res == "q":
                return
        except: pass


def ver_auto():
    """
    Muestra un auto segun su patente (lectura individual / Read).

    Pide una patente existente y muestra unicamente la ficha de ese auto.
    Si el catalogo esta vacio, lo informa.
    """
    autos = _cargar_autos()
    if not autos:
        print("\nNo hay autos en el catálogo.")
        try: input(" ")
        except: pass
        return
    patente = _pedir_patente_existente(autos)
    _mostrar_auto(patente, autos[patente])
    try: 
        input("\n Presiona ENTER para volver")
    except:
        pass


# ---------- CREATE ----------

def agregar_auto():
    """
    Da de alta un auto nuevo (Create).

    Pide todos los datos del auto y valida que la patente no exista previamente.
    Al finalizar, guarda la ultima version del diccionario en el archivo JSON.
    (Req 2 del TP: Create sobreescribe el archivo).
    """
    # TODO(TP - Req 1): manejar excepciones en la carga y en el guardado.
    autos = _cargar_autos()

    # Se pide la patente y se valida que no exista (una patente es unica).
    patente = input("Patente del nuevo auto: ").strip().upper()
    while patente in autos:
        patente = input("Esa patente ya existe. Ingrese otra: ").strip().upper()

    # Se piden y validan los demas atributos del auto.
    marca = _pedir_de_tupla("Marca: ", inf.MARCAS)
    modelo = input("Modelo: ").strip().lower()
    calidad = _pedir_de_tupla("Calidad:", inf.CALIDADES)
    anio = _pedir_entero("Año: ", 2000, 2026)
    precio = _pedir_float("Precio (u$d): ")
    categoria = _pedir_de_tupla("Categoría: ", inf.CATEGORIAS)

    # Se crea el registro usando la patente como clave del diccionario.
    autos[patente] = {
        "marca": marca,
        "modelo": modelo,
        "calidad": calidad,
        "año": anio,
        "precio": precio,
        "categoria": categoria,
    }
    # Se persiste el cambio y se confirma al usuario.
    _guardar_autos(autos)
    print(f"\nAuto {patente} agregado correctamente.")


# ---------- UPDATE ----------

def modificar_auto():
    """
    Modifica uno o mas campos de un auto existente (Update).

    Pide una patente valida, muestra los valores actuales y permite cambiar el
    campo elegido. Despues de cada cambio se guarda automaticamente en el JSON.
    (Req 2 del TP: Update sobreescribe el archivo).

    El bucle se repite hasta que el usuario elige la opcion [0] salir.
    """
    # TODO(TP - Req 1): manejar excepciones en la carga y en el guardado.
    autos = _cargar_autos()
    if not autos:
            print("\nNo hay autos en el catálogo.")
            try: input("[Enter] ")
            except: pass
            return

    patente = _pedir_patente_existente(autos)

    while True:
        # Muestra el menu de campos con su valor actual.
        print(f"\n--- Modificar auto [{patente}] ---")
        for clave, (campo, nombre) in CAMPOS.items():
            print(f"[{clave}] {nombre}: {autos[patente][campo]}")
        print("[0] Terminar")

        opcion = input("\n¿Qué campo desea modificar?: ").strip()

        # Opcion para salir del menu de modificacion.
        if opcion == "0":
            break
        # Validacion de la opcion ingresada.
        elif opcion not in CAMPOS:
            print("\nOpción no válida. Intente de nuevo.")
            continue

        # Se traduce la opcion a (campo del JSON, nombre visible).
        campo, nombre = CAMPOS[opcion]

        # Se pide el nuevo valor segun el tipo de campo elegido.
        if campo == "marca":
            autos[patente]["marca"] = _pedir_de_tupla("Marca", inf.MARCAS)
        elif campo == "modelo":
            autos[patente]["modelo"] = input("Nuevo modelo: ").strip().lower()
        elif campo == "calidad":
            autos[patente]["calidad"] = _pedir_de_tupla("Calidad", inf.CALIDADES)
        elif campo == "año":
            autos[patente]["año"] = _pedir_entero("Año", 2000, 2026)
        elif campo == "precio":
            autos[patente]["precio"] = _pedir_float("Nuevo precio (u$d)")
        elif campo == "categoria":
            autos[patente]["categoria"] = _pedir_de_tupla("Categoría", inf.CATEGORIAS)

        # Se guarda el cambio y se confirma.
        _guardar_autos(autos)
        print(f"\n{nombre} actualizado correctamente.")


# ---------- DELETE ----------

def eliminar_auto():
    """
    Elimina un auto del catalogo segun su patente (Delete).

    Pide una patente existente, borra el registro del diccionario y sobreescribe
    el archivo JSON con la ultima version.
    (Req 2 del TP: Delete sobreescribe el archivo).
    """
    # TODO(TP - Req 1): manejar excepciones en la carga y en el guardado.
    autos = _cargar_autos()
    if not autos:
            print("\nNo hay autos en el catálogo.")
            try: input("[Enter] ")
            except: pass
            return

    patente = _pedir_patente_existente(autos)
    # Se elimina el registro del diccionario y se guarda el estado actualizado.
    del autos[patente]
    _guardar_autos(autos)
    print(f"\nAuto {patente} eliminado correctamente.")


# ---------- Menu ----------

def menu_crud():
    """
    Muestra y gestiona el menu principal del CRUD de autos.

    Ofrece ver el catalogo, ver un auto, agregar, modificar, eliminar o salir.
    Redirige a la funcion correspondiente segun la opcion elegida y se mantiene
    activo hasta que se selecciona [0] Salir.
    """
    while True:
        limpiar()
        print("\n--- CRUD DE AUTOS ---")
        print("[1] Ver catálogo")
        print("[2] Ver un auto")
        print("[3] Agregar auto")
        print("[4] Modificar auto")
        print("[5] Eliminar auto")
        print("[0] Salir")
        # TODO(TP - Req 1): manejar excepciones en el ingreso de datos.
        opcion = input("Seleccione una opción: ").strip()

        # Despacho de la opcion elegida hacia la funcion correspondiente.
        if opcion == "1":
            ver_stock()
        elif opcion == "2":
            ver_auto()
        elif opcion == "3":
            agregar_auto()
        elif opcion == "4":
            modificar_auto()
        elif opcion == "5":
            eliminar_auto()
        elif opcion == "0":
            # Salir del menu CRUD.
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")


if __name__ == "__main__":
    # Punto de entrada: ejecuta el menu CRUD si se corre este archivo directamente.
    # TODO(TP - Req 3): verificar que autos.json contenga al menos 5 registros (precarga).
    menu_crud()
