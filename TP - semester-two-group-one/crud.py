"""
Requisitos del Trabajo Practico (TPO - SPRINT) - Programacion I
Facultad de Ingenieria Informatica

Modulo: crud.py - Gestion CRUD del catalogo de autos.
Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).

--------------------------------------------------------------------------------
Objetivo del trabajo
--------------------------------------------------------------------------------
Aplicar los conocimientos vistos en clase sobre archivos/JSON y manejo de
excepciones, ademas de los requisitos minimos del programa.
"""
# ------------------------------------------------------------------
# CUMPLIMIENTO DEL SPRINT - requisitos que aporta ESTE modulo:
#   Req 1 (excepciones especificas) ....... PARCIAL (sobran except genericos)
#   Req 2 (persistencia en JSON) .......... CUMPLIDO (autos.json / usuarios.json)
#   Req 4 (tuplas en la logica) ........... CUMPLIDO (CALIDAD, MARCA, CATEGORIA, ESTADO)
#   Req 6 (diccionario de diccionarios) .... CUMPLIDO (7 atributos por auto)
#   Req 7 (menu con CRUD completo) ........ CUMPLIDO (Create / Read / Update / Delete)
#   Req 8 (reporte matricial) ............. CUMPLIDO (ver_stock con pandas)
# Los trabajos pendientes estan marcados en el codigo como "TODO(TP - Req N)" y las mejoras sugeridas como
# "RECOMENDACION (Req N)".
# ------------------------------------------------------------------

import json, os
import informe as inf
import pandas as pd
import matplotlib as mt

# ==========================================
# CONFIGURACION Y CONSTANTES
# ==========================================

# Ruta del archivo JSON donde se guarda el catalogo de autos.
# (Req 2 y 3 del TP: persistencia y precarga desde archivo).
RUTA_AUTOS = inf.RUTA_AUTOS_JSON
RUTA_USUARIOS = inf.RUTA_USUARIOS_JSON
# Tuplas con los valores permitidos para cada campo.
# (Req 4 del TP: uso de tuplas como parte de la logica / validaciones).
CALIDAD = inf.CALIDADES
MARCA = inf.MARCAS
CATEGORIA = inf.CATEGORIAS
ESTADO = inf.DISPONIBLE
categ_preset = {
    "1": "sedan_hatchback",
    "2": "suv_crossover",
    "3": "pickup",
    "4": "monovolumen_mpv"
}

# Mapeo entre la opcion numerica del menu de modificacion y el campo del JSON.
# Formato: "clave de menu": ("nombre del campo en el JSON", "nombre para mostrar").
# Se usa para no repetir la lista de campos editables en varios lugares.
# NOTA (comentario huerfano): describe un diccionario de mapeo que ya no existe
# en el codigo; `modificar_auto` arma las opciones en forma dinamica segun las
# claves del auto elegido.

