"""
REQUISITOS DEL TRABAJO PRÁCTICO (TPO – SPRINT) — Programación I
Facultad de Ingeniería Informática

Módulo: crud.py — Gestión CRUD del catálogo de autos.
Tema del trabajo: Administración de una concesionaria (catálogo de autos + alquileres).

--------------------------------------------------------------------------------
OBJETIVO DEL TRABAJO
--------------------------------------------------------------------------------
Aplicar los conocimientos vistos en clase sobre archivos/JSON y manejo de
excepciones, además de los requisitos mínimos del programa.

--------------------------------------------------------------------------------
PAUTAS / REQUISITOS DEL TP
--------------------------------------------------------------------------------
1) MANEJO DE EXCEPCIONES:
Usar manejo de excepciones en todos los métodos que requieran:
- Ingreso de datos.
- Conversión de enteros o flotantes.
- Manipulación de diccionarios.
- Apertura / cierre de archivos.

2) PERSISTENCIA DE INFORMACIÓN:
Guardar y procesar los datos mediante un archivo JSON (autos.json).
Create, Update y Delete deben SOBREESCRIBIR el archivo con la última
versión del diccionario; Read puede leer esa última versión.
(Se valora especialmente implementar las DOS opciones de persistencia).

3) PRECARGA DE INFORMACIÓN:
Los datos ya no se cargan desde la memoria del programa, sino desde un
archivo inicial (autos.json). Se requiere una precarga de al menos 5 registros.

4) TUPLA O CONJUNTO:
Incluir el uso de una tupla o un conjunto como parte de la lógica
(por ejemplo, para validaciones o estructuras de datos).
En este módulo: CALIDADES, MARCAS y CATEGORIAS son tuplas.

5) LISTA POR COMPRENSIÓN O LAMBDA:
Incorporar al menos una lista por comprensión o una función lambda
aplicada a la información.
-> TODO(TP - Req 5): Agregar/explicitar al menos un uso de lista por
    comprensión o de lambda que procese los datos del catálogo.

6) ENTIDAD PRINCIPAL:
Representar la entidad principal con un DICCIONARIO DE DICCIONARIOS,
con un mínimo de 5 atributos por elemento.
En este módulo: autos = {patente: {marca, modelo, calidad, año, precio, categoria}}.

7) MENÚ CRUD COMPLETO:
Create (agregar_auto), Read (ver_autos / ver_auto),
Update (modificar_auto), Delete (eliminar_auto).

8) REPORTE MATRICIAL:
Generar al menos un reporte matricial (listas de listas) con información
procesada del conjunto. Recomendado: NumPy, Pandas y Matplotlib.
-> TODO(TP - Req 8): Este reporte se implementa en el módulo informe.py.

9) DOCUMENTACIÓN Y ENTREGA:
Uso de docstrings en las funciones, código claro y organizado, validación
de datos mediante funciones y entrega del informe en Word.

--------------------------------------------------------------------------------
CHECKLIST DE CUMPLIMIENTO (crud.py)
--------------------------------------------------------------------------------
[x] Entidad con diccionario de diccionarios y >= 5 atributos.
[x] Tuplas para validaciones (CALIDADES, MARCAS, CATEGORIAS).
[x] CRUD completo y menú en consola.
[x] Docstrings en las funciones.
[x] Persistencia en JSON (leer / escribir).
[ ] Req 1: Manejo de excepciones en carga/guardado y validaciones.
[ ] Req 5: Lista por comprensión o lambda aplicada a la información.
[ ] Req 3: Garantizar/documentar que autos.json tenga >= 5 registros.
[ ] Req 8: Reporte matricial (ver módulo informe.py).

NOTA: Esta versión solo AGREGA documentación y marcas TODO(TP) para indicar
lo que falta. NO se modificó ninguna línea de lógica del programa.
"""

import json, os
import informe as inf


# ==========================================
# CONFIGURACIÓN Y CONSTANTES
# ==========================================

# Ruta del archivo JSON donde se guarda el catálogo de autos.
# (Req 2 y 3 del TP: persistencia y precarga desde archivo).
RUTA_AUTOS = inf.RUTA_AUTOS_JSON

