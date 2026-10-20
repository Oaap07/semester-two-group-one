"""
(TPO - SPRINT) - Programacion I
Facultad de Ingenieria Informatica

Modulo: crud.py - Gestion CRUD del catalogo de autos.
Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).

"""
import json, os
import informe as inf
import pandas as pd


# ==========================================
# CONFIGURACION Y CONSTANTES
# ==========================================

# Ruta del archivo JSON donde se guarda el catalogo de autos.
RUTA_AUTOS = inf.RUTA_AUTOS_JSON
RUTA_USUARIOS = inf.RUTA_USUARIOS_JSON
# Tuplas con los valores permitidos para cada campo.
CALIDAD = inf.CALIDADES
MARCA = inf.MARCAS
CATEGORIA = inf.CATEGORIAS
ESTADO = inf.DISPONIBLE
# Mapeo entre la opcion numerica del menu y la categoria interna de autos.json.
categ_preset = {
    "1": "sedan_hatchback",
    "2": "suv_crossover",
    "3": "pickup",
    "4": "monovolumen_mpv"
}


def limpiar():
    """
    Limpia la consola segun el sistema operativo.

    En Windows usa 'cls'; en Linux/macOS usa 'clear'. Sirve para mantener la
    interfaz ordenada entre pantallas del menu.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# ---------- Utilidades de entrada ----------

def _entrada(mensaje: str = "") -> str | None:
    """
    Lee una linea por teclado manejando el fin de entrada (EOFError).

    Centraliza la lectura de datos para no repetir un try/except en cada prompt
    y evita que un cierre de la entrada (Ctrl+Z en Windows, Ctrl+D en Linux)
    corte el programa o deje variables sin definir.

    Args:
        mensaje (str): Texto del prompt que se muestra al usuario.

    Returns:
        str | None: El texto ingresado, recortado con strip(); o None si no hay
        mas entrada (EOFError), para que quien llama pueda salir ordenadamente.
    """
    try:
        return input(mensaje).strip()
    except EOFError:
        return None


# ---------- Persistencia ----------

def _cargar_autos() -> dict:
    """
    Carga el catalogo de autos desde el archivo JSON.

    Lee el contenido de `autos.json` y lo convierte a un diccionario de Python,
    donde cada clave es la patente del auto y cada valor es otro diccionario con
    sus atributos (diccionario de diccionarios).

    Returns:
        dict: Estructura {patente: {marca, modelo, calidad, ano, precio, categoria}, ...}.
        Devuelve {} si el archivo no existe, no es JSON valido, no es un
        diccionario o hay un error de sistema; nunca devuelve None.

    Nota:
        No propaga excepciones: FileNotFoundError, json.JSONDecodeError y OSError
        se manejan internamente y se informan por pantalla.
    """
    # devuelven un diccionario vacio y OSError informa el error de sistema. Siempre retorna un dict.
    try:
        with open(RUTA_AUTOS, "r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)
        # Validacion: el JSON debe ser un diccionario (patente -> atributos).
        if not isinstance(contenido, dict):
            print("/// El archivo de autos no tiene la estructura esperada (dict). ///")
            return {}
        return contenido
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        limpiar()
        print("/// El archivo de autos no tiene un formato JSON válido. ///")
        _entrada("[Enter] ")
        return {}
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        _entrada("[Enter] ")
        return {}

def _guardar_autos(autos):
    """
    Escribe el catalogo de autos en el archivo JSON.

    Sobreescribe `autos.json` con la ultima version del diccionario recibido,
    manteniendo un formato legible (indentado) y conservando los acentos.

    Args:
        autos (dict): Diccionario con el catalogo a guardar.

    Returns:
        bool: True si se guardo correctamente; False si 'autos' no es un
        diccionario, no es serializable a JSON o hay un error de escritura.

    Nota:
        No propaga excepciones: valida el tipo y captura los errores de tipo,
        valor y E/S.
    """
    # Validacion: solo se guarda un diccionario.
    if not isinstance(autos, dict):
        print("/// No se pudo guardar: 'autos' debe ser un diccionario. ///")
        return False
    try:
        with open(RUTA_AUTOS, "w", encoding="utf-8") as archivo:
            json.dump(autos, archivo, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        print(f"/// ¡El archivo {RUTA_AUTOS} no existe! ///")
        return False
    except (TypeError, ValueError) as e:
        # Algun valor del catalogo no es serializable a JSON.
        print(f"/// No se pudo guardar el catalogo: {e} ///")
        return False
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        _entrada("[Enter] ")
        return False
    return True

# ---------- Validaciones de entrada ----------

def _pedir_de_tupla(etiqueta, opciones):
    """
    Pide un valor que obligatoriamente debe estar dentro de 'opciones'.

    Repite la solicitud hasta que el usuario ingrese una opcion valida. Se usa
    para campos con valores predefinidos (marca, calidad, categoria, estado).

    Args:
        etiqueta (str): Nombre del campo a pedir (ej. "Marca").
        opciones (tuple): Tupla con los valores validos aceptados (todos str).

    Returns:
        str | bool | None: Valor validado (bool si es 'estado'); o None si se
        corto la entrada (EOFError) o las opciones no estan bien configuradas.
    """
    # Validacion: 'opciones' debe ser una coleccion no vacia de textos.
    if not opciones or not all(isinstance(o, str) for o in opciones):
        print(f"/// El campo {etiqueta} no tiene opciones validas configuradas. ///")
        return None
    print(f"{etiqueta} (opciones: {', '.join(opciones)}): ")
    while True:
        # Bucle de validacion: no se sale hasta que el valor pertenezca a 'opciones'.
        valor = _entrada()
        if valor is None:
            return None
        valor = valor.lower()
        if valor in opciones:
            break
        print(f"Valor inválido. {etiqueta} debe ser una de: {', '.join(opciones)}")
    # El campo 'estado' se guarda como booleano en el JSON.
    if valor == "true":
        return True
    if valor == "false":
        return False
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
        int | None: Numero entero valido ingresado; o None si el rango esta mal
        formado o se corto la entrada (EOFError).
    """
    # Validacion: el rango debe estar bien formado (enteros con minimo <= maximo).
    if not isinstance(minimo, int) or not isinstance(maximo, int) or minimo > maximo:
        print(f"/// Rango inválido para {etiqueta}: {minimo}-{maximo}. ///")
        return None
    while True:
        valor = _entrada(f"{etiqueta} ({minimo}-{maximo}): ")
        if valor is None:
            return None
        # Se repite hasta que el valor se pueda convertir a un entero dentro del rango permitido.
        try:
            numero = int(valor)
        except ValueError:
            numero = None
        if numero is not None and minimo <= numero <= maximo:
            return numero
        print(f"Inválido. {etiqueta} debe ser un número entre {minimo} y {maximo}.")