def limpiar():
    """
    Limpia la consola segun el sistema operativo.

    En Windows usa 'cls'; en Linux/macOS usa 'clear'. Sirve para mantener la
    interfaz ordenada entre pantallas del menu.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# ---------- Persistencia ----------

def _cargar_autos() -> dict:
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
    # RESUELTO (Req 1): la lectura se maneja con excepciones especificas; FileNotFoundError y json.JSONDecodeError
    # devuelven un diccionario vacio y OSError informa el error de sistema. Siempre retorna un dict.
    try:
        with open(RUTA_AUTOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        limpiar()
        print("/// El archivo de autos no tiene un formato JSON válido. ///")
        input("[Enter] ")
        return {}
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        input("[Enter] ")
        return {}

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
    # RESUELTO (Req 1): el guardado se envuelve en try/except (OSError) y se valida que 'autos' sea un diccionario
    # antes de escribir; un tipo inesperado avisa y no corta el programa.
    if not isinstance(autos, dict):
        print("/// No se pudo guardar: 'autos' debe ser un diccionario. ///")
        return
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
        str | bool: Valor elegido por el usuario, validado (bool si es 'estado').
    """
    print(f"{etiqueta} (opciones: {', '.join(opciones)}): ")
    
    valor = input().strip().lower()
    # Bucle de validacion: no se sale hasta que el valor pertenezca a 'opciones'.
    while valor not in opciones:
        print(f"Valor inválido. {etiqueta} debe ser una de: {', '.join(opciones)}")
        valor = input().strip().lower()
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
        int: Numero entero valido ingresado por el usuario.
    """
    # RESUELTO (Req 1): la conversion se hace con try/except ValueError en lugar de depender solo de .isdigit().
    valor = input(f"{etiqueta} ({minimo}-{maximo}): ").strip()
    # Se repite hasta que el valor se pueda convertir a un entero dentro del rango permitido.
    while True:
        try:
            numero = int(valor)
        except ValueError:
            numero = None
        if numero is not None and minimo <= numero <= maximo:
            return numero
        valor = input(f"Inválido. {etiqueta} debe ser un número entre {minimo} y {maximo}: ").strip()

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
    # RESUELTO (Req 1): se valida que 'autos' sea un diccionario y se reemplazaron los 'except: pass' por 'except
    # EOFError', de modo que 'patente' quede siempre definida (antes un ingreso fallido daba NameError).
    if not isinstance(autos, dict):
        print("\nEl catalogo recibido no es valido.")
        try: input("[Enter] ")
        except EOFError: pass
        return None
    if not autos:
        print("\nNo hay autos en el catálogo.")
        try: input("[Enter] ")
        except EOFError: pass
        return None

    try:
        patente = input("Ingrese la patente del auto: ").strip().upper()
    except EOFError:
        return None
    if patente == '0':
        return patente

    while patente not in autos:
        try:
            patente = input("Patente no encontrada. Ingrese una patente válida: ").strip().upper()
        except EOFError:
            return None
        if patente == '0':
            break
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
    # RESUELTO (Req 1): el acceso a los atributos se protege con try/except KeyError, asi la ficha no se corta si al
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

    Args:
        base (int): 1 para el catalogo completo; 0 para el listado de rentados.
        rentados (int): 1 para armar el listado de rentados; 0 para el catalogo.

    NOTA (funcion nueva / modificada): reemplaza a la antigua `ver_autos()` y
    ahora es el "motor" de los informes de menu.py (`informe_disponibilidad` y
    `estado_rentas`). Se apoya en pandas (DataFrame), que la documentacion
    tecnica recomienda para armar reportes matriciales (Req 8 del TP).

    Returns:
        None
    """
    limpiar()
    autos : dict = _cargar_autos()

    # --- MODO 1: catalogo completo (base=1, rentados=0) ---
    if base == 1 and rentados == 0:
        # Recorre el catalogo preparando los campos para mostrarlos en la tabla.
        for i in autos:
            # NOTA (posible error): si un auto no tiene la clave "estado" (por
            # ejemplo, uno dado de alta con `agregar_auto`), esto lanza KeyError.
            # Traduce el estado booleano a un texto legible para el usuario.
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
    # BUG (UnboundLocalError): con otra combinacion (por ejemplo, ver_stock(0, 0)) no entra en ningun modo y
    # "autos_rentados" queda sin definir -> UnboundLocalError (subclase de NameError) en la linea del DataFrame de
    # abajo.
    # Arma un DataFrame de pandas: si base == 1 usa el catalogo completo; si no,
    # usa el diccionario de rentados. Las patentes quedan como columnas y los
    # atributos como filas; el .T deja una fila por auto.
    autos_excel_modificado = pd.DataFrame(autos if base == 1 and rentados == 0 else (autos_disponibles if base == 1 and rentados == 1 else autos_rentados))

    # BUG (logica): en el modo rentados se controla "autos" (no "autos_rentados"), asi que si no hay autos rentados se
    # muestra una tabla vacia en vez del aviso.
    # RECOMENDACION (Req 8): controlar "autos_rentados" para que el informe de rentados avise correctamente cuando no
    # hay unidades alquiladas.
    if not autos:
        print("\nNo hay autos en el catálogo.")
        try: input("[Enter] ")
        except: pass
        return
    print("\n")
    print("--"*15,"CATALOGO DE AUTOS","--"*15)
    print(autos_excel_modificado.T)
    print("--"*39)
    
    try: 
        input("Presione cualquier tecla para salir: ")
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
    # BUG (KeyError): si el usuario escribe "0" (o la funcion devuelve None), 'autos[patente]' no existe y lanza
    # KeyError (sin try/except).
    _mostrar_auto(patente, autos[patente])
    try: 
        input("\n Presiona ENTER para volver")
    except:
        pass

def open_autos():
    """
    Lee y devuelve el catalogo de autos desde el archivo JSON.

    Funcion de persistencia nueva, usada por el menu (submenu_usuario) para
    tener el catalogo cargado en memoria.

    Returns:
        dict: Catalogo {patente: {atributos}}; o None si ocurre un error de sistema.
    """
    # RESUELTO (Req 1): se capturan FileNotFoundError, json.JSONDecodeError y OSError, y SIEMPRE se retorna un
    # diccionario ({} en caso de error) en vez de None, para que quien lo use no reciba un TypeError.
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
        try: input("[Enter] ")
        except: pass
        return {}
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        try: input("[Enter] ")
        except: pass
        return {}