# Tuplas con los valores permitidos para cada campo.
# (Req 4 del TP: uso de tuplas como parte de la lógica / validaciones).
CALIDAD = inf.CALIDADES
MARCA = inf.MARCAS
CATEGORIA = inf.CATEGORIAS

# Mapeo entre la opción numérica del menú de modificación y el campo del JSON.
# Formato: "clave de menú": ("nombre del campo en el JSON", "nombre para mostrar").
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
    Limpia la consola según el sistema operativo.

    En Windows usa 'cls'; en Linux/macOS usa 'clear'. Sirve para mantener la
    interfaz ordenada entre pantallas del menú.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# ---------- Persistencia ----------

def _cargar_autos() -> dict[dict]:
    """
    Carga el catálogo de autos desde el archivo JSON.

    Lee el contenido de `autos.json` y lo convierte a un diccionario de Python,
    donde cada clave es la patente del auto y cada valor es otro diccionario con
    sus atributos (diccionario de diccionarios).

    Returns:
        dict: Estructura {patente: {marca, modelo, calidad, año, precio, categoria}, ...}.

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
    Escribe el catálogo de autos en el archivo JSON.

    Sobreescribe `autos.json` con la última versión del diccionario recibido,
    manteniendo un formato legible (indentado) y conservando los acentos.
    (Req 2 del TP: Create/Update/Delete sobreescriben el archivo).

    Args:
        autos (dict): Diccionario con el catálogo a guardar.

    Raises:
        OSError: Si ocurre un error al abrir o escribir el archivo.
        TypeError: Si algún valor no es serializable a JSON.
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

    Repite la solicitud hasta que el usuario ingrese una opción válida. Se usa
    para campos con valores predefinidos (marca, calidad, categoría).

    Args:
        etiqueta (str): Nombre del campo a pedir (ej. "Marca").
        opciones (tuple): Tupla con los valores válidos aceptados.

    Returns:
        str: Valor elegido por el usuario, en minúsculas y validado.
    """
    print(f"{etiqueta} (opciones: {', '.join(opciones)}): ")
    valor = input().strip().lower()
    # Bucle de validación: no se sale hasta que el valor pertenezca a 'opciones'.
    while valor not in opciones:
        print(f"Valor inválido. {etiqueta} debe ser una de: {', '.join(opciones)}")
        valor = input().strip().lower()
    return valor


def _pedir_entero(etiqueta, minimo, maximo):
    """
    Pide un número entero dentro de un rango.

    Valida que la entrada sea numérica y que esté entre `minimo` y `maximo`
    (inclusive), repitiendo la solicitud hasta obtener un valor correcto.

    Args:
        etiqueta (str): Nombre del campo a pedir (ej. "Año").
        minimo (int): Valor mínimo permitido.
        maximo (int): Valor máximo permitido.

    Returns:
        int: Número entero válido ingresado por el usuario.
    """
    # TODO(TP - Req 1): convertir con try/except (ValueError) en lugar de
    # depender solo de .isdigit(), para un manejo de excepciones más robusto.
    valor = input(f"{etiqueta} ({minimo}-{maximo}): ").strip()
    # Se repite mientras no sea un dígito o esté fuera del rango permitido.
    while not valor.isdigit() or not (minimo <= int(valor) <= maximo):
        valor = input(f"Inválido. {etiqueta} debe ser un número entre {minimo} y {maximo}: ").strip()
    return int(valor)


def _pedir_float(etiqueta):
    """
    Pide un número decimal positivo (acepta coma o punto).

    Reemplaza la coma por punto para aceptar ambas notaciones y repite la
    solicitud hasta que se ingrese un número convertible a float mayor a 0.

    Args:
        etiqueta (str): Nombre del campo a pedir (ej. "Precio (u$d)").

    Returns:
        float: Valor decimal positivo ingresado por el usuario.
    """
    valor = input(f"{etiqueta}: ").strip().replace(",", ".")
    while True:
        try:
            numero = float(valor)
            # Solo se acepta si el número es positivo.
            if numero > 0:
                return numero
        except ValueError:
            # Si no se puede convertir a float, se vuelve a pedir el valor.
            pass
        valor = input(f"Inválido. {etiqueta} debe ser un número positivo: ").strip().replace(",", ".")


