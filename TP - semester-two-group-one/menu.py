"""
REQUISITOS DEL TRABAJO PRÁCTICO (TPO – SPRINT) — Programación I
Facultad de Ingeniería Informática

Módulo: menu.py — Menú principal, alquileres y navegación.
Tema del trabajo: Administración de una concesionaria (catálogo de autos + alquileres).

--------------------------------------------------------------------------------
OBJETIVO DEL TRABAJO
--------------------------------------------------------------------------------
Aplicar los conocimientos vistos en clase sobre archivos/JSON y manejo de
excepciones, además de los requisitos mínimos del programa.

--------------------------------------------------------------------------------
PAUTAS / REQUISITOS DEL TP Y CÓMO SE RELACIONAN CON ESTE MÓDULO
--------------------------------------------------------------------------------
1) MANEJO DE EXCEPCIONES:
   Usar manejo de excepciones en apertura/lectura/escritura de archivos,
   ingreso de datos, conversiones y manipulación de diccionarios.
   -> TODO(TP - Req 1): completar los try/except marcados en este archivo.

2) PERSISTENCIA DE INFORMACIÓN:
   rentados.json guarda los autos alquilados (diccionario). Las acciones que
   modifican datos deben sobreescribir el archivo con la última versión.
   (Se valora implementar las DOS opciones de persistencia).

3) PRECARGA DE INFORMACIÓN:
   El catálogo se alimenta desde autos.json (precarga de al menos 5 registros).

4) TUPLA O CONJUNTO:
   Usar una tupla o conjunto dentro de la lógica. Aquí se usan conjuntos
   (set comprehension) al filtrar modelos y claves de categorías.

5) LISTA POR COMPRENSIÓN O LAMBDA:
   Incorporar al menos una lista por comprensión o una función lambda.
   -> TODO(TP - Req 5): en rentar_auto() ya hay comprensiones; se pide
      documentarlas explícitamente y/o agregar una lambda aplicada a los datos.

6) ENTIDAD PRINCIPAL:
   Diccionario de diccionarios con un mínimo de 5 atributos por elemento
   (tanto 'lista' de autos como 'rentados').

7) MENÚ CRUD COMPLETO:
   Menú principal + submenús de usuario y empresa.

8) REPORTE MATRICIAL:
   Los informes deben incluir al menos un reporte matricial (listas de listas).
   Recomendado: NumPy, Pandas y Matplotlib.
   -> TODO(TP - Req 8): implementar en el módulo informe.py.

9) DOCUMENTACIÓN Y ENTREGA:
   Docstrings, código claro y organizado, informe en Word.

--------------------------------------------------------------------------------
CHECKLIST DE CUMPLIMIENTO (menu.py)
--------------------------------------------------------------------------------
[x] Integración con JSON (autos.json y rentados.json).
[x] Menús y navegación (principal, usuario, empresa).
[x] Uso de comprensiones al filtrar modelos/patentes.
[x] Docstrings en las funciones.
[ ] Req 1: try/except completo en la entrada/salida de archivos.
[ ] Req 5: documentar explícitamente una lista por comprensión o lambda.
[ ] Req 8: asegurar el reporte matricial (delegado a informe.py).
[ ] Completar la lógica de devolver_auto() y estado_rentas().

NOTA: Esta versión solo AGREGA documentación y marcas TODO(TP) para indicar
lo que falta. NO se modificó ninguna línea de lógica del programa.
"""

import json, os
import informe as inf