def _pedir_float(etiqueta):
    """
    Pide un numero decimal positivo (acepta coma o punto).

    Reemplaza la coma por punto para aceptar ambas notaciones y repite la
    solicitud hasta que se ingrese un numero convertible a float mayor a 0.

    Args:
        etiqueta (str): Nombre del campo a pedir (ej. "Precio (u$d)").

    Returns:
        float | None: Valor decimal positivo ingresado; o None si se corto la
        entrada (EOFError).
    """
    while True:
        valor = _entrada(f"{etiqueta}: ")
        if valor is None:
            return None
        try:
            # Solo se acepta si el numero es convertible a float y es positivo.
            numero = float(valor.replace(",", "."))
        except ValueError:
            numero = None
        if numero is not None and numero > 0:
            return numero
        print(f"Inválido. {etiqueta} debe ser un número positivo.")

def _pedir_patente_existente(autos : dict) -> str | None:
    """
    Pide una patente y valida que ya exista en el catalogo.

    Convierte la patente a mayusculas para mantener coherencia con el formato
    usado en el JSON y repite la solicitud hasta que exista.

    Args:
        autos (dict): Diccionario con el catalogo cargado.

    Returns:
        str | None: Patente existente en mayusculas; o None si el catalogo no es
        valido, esta vacio, el usuario cancela ("0") o se corta la entrada.
    """
    # Validacion: el catalogo debe ser un diccionario con datos.
    if not isinstance(autos, dict):
        print("\nEl catalogo recibido no es valido.")
        _entrada("[Enter] ")
        return None
    if not autos:
        print("\nNo hay autos en el catálogo.")
        _entrada("[Enter] ")
        return None

    while True:
        patente = _entrada("Ingrese la patente del auto (0 para cancelar): ")
        if patente is None:
            return None
        patente = patente.upper()
        # El usuario cancelo: se devuelve None
        if patente == "0":
            return None
        if patente in autos:
            return patente
        print("Patente no encontrada. Ingrese una patente válida (0 para cancelar): ")

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
    # auto le falta algun dato en el JSON.
    print(f"\n[{patente}]")
    try:
        print(f"\tMarca: {datos['marca'].capitalize()}")
        print(f"\tModelo: {datos['modelo'].capitalize()}")
        print(f"\tCalidad: {datos['calidad']}")
        print(f"\tAño: {datos['año']}")
        print(f"\tPrecio: u$d {datos['precio']:.1f}")
        print(f"\tCategoría: {datos['categoria']}")
        print(f"\tEstado: {datos['estado']}")
    except KeyError as e:
        print(f"\t[Falta un dato del auto: {e}]")