def open_usuarios():
    """
    Lee y devuelve los usuarios desde el archivo JSON.

    Returns:
        dict: Usuarios {dni: {nombre, clave, autos_rentados}}; o None si ocurre
        un error de sistema.
    """
    # RESUELTO (Req 1): se capturan FileNotFoundError, json.JSONDecodeError y OSError, y SIEMPRE se retorna un
    # diccionario ({} en caso de error) en vez de None, para que quien lo use no reciba un TypeError.
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
        try: input("[Enter] ")
        except: pass
        return {}
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        try: input("[Enter] ")
        except: pass
        return {}

def escribir_usuario(lista_usu):
    """
    Sobreescribe el archivo de usuarios con el diccionario recibido.

    Args:
        lista_usu (dict): Diccionario completo de usuarios a guardar.
    """
    # RESUELTO (Req 1): el guardado se envuelve en try/except OSError; si el archivo no se puede escribir (permisos,
    # disco lleno) se informa y no se corta el programa.
    try:
        with open(inf.RUTA_USUARIOS_JSON, 'w', encoding="utf-8") as archivo:
            json.dump(lista_usu, archivo, indent=4, ensure_ascii=False)
    except OSError as e:
        print(f"/// No se pudo escribir el archivo de usuarios: {e} ///")

def escribir_auto(lista_aut):
    """
    Sobreescribe el archivo del catalogo de autos con el diccionario recibido.

    Args:
        lista_aut (dict): Diccionario completo de autos a guardar.
    """
    # RESUELTO (Req 1): el guardado se envuelve en try/except OSError; si el archivo no se puede escribir se informa y
    # no se corta el programa.
    try:
        with open(inf.RUTA_AUTOS_JSON, 'w', encoding="utf-8") as archivo:
            json.dump(lista_aut, archivo, indent=4, ensure_ascii=False)
    except OSError as e:
        print(f"/// No se pudo escribir el archivo de autos: {e} ///")



# ---------- CREATE ----------

def agregar_auto():
    """
    Da de alta un auto nuevo (Create).

    Pide todos los datos del auto y valida que la patente no exista previamente.
    Al finalizar, guarda la ultima version del diccionario en el archivo JSON.
    (Req 2 del TP: Create sobreescribe el archivo).
    """
    autos = _cargar_autos()

    # Se pide la patente y se valida que no exista (una patente es unica).
    # RESUELTO (Req 1): se reemplazo el 'except: pass' por 'except EOFError' con retorno, de modo que 'patente' quede
    # siempre definida (antes un input fallido la dejaba sin definir -> NameError).
    try: patente = input("Patente del nuevo auto: ").strip().upper()
    except EOFError: return
    while patente in autos:
            try: patente = input("Esa patente ya existe. Ingrese otra: ").strip().upper()
            except EOFError: return

    # Se piden y validan los demas atributos del auto.
    marca = _pedir_de_tupla("Marca: ", MARCA)
    modelo = input("Modelo: ").strip().lower()
    calidad = _pedir_de_tupla("Calidad:", CALIDAD)
    anio = _pedir_entero("Año: ", 2000, 2026)
    precio = _pedir_float("Precio (u$d): ")
    categoria = _pedir_de_tupla("Categoría: ", CATEGORIA)

    # Se crea el registro usando la patente como clave del diccionario.
    # BUG (KeyError): esta alta no agrega la clave "estado", a diferencia de informe.informe_autos (que la inicializa en
    # True). Sin "estado", `_mostrar_auto`, `ver_stock` y `rentar_auto` lanzan KeyError al leerlo.
    # TODO(TP - Req 6): agregar "estado": True para respetar el esquema de 7 atributos por auto que exige la entidad del
    # Req 6.
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
def modificar_estado_auto(patente, estado_auto):
    """
    Modifica el estado de un auto en el archivo autos.json.

    Args:
        patente (str): Patente del auto a modificar.
        estado_auto (bool): Estado actual del auto (True = disponible, False = no disponible).
                            La funcion invierte este estado al guardar.
    Returns:
        None
    """
    # Invierte el estado: True = disponible -> pasa a False (rentado)
    # NOTA (posible error): la ruta "autos.json" esta escrita a mano (no usa la
    # constante RUTA_AUTOS) y si la patente no existe, autos[patente] da KeyError.
    if estado_auto == True:
        autos = _cargar_autos()
        autos[patente]["estado"] = False
        with open("autos.json", 'w', encoding="utf-8") as archivo:
            json.dump(autos, archivo, indent=4, ensure_ascii=False)
    # Invierte el estado: False = rentado -> pasa a True (disponible)
    elif estado_auto == False:
        autos = _cargar_autos()
        autos[patente]["estado"] = True
        with open("autos.json", 'w', encoding="utf-8") as archivo:
            json.dump(autos, archivo, indent=4, ensure_ascii=False)