def limpiar():
    """
    Limpia la consola según el sistema operativo.

    En Windows usa 'cls'; en Linux/macOS usa 'clear'. Sirve para mantener la
    interfaz ordenada entre pantallas del menú.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def cargar_rentados():
    """
    Carga el diccionario de autos actualmente rentados desde `rentados.json`.

    Si el archivo no existe (primer uso o sin rentas), devuelve un diccionario
    vacío para evitar errores de lectura.

    Returns:
        dict: Estructura {patente: datos_del_auto, ...} con los mismos campos
        que cada auto de autos.json.

    Raises:
        json.JSONDecodeError: Si rentados.json tiene un formato inválido.
    """
    # TODO(TP - Req 1): ampliar el manejo de excepciones (JSONDecodeError, OSError).
    try:
        with open("rentados.json", 'r', encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError as e:
        #  Empieza con un diccionario vacío si no se encuentra el archivo 
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
    (Req 2 del TP: la acción debe sobreescribir el archivo con la última versión).

    Args:
        rentados (dict): Diccionario con los autos actualmente en alquiler.

    Raises:
        OSError: Si ocurre un error al abrir o escribir el archivo.
        TypeError: Si algún valor no es serializable a JSON.
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
    1. Muestra las categorías de autos.
    2. Filtra los modelos disponibles de esa categoría, excluyendo los ya rentados.
    3. Muestra las patentes de ese modelo, también excluyendo los ya rentados.
    4. Confirma el alquiler guardando la ficha completa en `rentados.json`.

    El flujo está anidado con bucles while para poder volver entre niveles
    (Categorías -> Modelos -> Patentes).

    Notas (Req 5 del TP):
        Se usan listas por comprensión y conjuntos (set) para filtrar los datos.
        TODO(TP - Req 5): documentar explícitamente al menos una de estas
        comprensiones o agregar una función lambda aplicada a la información.
    """

    # Carga el catálogo completo de autos desde el archivo.
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
        # --- NIVEL 1: selección de categoría ---
        print(" --- Escoja una categoría ---\n\n"
              "[1] Sedán / Hatchback\n"
              "[2] SUV / Crossover\n"
              "[3] Pick-up\n"
              "[4] Monovolumen / Utilitario (MPV)\n"
              "-------------------------\n"
              "[0] Para ir a Sub menú\n")
        
        try: opcion : str = input("\nSeleccione una opción: ").strip()
        except: opcion : str = ""
        # Relaciona cada opción numérica con el valor interno de la categoría.
        categ_preset = {
            "1": "sedan_hatchback",
            "2": "suv_crossover",
            "3": "pickup",
            "4": "monovolumen_mpv"
        }

        if opcion == '0':
            # Volver al submenú de usuario.
            break
        elif opcion not in list(map(str, list(range(1,5)))): 
            # Validación: la opción debe estar entre 1 y 4.
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass
        else:
            # --- NIVEL 2: selección de modelo dentro de la categoría ---
            while True:
                limpiar()
                print("--- Modelos disponibles ---\n")

                # Estado actual de los autos rentados (se recarga cada vez).
                rentados = cargar_rentados()

                # Filtra modelos únicos disponibles de la categoría elegida.
                # Se considera "disponible" si pertenece a la categoría y su
                # patente NO está en 'rentados'. Es una lista por comprensión
                # que alimenta un conjunto (set) para eliminar duplicados.
                # TODO(TP - Req 5): esta comprensión es un uso válido del requisito.
                filtrados = {str(i+1): j.capitalize() for i ,j in enumerate(list({lista[i]["modelo"] for i in lista if lista[i]["categoria"] == categ_preset[opcion] and i not in rentados}))}

                # Si no quedan modelos disponibles, se avisa y se vuelve a categorías.
                if not filtrados:
                    print("No hay autos disponibles en esta categoría.")
                    try: input("[Enter] ")
                    except: pass
                    break

                # Muestra el modelo numerado y una opción para salir.
                [print(f"[{i}] {j}") for i, j in filtrados.items()]
                print("-------------------------")
                print("[0] Para salir a Categorías")
                
                try: opcion2 : str = input("\nSeleccione una opción: ").strip()
                except: opcion2 : str = ""

                if opcion2 == '0':
                    # Volver al nivel de categorías.
                    break
                elif opcion2 not in filtrados.keys():
                    # Validación: el modelo debe estar entre los mostrados.
                    print("\nOpción no válida. Intente de nuevo.")
                    try: input("[Enter] ")
                    except: pass
                else:
                    # --- NIVEL 3: selección de patente del modelo elegido ---
                    while True:
                        limpiar()
                        print(f"--- PATENTES con Modelo: {filtrados[opcion2]}---")

                        # Lista por comprensión: patentes de ese modelo que
                        # todavía no están rentadas.
                        # TODO(TP - Req 5): otro uso de lista por comprensión.
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
                            # Validación: la opción debe corresponder a una patente mostrada.
                            print("\nOpción no válida. Intente de nuevo.")
                            try: input("[Enter] ")
                            except: pass
                        else:
                            # --- Confirmación y registro del alquiler ---
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
    Interfaz para registrar la devolución de un auto rentado.

    Actualmente solo muestra un mensaje informativo y espera confirmación.
    TODO(TP): completar la funcionalidad:
        - Listar los autos rentados (patente + datos).
        - Pedir la patente a devolver, validando que exista.
        - Eliminarla de `rentados.json` (sobreescribir el archivo con la
          última versión del diccionario).
        - Informar que la devolución se realizó correctamente.
    """
    limpiar()
    # TODO(TP - Req 1): manejar excepciones al cargar.
    rentados = cargar_rentados()

    # Si no hay autos rentados, se avisa y se sale de la función.
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
    TODO(TP): completar la visualización con el formato de ficha y considerar
    el uso de una lista por comprensión o lambda para resumir la información.
    """
    limpiar()
    # TODO(TP - Req 1): manejar excepciones al cargar.
    rentados = cargar_rentados()
    print("--- ESTADO DE AUTOS RENTADOS ---\n")
    # TODO(TP): recorrer 'rentados' y mostrar la información de cada auto.
    # TODO(TP - Req 5): aplicar lista por comprensión o lambda para un resumen.
    try: input("[Enter] ")
    except: pass

# ---------- Menús ----------

def menu_principal():
    """
    Menú principal del sistema.

    Permite acceder al submenú de usuario o al submenú de empresa.
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

        # Despacho de la opción elegida hacia el submenú correspondiente.
        if opcion == "1":
            submenu_usuario()
        elif opcion == "2":
            submenu_empresa()
        elif opcion == "0":
            # Finalizar la ejecución del programa.
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass


def submenu_usuario():
    """
    Submenú destinado al usuario final.

    Ofrece acciones de alquiler: rentar auto o devolver auto.
    Permite volver al menú principal con [0].
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
            # Volver al menú principal.
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass


def submenu_empresa():
    """
    Submenú destinado a la empresa (gestión e informes).

    Accede a las funciones de informe del módulo `informe`:
    - Disponibilidad de unidades.
    - Estadísticas del mes.
    - Estado de autos rentados (función local estado_rentas).
    Permite volver al menú principal con [0].

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
            # Informe de disponibilidad (módulo informe).
            # TODO(TP - Req 8): verificar que incluya un reporte matricial.
            informe.informe_disponibilidad()
        elif opcion == "2":
            # Informe de estadísticas (módulo informe).
            # TODO(TP - Req 8): verificar que incluya un reporte matricial.
            informe.informe_estadisticas()
        elif opcion == "3":
            # Estado local de los autos rentados.
            estado_rentas()
        elif opcion == "0":
            # Volver al menú principal.
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass

if __name__ == "__main__":
    # Inicio de la aplicación.
    # TODO(TP - Req 3): confirmar que autos.json tenga al menos 5 registros (precarga).
    limpiar()
    menu_principal()
    limpiar()