# ---------- READ ----------

def ver_stock(base,rentados):
    """
    Muestra autos del catalogo como una tabla (lectura general / Read).

    Carga el catalogo con `_cargar_autos()` y lo muestra como tabla usando
    pandas (DataFrame). `base` y `rentados` funcionan como un "modo":

        ver_stock(1, 0): muestra TODO el catalogo (estado legible y precio con "$").
        ver_stock(0, 1): muestra SOLO los autos rentados (los no disponibles).
        ver_stock(1, 1): muestra SOLO los autos disponibles.

    Args:
        base (int): 1 para el catalogo completo; 0 para el listado de rentados.
        rentados (int): 1 para armar un listado filtrado; 0 para el catalogo.

    Es el "motor" de los informes de menu.py (`ver_catalogo`,
    `informe_disponibilidad` y `estado_rentas`). Se apoya en pandas (DataFrame)
    para armar reportes matriciales.

    Returns:
        None
    """

    # se validan los argumentos al comienzo y se sale con un aviso.
    if (base, rentados) not in ((1, 0), (0, 1), (1, 1)):
        print("\nModo de informe inválido. Use (base, rentados) = (1,0), (0,1) o (1,1).")
        _entrada("[Enter] ")
        return

    limpiar()
    autos : dict = _cargar_autos()

    # --- MODO 1: catalogo completo (base=1, rentados=0) ---
    if base == 1 and rentados == 0:
        # Recorre el catalogo preparando los campos para mostrarlos en la tabla.
        for i in autos:
            autos[i]["estado"] = "disponible" if autos[i]["estado"] == True else "ocupado"
            # Antepone "$" al precio para mostrarlo como importe.
            autos[i]["precio"] = "$" + str(autos[i]["precio"])
    # --- MODO 2: solo autos rentados (base=0, rentados=1) ---
    elif base == 0 and rentados == 1:
        # Diccionario auxiliar con SOLO los autos que NO estan disponibles.
        autos_rentados = {}
        # Recorre todo el catalogo, pero solo procesa los autos rentados.
        for i in autos:
            # Copia el auto para no modificar el original del catalogo.
            auto_visual = autos[i].copy()
            # Usa .get(): si el estado es True (disponible), lo saltea.
            if autos[i].get("estado") == True:
                continue 
            
            auto_visual["estado"] = "ocupado"
            auto_visual["precio"] = "$" + str(auto_visual["precio"])
            autos_rentados[i] = auto_visual
    elif base == 1 and rentados == 1:
            # Diccionario auxiliar con SOLO los autos que NO estan disponibles.
            autos_disponibles = {}
            # Recorre todo el catalogo, pero solo procesa los autos rentados.
            
            for i in autos:
                # Copia el auto para no modificar el original del catalogo.
                auto_visual = autos[i].copy()
                # Usa .get(): si el estado es True (disponible), lo saltea.
                if autos[i].get("estado") == False:
                    continue
        
                # --- DISPONIBLES ---
                # Formatea los campos solo para los autos que si se van a mostrar.
                auto_visual["estado"] = "disponible"
                auto_visual["precio"] = "$" + str(auto_visual["precio"])
                autos_disponibles[i] = auto_visual
    # AHORA se elige el diccionario del modo y se controla ESE.
    if base == 1 and rentados == 0:
        autos_a_mostrar = autos
        aviso_vacio = "\nNo hay autos en el catálogo."
    elif base == 1 and rentados == 1:
        autos_a_mostrar = autos_disponibles
        aviso_vacio = "\nNo hay autos disponibles en el catálogo."
    else:
        autos_a_mostrar = autos_rentados
        aviso_vacio = "\nNo hay autos rentados en el catálogo."
    if not autos_a_mostrar:
        print(aviso_vacio)
        _entrada("[Enter] ")
        return
    # Arma un DataFrame de pandas sobre el diccionario del modo elegido. Las
    # patentes quedan como columnas y los atributos como filas; el .T deja una
    # fila por auto.
    try:
        autos_excel_modificado = pd.DataFrame(autos_a_mostrar)
    except (TypeError, ValueError) as e:
        print(f"\nNo se pudo generar la tabla: {e}")
        _entrada("[Enter] ")
        return
    print("\n")
    print("--"*15,"CATALOGO DE AUTOS","--"*15)
    print(autos_excel_modificado.T)
    print("--"*39)
    
    _entrada("Presione cualquier tecla para salir: ")