def modificar_auto():
    """
    Modifica uno o mas campos de un auto existente (Update).

    Pide una patente valida, muestra los valores actuales y permite cambiar el
    campo elegido. Despues de cada cambio se guarda automaticamente en el JSON.
    (Req 2 del TP: Update sobreescribe el archivo).

    El bucle se repite hasta que el usuario elige la opcion [0] salir.
    """
    autos = _cargar_autos()
    if not autos:
            print("\nNo hay autos en el catálogo.")
            try: input("[Enter] ")
            except: pass
            return

    # NOTA (posible error): si el usuario escribe "0" para salir,
    # _pedir_patente_existente devuelve "0" y autos["0"] lanza KeyError
    # en el bucle de abajo.
    patente = _pedir_patente_existente(autos)

    while True:
        # Muestra el menu de campos con su valor actual.
        print(f"\n--- Modificar auto [{patente}] ---")
        
        for i, j in enumerate(autos[patente]):
            print(f"[{i+1}] {j.capitalize()}: {autos[patente][j]}")
        print("--------------------")
        print("[0] Terminar")

        opcion = input("\n¿Qué campo desea modificar?: ").strip()

        # Opcion para salir del menu de modificacion.
        if opcion == "0":
            break
        # Validacion de la opcion ingresada.
        # NOTA (posible error): int(opcion) lanza ValueError si el usuario escribe
        # algo que no sea un numero (solo se controla la opcion "0" antes).
        elif int(opcion) not in list(range(1, len(autos[patente]) + 1)):
            print("\nOpción no válida. Intente de nuevo.")
            continue

        # Se pide el nuevo valor segun el tipo de campo elegido.
        # NOTA: el mapeo 1-7 es fijo; si el auto tiene menos claves (por ejemplo,
        # no tiene "estado"), las opciones mostradas no coinciden con estos casos.
        
        if opcion == "1":
            autos[patente]["marca"] = _pedir_de_tupla("Marca", MARCA)
        elif opcion == "2":
            autos[patente]["modelo"] = input("Nuevo modelo: ").strip().lower()
        elif opcion == "3":
            autos[patente]["calidad"] = _pedir_de_tupla("Calidad", CALIDAD)
        elif opcion == "4":
            autos[patente]["año"] = _pedir_entero("Año", 2000, 2026)
        elif opcion == "5":
            autos[patente]["precio"] = _pedir_float("Nuevo precio (u$d)")
        elif opcion == "6":
            autos[patente]["categoria"] = _pedir_de_tupla("Categoría", CATEGORIA)
        elif opcion == "7":
            autos[patente]["estado"] = _pedir_de_tupla("estado", ESTADO)

        # Se guarda el cambio y se confirma.
        _guardar_autos(autos)
        print(f"\n{patente} actualizado correctamente.")



# ---------- DELETE ----------

def eliminar_auto():
    """
    Elimina un auto del catalogo segun su patente (Delete).

    Pide una patente existente, borra el registro del diccionario y sobreescribe
    el archivo JSON con la ultima version.
    (Req 2 del TP: Delete sobreescribe el archivo).
    """
    # RESUELTO (Req 1): la carga y el guardado se delegan en _cargar_autos() y _guardar_autos(), que ya manejan las
    # excepciones (FileNotFoundError, json.JSONDecodeError y OSError).
    autos = _cargar_autos()
    if not autos:
            print("\nNo hay autos en el catálogo.")
            try: input("[Enter] ")
            except: pass
            return

    patente = _pedir_patente_existente(autos)
    # BUG (KeyError): con la patente "0" (o None), 'del autos[patente]' intenta borrar una clave inexistente y lanza
    # KeyError.
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
        # RESUELTO (Req 1): el ingreso de la opcion usa try/except EOFError, asi 'opcion' quede siempre definida
        # (antes un input fallido la dejaba sin definir -> NameError); al terminar la entrada se sale del menu.
        try: opcion = input("Seleccione una opción: ").strip()
        except EOFError: break

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
    # TODO(TP - Req 3): verificar que autos.json contenga al menos 5 registros (precarga).
    limpiar()
    menu_crud()
    limpiar()
