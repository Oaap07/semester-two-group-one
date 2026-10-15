"""
REQUISITOS DEL TRABAJO PRACTICO (TPO – SPRINT) — Programacion I
Facultad de Ingenieria Informatica

Modulo: menu.py — Menu principal, alquileres y navegacion.
Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).

--------------------------------------------------------------------------------
OBJETIVO DEL TRABAJO
--------------------------------------------------------------------------------
Aplicar los conocimientos vistos en clase sobre archivos/JSON y manejo de
excepciones, ademas de los requisitos minimos del programa.

--------------------------------------------------------------------------------
PAUTAS / REQUISITOS DEL TP Y COMO SE RELACIONAN CON ESTE MODULO
--------------------------------------------------------------------------------
1) MANEJO DE EXCEPCIONES:
   Usar manejo de excepciones en apertura/lectura/escritura de archivos,
   ingreso de datos, conversiones y manipulacion de diccionarios.
   -> TODO(TP - Req 1): completar los try/except marcados en este archivo.

2) PERSISTENCIA DE INFORMACION:
   rentados.json guarda los autos alquilados (diccionario). Las acciones que
   modifican datos deben sobreescribir el archivo con la ultima version.
   (Se valora implementar las DOS opciones de persistencia).

3) PRECARGA DE INFORMACION:
   El catalogo se alimenta desde autos.json (precarga de al menos 5 registros).

4) TUPLA O CONJUNTO:
   Usar una tupla o conjunto dentro de la logica. Aqui se usan conjuntos
   (set comprehension) al filtrar modelos y claves de categorias.

5) LISTA POR COMPRENSION O LAMBDA:
   Incorporar al menos una lista por comprension o una funcion lambda.
   -> TODO(TP - Req 5): en rentar_auto() ya hay comprensiones; se pide
      documentarlas explicitamente y/o agregar una lambda aplicada a los datos.

6) ENTIDAD PRINCIPAL:
   Diccionario de diccionarios con un minimo de 5 atributos por elemento
   (tanto 'lista' de autos como 'rentados').

7) MENU CRUD COMPLETO:
   Menu principal + submenus de usuario y empresa.

8) REPORTE MATRICIAL:
   Los informes deben incluir al menos un reporte matricial (listas de listas).
   Recomendado: NumPy, Pandas y Matplotlib.
   -> TODO(TP - Req 8): implementar en el modulo informe.py.

9) DOCUMENTACION Y ENTREGA:
   Docstrings, codigo claro y organizado, informe en Word.

--------------------------------------------------------------------------------
CHECKLIST DE CUMPLIMIENTO (menu.py)
--------------------------------------------------------------------------------
[x] Integracion con JSON (autos.json y rentados.json).
[x] Menus y navegacion (principal, usuario, empresa).
[x] Uso de comprensiones al filtrar modelos/patentes.
[x] Docstrings en las funciones.
[ ] Req 1: try/except completo en la entrada/salida de archivos.
[ ] Req 5: documentar explicitamente una lista por comprension o lambda.
[ ] Req 8: asegurar el reporte matricial (delegado a informe.py).
[ ] Completar la logica de devolver_auto() y estado_rentas().

NOTA: Esta version solo AGREGA documentacion y marcas TODO(TP) para indicar
lo que falta. NO se modifico ninguna linea de logica del programa.
"""

import json, os
import informe as inf