def _pedir_patente_existente(autos : dict) -> str:
    """
    Pide una patente y valida que ya exista en el catálogo.

    Convierte la patente a mayúsculas para mantener coherencia con el formato
    usado en el JSON y repite la solicitud hasta que exista.

    Args:
        autos (dict): Diccionario con el catálogo cargado.

    Returns:
        str: Patente existente, en mayúsculas.
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
    Muestra por pantalla la información completa de un auto.

    Imprime la ficha del auto (patente, marca, modelo, calidad, año, precio y
    categoría) con un formato legible.

    Args:
        patente (str): Patente del auto (clave del diccionario).
        datos (dict): Diccionario con los atributos del auto.
    """
    # TODO(TP - Req 1): proteger el acceso a claves con try/except (KeyError)
    # por si al auto le falta algún atributo en el JSON.
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
    Muestra todo el catálogo de autos (lectura general / Read).

    Carga el archivo JSON y, si hay autos, los lista uno por uno usando
    `_mostrar_auto()`. Si el catálogo está vacío, lo informa.
    """
    autos = _cargar_autos()
    # Si el diccionario está vacío, no hay nada para mostrar.
    if not autos:
        print("\nNo hay autos en el catálogo.")
        try: input("[Enter] ")
        except: pass
        return
    print("\n--- CATÁLOGO DE AUTOS ---")
    # Recorre cada par (patente, datos) del diccionario de diccionarios.
    # TODO(TP - Req 5): aquí se podría aplicar una lista por comprensión
    # o una lambda para generar un resumen del catálogo.
    for patente, datos in autos.items():
        _mostrar_auto(patente, datos)
        try: 
            res = input(" ")
            if res == "q":
                return
        except: pass


def ver_auto():
    """
    Muestra un auto según su patente (lectura individual / Read).

    Pide una patente existente y muestra únicamente la ficha de ese auto.
    Si el catálogo está vacío, lo informa.
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
    Al finalizar, guarda la última versión del diccionario en el archivo JSON.
    (Req 2 del TP: Create sobreescribe el archivo).
    """
    # TODO(TP - Req 1): manejar excepciones en la carga y en el guardado.
    autos = _cargar_autos()

    # Se pide la patente y se valida que no exista (una patente es única).
    patente = input("Patente del nuevo auto: ").strip().upper()
    while patente in autos:
        patente = input("Esa patente ya existe. Ingrese otra: ").strip().upper()

    # Se piden y validan los demás atributos del auto.
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
    Modifica uno o más campos de un auto existente (Update).

    Pide una patente válida, muestra los valores actuales y permite cambiar el
    campo elegido. Después de cada cambio se guarda automáticamente en el JSON.
    (Req 2 del TP: Update sobreescribe el archivo).

    El bucle se repite hasta que el usuario elige la opción [0] salir.
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
        # Muestra el menú de campos con su valor actual.
        print(f"\n--- Modificar auto [{patente}] ---")
        for clave, (campo, nombre) in CAMPOS.items():
            print(f"[{clave}] {nombre}: {autos[patente][campo]}")
        print("[0] Terminar")

        opcion = input("\n¿Qué campo desea modificar?: ").strip()

        # Opción para salir del menú de modificación.
        if opcion == "0":
            break
        # Validación de la opción ingresada.
        elif opcion not in CAMPOS:
            print("\nOpción no válida. Intente de nuevo.")
            continue

        # Se traduce la opción a (campo del JSON, nombre visible).
        campo, nombre = CAMPOS[opcion]

        # Se pide el nuevo valor según el tipo de campo elegido.
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
    Elimina un auto del catálogo según su patente (Delete).

    Pide una patente existente, borra el registro del diccionario y sobreescribe
    el archivo JSON con la última versión.
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


# ---------- Menú ----------

def menu_crud():
    """
    Muestra y gestiona el menú principal del CRUD de autos.

    Ofrece ver el catálogo, ver un auto, agregar, modificar, eliminar o salir.
    Redirige a la función correspondiente según la opción elegida y se mantiene
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

        # Despacho de la opción elegida hacia la función correspondiente.
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
            # Salir del menú CRUD.
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")


if __name__ == "__main__":
    # Punto de entrada: ejecuta el menú CRUD si se corre este archivo directamente.
    # TODO(TP - Req 3): verificar que autos.json contenga al menos 5 registros (precarga).
    menu_crud()
