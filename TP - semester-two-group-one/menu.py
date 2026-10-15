"""
Requisitos del Trabajo PrÃ¡ctico (TPO - SPRINT) - ProgramaciÃ³n I
Facultad de IngenierÃ­a InformÃ¡tica

MÃ³dulo: menu.py - MenÃº principal, alquileres y navegaciÃ³n.
Tema del trabajo: AdministraciÃ³n de una concesionaria (catÃ¡logo de autos + alquileres).
"""

import json, os
import informe as inf
import crud as cd

def limpiar():
    """
    Limpia la consola segun el sistema operativo.

    En Windows usa 'cls'; en Linux/macOS usa 'clear'. Sirve para mantener la
    interfaz ordenada entre pantallas del menÃº.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

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
        Se usan listas por comprensiÃ³n y conjuntos (set) para filtrar los datos.
        Se documentan explÃ­citamente las listas por comprensiÃ³n utilizadas.
    """

    # Carga el catalogo completo de autos desde el archivo.
    try:
        with open("autos.json", 'r', encoding="utf-8") as archivo:
            lista = json.load(archivo)
    except OSError as e:
        limpiar()
        print(f"/// OcurriÃ³ un error de sistema: {e} ///")
        try: input("[Enter] ")
        except: pass
        return
    

    while True:
        limpiar()
        # --- NIVEL 1: selecciÃ³n de categorÃ­a ---
        print(" --- Escoja una categorÃ­a ---\n\n"
            "[1] SedÃ¡n / Hatchback\n"
            "[2] SUV / Crossover\n"
            "[3] Pick-up\n"
            "[4] Monovolumen / Utilitario (MPV)\n"
            "-------------------------\n"
            "[0] Para ir a Sub menÃº\n")

        try:
            opcion: str = input("\nSeleccione una opciÃ³n: ").strip()
        except:
            opcion: str = ""
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
            print("\nOpciÃ³n no vÃ¡lida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass
        else:
            # --- NIVEL 2: seleccion de modelo dentro de la categoria ---
            while True:
                limpiar()
                print("--- Modelos disponibles ---\n")

                # Filtra modelos unicos disponibles de la categoria elegida.
                # Se considera "disponible" si pertenece a la categoria y su
                # patente NO esta en 'rentados'. Es una lista por comprension
                # que alimenta un conjunto (set) para eliminar duplicados.
                # TODO(TP - Req 5): esta comprension es un uso valido del requisito.
                filtrados = {str(i+1): j.capitalize() for i ,j in enumerate(list({lista[i]["modelo"] for i in lista if lista[i]["categoria"] == categ_preset[opcion] and lista[i]["estado"] == True }))}

                # Si no quedan modelos disponibles, se avisa y se vuelve a categorias.
                if not filtrados:
                    print("No hay autos disponibles en esta categorÃ­a.")
                    try: input("[Enter] ")
                    except: pass
                    break

                # Muestra el modelo numerado y una opcion para salir.
                [print(f"[{i}] {j}") for i, j in filtrados.items()]
                print("-------------------------")
                print("[0] Para salir a CategorÃ­as")
                
                try: opcion2 : str = input("\nSeleccione una opciÃ³n: ").strip()
                except: opcion2 : str = ""

                if opcion2 == '0':
                    # Volver al nivel de categorias.
                    break
                elif opcion2 not in filtrados.keys():
                    # Validacion: el modelo debe estar entre los mostrados.
                    print("\nOpciÃ³n no vÃ¡lida. Intente de nuevo.")
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
                        patentes = [i for i in lista if lista[i]["modelo"].capitalize() == filtrados[opcion2] and lista[i]["estado"] == True]

                        # Muestra la ficha resumida de cada patente disponible.
                        for i, j in enumerate(patentes):
                            
                            print(f"\n[{i+1}]: {j}\n"
                                f"\tCalidad: {lista[j]['calidad']}\n"\
                                f"\tAÃ±o: {lista[j]['aÃ±o']}\n"\
                                f"\tPrecio: u$d {lista[j]['precio']:.1f}")
                        print("-------------------------")
                        print("[0] Para salir a Modelos")

                        try: opcion3 : str = input("\nSeleccione una opciÃ³n: ").strip()
                        except: opcion3 : str = ""

                        if opcion3 == '0':
                            # Volver al nivel de modelos.
                            break
                        elif opcion3 not in list(map(str, list(range(1, len(patentes)+1)))):
                            # Validacion: la opcion debe corresponder a una patente mostrada.
                            print("\nOpciÃ³n no vÃ¡lida. Intente de nuevo.")
                            try: input("[Enter] ")
                            except: pass
                        else:
                            # --- Confirmacion y registro del alquiler ---
                            limpiar()
                            patente_elegida = patentes[int(opcion3)-1]
                            cd.modificar_estado_auto(patente_elegida)
                            print(f"\nÂ¡Auto con patente: {patente_elegida} RENTADO!")
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
        - ultima version del diccionario).
        - Informar que la devolucion se realizo correctamente.
    """
    limpiar()
    
    # TODO(TP - Req 1): manejar excepciones al cargar.

    # Si no hay autos rentados, se avisa y se sale de la funcion.
    print("No hay autos rentados actualmente.")
    input("\n[Enter]")

    # Interfaz base (en desarrollo).
    print("Â¿Que auto desea devolver?")
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
        print("--- MENÃ PRINCIPAL ---\n")
        print("[1] Menu de usuario.")
        print("[2] Menu de empresa.")
        print("-------------------------")
        print("[0] Salir.")
        
        
        try: opcion = input("\nSeleccione una opciÃ³n: ").strip()
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
            print("\nOpciÃ³n no vÃ¡lida. Intente de nuevo.")
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
        print("--- SUBMENÃ: MANEJO DE AUTOS ---\n")
        print("[1] Rentar auto.")
        print("[2] Devolver auto.")
        print("-------------------------")
        print("[0] Volver al menÃº principal")
        
        try: opcion : str = input("\nSeleccione una opciÃ³n: ").strip()
        except: opcion : str = ""

        if opcion == "1":
            rentar_auto()
        elif opcion == "2":
            devolver_auto()
        elif opcion == "0":
            # Volver al menu principal.
            break
        else:
            print("\nOpciÃ³n no vÃ¡lida. Intente de nuevo.")
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
        print("--- SUBMENÃ: INFORMES ---\n")
        print("[1] Disponibilidad de unidades")
        print("[2] Estadisticas del mes")
        print("[3] Estado de autos rentados")
        print("[0] Volver al menÃº principal")

        try: opcion : str = input("\nSeleccione una opciÃ³n: ").strip()
        except: opcion : str = ""

        if opcion == "1":
            # Informe de disponibilidad (modulo informe).
            # TODO(TP - Req 8): verificar que incluya un reporte matricial.
            inf.informe_disponibilidad()
        elif opcion == "2":
            # Informe de estadisticas (modulo informe).
            # TODO(TP - Req 8): verificar que incluya un reporte matricial.
            inf.informe_estadisticas()
        elif opcion == "3":
            # Estado local de los autos rentados.
            estado_rentas()
        elif opcion == "0":
            # Volver al menu principal.
            break
        else:
            print("\nOpciÃ³n no vÃ¡lida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass

if __name__ == "__main__":
    # Inicio de la aplicacion.
    # TODO(TP - Req 3): confirmar que autos.json tenga al menos 5 registros (precarga).
    limpiar()
    menu_principal()
    limpiar()