def ver_auto():
    """
    Muestra un auto segun su patente (lectura individual / Read).

    Pide una patente existente y muestra unicamente la ficha de ese auto.
    Si el catalogo esta vacio, lo informa.

    Returns:
        None
    """
    autos = _cargar_autos()
    if not autos:
        print("\nNo hay autos en el catálogo.")
        _entrada(" ")
        return
    patente = _pedir_patente_existente(autos)
    # cancelo (None) se sale sin lanzar KeyError.
    if patente is None:
        return
    _mostrar_auto(patente, autos[patente])
    _entrada("\n Presiona ENTER para volver")

def open_autos():
    """
    Lee y devuelve el catalogo de autos desde el archivo JSON.

    Funcion de persistencia nueva, usada por el menu (submenu_usuario) para
    tener el catalogo cargado en memoria.

    Returns:
        dict: Catalogo {patente: {atributos}}. Devuelve {} si el archivo no
        existe, no es JSON valido, no es un diccionario o hay un error de
        sistema; nunca devuelve None.
    """
    try:
        with open(inf.RUTA_AUTOS_JSON, 'r', encoding="utf-8") as archivo:
            lista_aut = json.load(archivo)
        if not isinstance(lista_aut, dict):
            return {}
        return lista_aut
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        limpiar()
        print("/// El archivo de autos no tiene un formato JSON válido. ///")
        _entrada("[Enter] ")
        return {}
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        _entrada("[Enter] ")
        return {}

def open_usuarios():
    """
    Lee y devuelve los usuarios desde el archivo JSON.

    Returns:
        dict: Usuarios {dni: {nombre, clave, autos_rentados}}. Devuelve {} si el
        archivo no existe, no es JSON valido, no es un diccionario o hay un
        error de sistema; nunca devuelve None.
    """
    try:
        with open(inf.RUTA_USUARIOS_JSON, 'r', encoding="utf-8") as archivo:
            lista_usu = json.load(archivo)
        if not isinstance(lista_usu, dict):
            return {}
        return lista_usu
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        limpiar()
        print("/// El archivo de usuarios no tiene un formato JSON válido. ///")
        _entrada("[Enter] ")
        return {}
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        _entrada("[Enter] ")
        return {}