def limpiar():
    """
    Limpia la consola segun el sistema operativo.

    En Windows usa 'cls'; en Linux/macOS usa 'clear'. Sirve para mantener la
    interfaz ordenada entre pantallas del menu.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def cargar_rentados():
    """
    Carga el diccionario de autos actualmente rentados desde `rentados.json`.

    Si el archivo no existe (primer uso o sin rentas), devuelve un diccionario
    vacio para evitar errores de lectura.

    Returns:
        dict: Estructura {patente: datos_del_auto, ...} con los mismos campos
        que cada auto de autos.json.

    Raises:
        json.JSONDecodeError: Si rentados.json tiene un formato invalido.
    """
    # TODO(TP - Req 1): ampliar el manejo de excepciones (JSONDecodeError, OSError).
    try:
        with open("rentados.json", 'r', encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError as e:
        #  Empieza con un diccionario vacio si no se encuentra el archivo 
        return {}
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        input("[Enter] ")
    


def guardar_rentados(rentados):
    """
    Guarda el diccionario de autos rentados en `rentados.json`.

    Sobreescribe el archivo con el estado actual. Se usa al alquilar un auto
    para actualizar el registro.
    (Req 2 del TP: la accion debe sobreescribir el archivo con la ultima version).

    Args:
        rentados (dict): Diccionario con los autos actualmente en alquiler.

    Raises:
        OSError: Si ocurre un error al abrir o escribir el archivo.
        TypeError: Si algun valor no es serializable a JSON.
    """
    # TODO(TP - Req 1): agregar try/except para el guardado (OSError).
    try:
        with open("rentados.json", 'w', encoding="utf-8") as archivo:
            json.dump(rentados, archivo, indent=4)
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        input("[Enter] ")
        return


def rentar_auto():
    """
    Flujo completo para alquilar un auto disponible.

    Pasos:
    1. Muestra las categorias de autos.
    2. Filtra los modelos disponibles de esa categoria, excluyendo los ya rentados.
    3. Muestra las patentes de ese modelo, tambien excluyendo los ya rentados.
    4. Confirma el alquiler guardando la ficha completa en `rentados.json`.

    El flujo esta anidado con bucles while para poder volver entre niveles
    (Categorias -> Modelos -> Patentes).

    Notas (Req 5 del TP):
        Se usan listas por comprension y conjuntos (set) para filtrar los datos.
        TODO(TP - Req 5): documentar explicitamente al menos una de estas
        comprensiones o agregar una funcion lambda aplicada a la informacion.
    """

    # Carga el catalogo completo de autos desde el archivo.
    # TODO(TP - Req 1): manejar excepciones (FileNotFoundError, JSONDecodeError).
    try:
        with open("autos.json", 'r', encoding="utf-8") as archivo:
            lista = json.load(archivo)
    except OSError as e:
        limpiar()
        print(f"/// Ocurrió un error de sistema: {e} ///")
        try: input("[Enter] ")
        except: pass
        return

    while True:
        limpiar()
        # --- NIVEL 1: seleccion de categoria ---
        print(" --- Escoja una categoría ---\n\n"
              "[1] Sedán / Hatchback\n"
              "[2] SUV / Crossover\n"
              "[3] Pick-up\n"
              "[4] Monovolumen / Utilitario (MPV)\n"
              "-------------------------\n"
              "[0] Para ir a Sub menú\n")
        
        try: opcion : str = input("\nSeleccione una opción: ").strip()
        except: opcion : str = ""
        # Relaciona cada opcion numerica con el valor interno de la categoria.
        categ_preset = {
            "1": "sedan_hatchback",
            "2": "suv_crossover",
            "3": "pickup",
            "4": "monovolumen_mpv"
        }

        if opcion == '0':
            # Volver al submenu de usuario.
            break
        elif opcion not in list(map(str, list(range(1,5)))): 
            # Validacion: la opcion debe estar entre 1 y 4.
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass
        else:
            # --- NIVEL 2: seleccion de modelo dentro de la categoria ---
            while True:
                limpiar()
                print("--- Modelos disponibles ---\n")

                # Estado actual de los autos rentados (se recarga cada vez).
                rentados = cargar_rentados()

                # Filtra modelos unicos disponibles de la categoria elegida.
                # Se considera "disponible" si pertenece a la categoria y su
                # patente NO esta en 'rentados'. Es una lista por comprension
                # que alimenta un conjunto (set) para eliminar duplicados.
                # TODO(TP - Req 5): esta comprension es un uso valido del requisito.
                filtrados = {str(i+1): j.capitalize() for i ,j in enumerate(list({lista[i]["modelo"] for i in lista if lista[i]["categoria"] == categ_preset[opcion] and i not in rentados}))}

                # Si no quedan modelos disponibles, se avisa y se vuelve a categorias.
                if not filtrados:
                    print("No hay autos disponibles en esta categoría.")
                    try: input("[Enter] ")
                    except: pass
                    break

                # Muestra el modelo numerado y una opcion para salir.
                [print(f"[{i}] {j}") for i, j in filtrados.items()]
                print("-------------------------")
                print("[0] Para salir a Categorías")
                
                try: opcion2 : str = input("\nSeleccione una opción: ").strip()
                except: opcion2 : str = ""

                if opcion2 == '0':
                    # Volver al nivel de categorias.
                    break
                elif opcion2 not in filtrados.keys():
                    # Validacion: el modelo debe estar entre los mostrados.
                    print("\nOpción no válida. Intente de nuevo.")
                    try: input("[Enter] ")
                    except: pass
                else:
                    # --- NIVEL 3: seleccion de patente del modelo elegido ---
                    while True:
                        limpiar()
                        print(f"--- PATENTES con Modelo: {filtrados[opcion2]}---")

                        # Lista por comprension: patentes de ese modelo que
                        # todavia no estan rentadas.
                        # TODO(TP - Req 5): otro uso de lista por comprension.
                        patentes = [i for i in lista if lista[i]["modelo"].capitalize() == filtrados[opcion2] and i not in rentados]

                        # Muestra la ficha resumida de cada patente disponible.
                        for i, j in enumerate(patentes):
                            
                            print(f"\n[{i+1}]: {j}\n"
                                f"\tCalidad: {lista[j]['calidad']}\n"\
                                f"\tAño: {lista[j]['año']}\n"\
                                f"\tPrecio: u$d {lista[j]['precio']:.1f}")
                        print("-------------------------")
                        print("[0] Para salir a Modelos")

                        try: opcion3 : str = input("\nSeleccione una opción: ").strip()
                        except: opcion3 : str = ""

                        if opcion3 == '0':
                            # Volver al nivel de modelos.
                            break
                        elif opcion3 not in list(map(str, list(range(1, len(patentes)+1)))):
                            # Validacion: la opcion debe corresponder a una patente mostrada.
                            print("\nOpción no válida. Intente de nuevo.")
                            try: input("[Enter] ")
                            except: pass
                        else:
                            # --- Confirmacion y registro del alquiler ---
                            limpiar()
                            patente_elegida = patentes[int(opcion3)-1]
                            print(f"\n¡Auto con patente: {patente_elegida} RENTADO!")
        
                            # Se copia la ficha completa del auto al diccionario
                            # de rentados y se guarda (sobreescribe el archivo).
                            # TODO(TP - Req 1): validar claves (KeyError) y guardar con try/except.
                            rentados[patente_elegida] = lista[patente_elegida]
                            guardar_rentados(rentados)

                            try: input("[Enter] ")
                            except: pass
                            # Salir del bucle de patentes tras alquilar.
                            break
                    # Salir del bucle de modelos.
                    break
            break
        


def devolver_auto():
    """
    Interfaz para registrar la devolucion de un auto rentado.

    Actualmente solo muestra un mensaje informativo y espera confirmacion.
    TODO(TP): completar la funcionalidad:
        - Listar los autos rentados (patente + datos).
        - Pedir la patente a devolver, validando que exista.
        - Eliminarla de `rentados.json` (sobreescribir el archivo con la
          ultima version del diccionario).
        - Informar que la devolucion se realizo correctamente.
    """
    limpiar()
    # TODO(TP - Req 1): manejar excepciones al cargar.
    rentados = cargar_rentados()

    # Si no hay autos rentados, se avisa y se sale de la funcion.
    if rentados == None:
        print("No hay autos rentados actualmente.")
        input("\n[Enter]")

    # Interfaz base (en desarrollo).
    print("¿Que auto desea devolver?")
    print("="*15)
    try: input("[Enter] ")
    except: pass


def estado_rentas():
    """
    Muestra el estado actual de los autos rentados.

    Lee `rentados.json` y muestra un listado de los autos (patentes y datos).
    TODO(TP): completar la visualizacion con el formato de ficha y considerar
    el uso de una lista por comprension o lambda para resumir la informacion.
    """
    limpiar()
    # TODO(TP - Req 1): manejar excepciones al cargar.
    rentados = cargar_rentados()
    print("--- ESTADO DE AUTOS RENTADOS ---\n")
    # TODO(TP): recorrer 'rentados' y mostrar la informacion de cada auto.
    # TODO(TP - Req 5): aplicar lista por comprension o lambda para un resumen.
    try: input("[Enter] ")
    except: pass

# ---------- Menus ----------

def menu_principal():
    """
    Menu principal del sistema.

    Permite acceder al submenu de usuario o al submenu de empresa.
    El bucle termina cuando se selecciona [0] Salir.
    """
    while True:
        limpiar()
        print("--- MENÚ PRINCIPAL ---\n")
        print("[1] Menu de usuario.")
        print("[2] Menu de empresa.")
        print("-------------------------")
        print("[0] Salir.")
        
        
        try: opcion = input("\nSeleccione una opción: ").strip()
        except: opcion : str = ""

        # Despacho de la opcion elegida hacia el submenu correspondiente.
        if opcion == "1":
            submenu_usuario()
        elif opcion == "2":
            submenu_empresa()
        elif opcion == "0":
            # Finalizar la ejecucion del programa.
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass


def submenu_usuario():
    """
    Submenu destinado al usuario final.

    Ofrece acciones de alquiler: rentar auto o devolver auto.
    Permite volver al menu principal con [0].
    """
    while True:
        limpiar()
        print("--- SUBMENÚ: MANEJO DE AUTOS ---\n")
        print("[1] Rentar auto.")
        print("[2] Devolver auto.")
        print("-------------------------")
        print("[0] Volver al menú principal")
        
        try: opcion : str = input("\nSeleccione una opción: ").strip()
        except: opcion : str = ""

        if opcion == "1":
            rentar_auto()
        elif opcion == "2":
            devolver_auto()
        elif opcion == "0":
            # Volver al menu principal.
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass


def submenu_empresa():
    """
    Submenu destinado a la empresa (gestion e informes).

    Accede a las funciones de informe del modulo `informe`:
    - Disponibilidad de unidades.
    - Estadisticas del mes.
    - Estado de autos rentados (funcion local estado_rentas).
    Permite volver al menu principal con [0].

    Importante (Req 8 del TP): las funciones de informe deben generar al menos
    UN REPORTE MATRICIAL (listas de listas). Recomendado NumPy/Pandas/Matplotlib.
    """
    while True:
        limpiar()
        print("--- SUBMENÚ: INFORMES ---\n")
        print("[1] Disponibilidad de unidades")
        print("[2] Estadisticas del mes")
        print("[3] Estado de autos rentados")
        print("[0] Volver al menú principal")

        try: opcion : str = input("\nSeleccione una opción: ").strip()
        except: opcion : str = ""

        if opcion == "1":
            # Informe de disponibilidad (modulo informe).
            # TODO(TP - Req 8): verificar que incluya un reporte matricial.
            informe.informe_disponibilidad()
        elif opcion == "2":
            # Informe de estadisticas (modulo informe).
            # TODO(TP - Req 8): verificar que incluya un reporte matricial.
            informe.informe_estadisticas()
        elif opcion == "3":
            # Estado local de los autos rentados.
            estado_rentas()
        elif opcion == "0":
            # Volver al menu principal.
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass

if __name__ == "__main__":
    # Inicio de la aplicacion.
    # TODO(TP - Req 3): confirmar que autos.json tenga al menos 5 registros (precarga).
    limpiar()
    menu_principal()
    limpiar()