def escribir_usuario(lista_usu):
    """
    Sobreescribe el archivo de usuarios con el diccionario recibido.

    Args:
        lista_usu (dict): Diccionario completo de usuarios a guardar.

    Returns:
        bool: True si se guardo correctamente; False si el dato no es un
        diccionario, no es serializable a JSON o hay un error de escritura.
    """
    # Validacion: solo se guarda un diccionario.
    if not isinstance(lista_usu, dict):
        print("/// No se pudo guardar: 'lista_usu' debe ser un diccionario. ///")
        return False
    try:
        with open(inf.RUTA_USUARIOS_JSON, 'w', encoding="utf-8") as archivo:
            json.dump(lista_usu, archivo, indent=4, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        print(f"/// No se pudo guardar el archivo de usuarios: {e} ///")
        return False
    except OSError as e:
        print(f"/// No se pudo escribir el archivo de usuarios: {e} ///")
        return False
    return True

def escribir_auto(lista_aut):
    """
    Sobreescribe el archivo del catalogo de autos con el diccionario recibido.

    Args:
        lista_aut (dict): Diccionario completo de autos a guardar.

    Returns:
        bool: True si se guardo correctamente; False si el dato no es un
        diccionario, no es serializable a JSON o hay un error de escritura.
    """
    # Validacion: solo se guarda un diccionario.
    if not isinstance(lista_aut, dict):
        print("/// No se pudo guardar: 'lista_aut' debe ser un diccionario. ///")
        return False
    try:
        with open(inf.RUTA_AUTOS_JSON, 'w', encoding="utf-8") as archivo:
            json.dump(lista_aut, archivo, indent=4, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        print(f"/// No se pudo guardar el archivo de autos: {e} ///")
        return False
    except OSError as e:
        print(f"/// No se pudo escribir el archivo de autos: {e} ///")
        return False
    return True

# ---------- CREATE ----------

def agregar_auto():
    """
    Da de alta un auto nuevo (Create).

    Pide todos los datos del auto y valida que la patente no exista previamente.
    Al finalizar, guarda la ultima version del diccionario en el archivo JSON.
    """
    autos = _cargar_autos()

    # Se pide la patente y se valida que no exista (una patente es unica).
    anio = _pedir_entero("Año: ", 2000, 2026)
    # Si se corto la entrada al pedir el año, se aborta el alta sin guardar.
    if anio is None:
        return
    while True:
        try:
            if anio <= 2016:
                print('Seleccione una patente ANTIGUA (ej: AAA123) ')
            else:
                print('Seleccione una patente MERCOSUR (ej: AA123AA) ')
            patente = input('Patente del nuevo auto : ').strip().upper()
        except EOFError:
            return
        largo = len(patente)
        valida = False
        
        if largo == 6 and anio <= 2016:
            # Formato viejo: 3 letras (primeras) y 3 numeros (ultimos)
            parte_letras = patente[0:3]
            parte_numeros = patente[3:6]
            if parte_letras.isalpha()and parte_numeros.isdigit():
                valida = True
        elif largo == 7 and anio > 2016:
            letras1 = patente[0:2]
            numeros = patente[2:5]
            letras2 = patente[5:7]
            if letras1.isalpha() and numeros.isdigit() and letras2.isalpha():
                valida = True
        if not valida:
            print('PATENTE INCORRECTA: Formato invalido. Usa 3 letras y 3 numeros (ej: ABC123) o 2 letras, 3 numeros y 2 letras (ej: AA123AA) ')
            continue
        if patente in autos:
            print('Esa patente ya existe. Ingrese otra ')
            continue
        break

    # Se piden y validan los demas atributos del auto.
    marca = _pedir_de_tupla("Marca: ", MARCA)
    modelo = _pedir_de_tupla("Modelo: ", inf.AUTOS[marca])
    while modelo not in inf.AUTOS[marca]:
        print('Modelo no existente dentro de los disponibles ')
        modelo = input(f"Modelo: ").strip().lower()
    calidad = _pedir_de_tupla("Calidad:", CALIDAD)
    precio = _pedir_float("Precio (u$d): ")
    categoria = _pedir_de_tupla("Categoría: ", CATEGORIA)
    

    # Se crea el registro usando la patente como clave del diccionario.
    autos[patente] = {
        "marca": marca,
        "modelo": modelo,
        "calidad": calidad,
        "año": anio,
        "precio": precio,
        "categoria": categoria,
        "estado": True
    }
    # Se persiste el cambio y se confirma al usuario.
    _guardar_autos(autos)
    print(f"\nAuto {patente} agregado correctamente.")

# ---------- UPDATE ----------

def modificar_estado_auto(patente, estado_auto):
    """
    Invierte el estado de un auto (disponible <-> ocupado) en autos.json.

    Args:
        patente (str): Patente del auto a modificar.
        estado_auto (bool): Estado actual del auto (True = disponible,
            False = no disponible). La funcion guarda el estado invertido.

    Returns:
        bool: True si el cambio se guardo; False si el estado no es booleano, la
        patente no existe o hay un error de escritura.

    Nota:
        No propaga excepciones: valida los datos y los errores de E/S se
        informan por pantalla.
    """
    # Validacion: el estado debe ser booleano.
    if not isinstance(estado_auto, bool):
        print("\nEstado inválido: se esperaba True (disponible) o False (ocupado).")
        return False

    autos = _cargar_autos()
    # Validacion: debe ser un catalogo con la patente pedida (evita KeyError).
    if not isinstance(autos, dict) or patente not in autos:
        print(f"\nNo existe un auto con la patente {patente}.")
        return False

    # Invierte el estado actual y persiste el cambio (ruta constante RUTA_AUTOS).
    autos[patente]["estado"] = not estado_auto
    try:
        with open(RUTA_AUTOS, "w", encoding="utf-8") as archivo:
            json.dump(autos, archivo, indent=4, ensure_ascii=False)
    except OSError as e:
        print(f"/// No se pudo escribir el archivo de autos: {e} ///")
        return False
    return True

def modificar_auto():
    """
    Modifica uno o mas campos de un auto existente (Update).

    Pide una patente valida, muestra los valores actuales y permite cambiar el
    campo elegido. Despues de cada cambio se guarda automaticamente en el JSON.

    El bucle se repite hasta que el usuario elige la opcion [0] salir.
    """
    autos = _cargar_autos()
    if not autos:
        print("\nNo hay autos en el catálogo.")
        _entrada("[Enter] ")
        return

    # _pedir_patente_existente devuelve None si el usuario cancela ("0").
    patente = _pedir_patente_existente(autos)
    if patente is None:
        return

    while True:
        # Muestra el menu de campos con su valor actual.
        print(f"\n--- Modificar auto [{patente}] ---")
        
        for i, j in enumerate(autos[patente]):
            print(f"[{i+1}] {j.capitalize()}: {autos[patente][j]}")
        print("--------------------")
        print("[0] Terminar")

        opcion = _entrada("\n¿Qué campo desea modificar?: ")
        if opcion is None:
            return

        # Opcion para salir del menu de modificacion.
        if opcion == "0":
            break
        # Validacion de la opcion: debe ser un numero entero dentro del rango mostrado.
        try:
            indice = int(opcion)
        except ValueError:
            print("\nOpción no válida. Intente de nuevo.")
            continue
        if indice < 1 or indice > len(autos[patente]):
            print("\nOpción no válida. Intente de nuevo.")
            continue

        # Se pide el nuevo valor segun el tipo de campo elegido.
        campo = None
        nuevo = None
        if opcion == "1":
            campo = "marca"
            nuevo = _pedir_de_tupla("Marca", MARCA)
        elif opcion == "2":
            campo = "modelo"
            texto = _entrada("Nuevo modelo: ")
            nuevo = None if texto is None else texto.lower()
        elif opcion == "3":
            campo = "calidad"
            nuevo = _pedir_de_tupla("Calidad", CALIDAD)
        elif opcion == "4":
            campo = "año"
            nuevo = _pedir_entero("Año", 2000, 2026)
        elif opcion == "5":
            campo = "precio"
            nuevo = _pedir_float("Nuevo precio (u$d)")
        elif opcion == "6":
            campo = "categoria"
            nuevo = _pedir_de_tupla("Categoría", CATEGORIA)
        elif opcion == "7":
            campo = "estado"
            nuevo = _pedir_de_tupla("estado", ESTADO)

        # Validacion: si la entrada se corto (None) o no hay campo mapeado, no se guarda.
        if campo is None or nuevo is None:
            return
        autos[patente][campo] = nuevo

        # Se guarda el cambio y se confirma.
        _guardar_autos(autos)
        print(f"\n{patente} actualizado correctamente.")

# ---------- DELETE ----------

def eliminar_auto():
    """
    Elimina un auto del catalogo segun su patente (Delete).

    Pide una patente existente, borra el registro del diccionario y sobreescribe
    el archivo JSON con la ultima version.
    """
    autos = _cargar_autos()
    if not autos:
        print("\nNo hay autos en el catálogo.")
        _entrada("[Enter] ")
        return
    # se valida el resultado de la busqueda: si el usuario cancela (None) se
    # sale sin borrar nada.
    patente = _pedir_patente_existente(autos)
    if patente is None:
        return
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
        opcion = _entrada("Seleccione una opción: ")
        if opcion is None:
            break

        # Despacho de la opcion elegida hacia la funcion correspondiente.
        if opcion == "1":
            # ver_stock(base=1, rentados=0): muestra el catalogo completo.
            ver_stock(1,0)
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
    limpiar()
    menu_crud()
    limpiar()
