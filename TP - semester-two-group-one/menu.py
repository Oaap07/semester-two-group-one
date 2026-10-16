"""
Requisitos del Trabajo Practico (TPO - SPRINT) - Programacion I
Facultad de Ingenieria Informatica

Modulo: menu.py - Menu principal, alquileres y navegacion.
Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).
"""

import json, os
import informe as inf
import crud as cd
import usuarios as us

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

def rentar_auto(usu_info):
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
        Se documentan explicitamente las listas por comprension utilizadas.
    """

    # Carga el catalogo completo de autos desde el archivo.
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
        print(f" --- Escoja una categoría --- [{usu_info[0]}]\n\n"
            "[1] Sedán / Hatchback\n"
            "[2] SUV / Crossover\n"
            "[3] Pick-up\n"
            "[4] Monovolumen / Utilitario (MPV)\n"
            "-------------------------\n"
            "[0] Para ir a Sub menú\n")

        try:
            opcion: str = input("\nSeleccione una opción: ").strip()
        except:
            opcion: str = ""
        # Relaciona cada opcion numerica con el valor interno de la categoria.

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
                print(f"--- Modelos disponibles --- [{usu_info[0]}]\n")

                # Filtra modelos unicos disponibles de la categoria elegida.
                # Se considera "disponible" si pertenece a la categoria y su
                # patente NO esta en 'rentados'. Es una lista por comprension
                # que alimenta un conjunto (set) para eliminar duplicados.
                # TODO(TP - Req 5): esta comprension es un uso valido del requisito.
                filtrados = {str(i+1): j.capitalize() for i ,j in enumerate(list({lista[i]["modelo"] for i in lista if lista[i]["categoria"] == categ_preset[opcion] and lista[i]["estado"] == True }))}

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
                        print(f"--- PATENTES con Modelo: {filtrados[opcion2]}---  [{usu_info[0]}]")

                        # Lista por comprension: patentes de ese modelo que
                        # todavia no estan rentadas.
                        # TODO(TP - Req 5): otro uso de lista por comprension.
                        patentes = [i for i in lista if lista[i]["modelo"].capitalize() == filtrados[opcion2] and lista[i]["estado"] == True]

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
                            cd.modificar_estado_auto(patente_elegida, True)
                            print(f"\n¡Auto con patente: {patente_elegida} RENTADO!")
                            try: input("[Enter] ")
                            except: pass
                            # Salir del bucle de patentes tras alquilar.
                            return 

def devolver_auto():
    """
    Interfaz para registrar la devolucion de un auto rentado.

    Actualmente solo muestra los autos rentados y los devuelve(creo).
    TODO(TP): completar la funcionalidad:
        - Pedir la patente a devolver, validando que exista.
        - Informar que la devolucion se realizo correctamente.
    """
    limpiar()
    # TODO(TP - Req 1): manejar excepciones al cargar.
    #en desarrollo
    patentes = [i for i in lista if lista[i]["modelo"].capitalize() == filtrados[opcion2] and lista[i]["estado"] == False]
    # Si no hay autos rentados, se avisa y se sale de la funcion.
    if len() == 0:
        limpiar()
        print("No hay autos rentados actualmente.")
        input("\n[Enter]")
    else:
        print("¿Que auto desea devolver?")
        print("="*15)
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
                # Volver.
                break
            elif opcion3 not in list(map(str, list(range(1, len(patentes)+1)))):
                # Validacion: la opcion debe corresponder a una patente mostrada.
                print("\nOpción no válida. Intente de nuevo.")
                try: input("[Enter] ")
                except: pass
            else:
                # --- Confirmacion y registro de devolucion ---
                limpiar()
                patente_elegida = patentes[int(opcion3)-1]
                cd.modificar_estado_auto(patente_elegida, False)
                print(f"\n¡Auto con patente: {patente_elegida} DEVUELTO!")
                try: input("[Enter] ")
                except: pass
                # Salir del bucle de patentes tras devolver.
                return 
        try: input("[Enter] ")
        except: pass

# Muestra autos disponibles aplicando filtros por categoria/modelo (contexto global: lista, opcion, opcion2)
def informe_disponibilidad():
    """
    Muestra la lista de autos disponibles segun filtros seleccionados.

    Esta funcion forma parte de los informes para el submenu de empresa.
    NOTA: Esta funcion esta incompleta en la implementacion actual (utiliza
    variables globales como 'lista', 'opcion' y 'opcion2' que se espera
    que esten definidas en el contexto desde donde se llama). No modifica
    el comportamiento existente.

    Returns:
        None
    """
    filtrados = {str(i+1): j.capitalize() for i ,j in enumerate(list({lista[i]["modelo"] for i in lista if lista[i]["categoria"] == categ_preset[opcion] and lista[i]["estado"] == True }))}
    patentes = [i for i in lista if lista[i]["modelo"].capitalize() == filtrados[opcion2] and lista[i]["estado"] == True]

    if len(patentes) == 0: #no se si esto anda, pense en poner filtrados tmb
        limpiar()
        print("No hay autos disponibles actualmente.")
        input("\n[Enter]")
    else:
        for i, j in enumerate(patentes):

            print(f"\n[{i+1}]: {j}\n"
                f"\tCalidad: {lista[j]['calidad']}\n"\
                f"\tAño: {lista[j]['año']}\n"\
                f"\tPrecio: u$d {lista[j]['precio']:.1f}")
            print("-------------------------")

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
        
        
        try: 
            opcion = input("\nSeleccione una opción: ").strip()

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

        except: opcion : str = ""


def submenu_usuario():
    """
    Submenu destinado al usuario final.

    Ofrece acciones de alquiler: ingresar, registrarse, rentar auto o devolver auto.
    Permite volver al menu principal con [0].
    """
    with open("usuarios.json", 'r', encoding="utf-8") as archivo:
        lista = json.load(archivo)

    while True:
        limpiar()
        print("--- INGRESO: USUARIOS ---\n")
        print("[1] Ingresar")
        print("[2] Registrarse")
        print("-------------------------")
        print("[0] Volver al menú principal")
        try:
            opcion : str = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                usu_info : tuple = us.ingresa_usuario(lista)
                if not usu_info: usu_info
                else: break
            elif opcion == "2":
                us.registro_usuario(lista)
            elif opcion == "0":
                return
            else:
                print("\nOpción no válida. Intente de nuevo.")
                try: input("[Enter] ")
                except: pass

        except: opcion = ""


    while True:
        limpiar()
        print("--- SUBMENÚ: MANEJO DE AUTOS ---", end="")
        print(f"  [{usu_info[0]}]\n")
        print("[1] Rentar auto.")
        print("[2] Devolver auto.")
        print("-------------------------")
        print("[0] Volver al menú principal")
        
        try: 
            opcion : str = input("\nSeleccione una opción: ").strip()
            if opcion == "1":
                rentar_auto(usu_info)
            elif opcion == "2":
                devolver_auto(usu_info)
            elif opcion == "0":
                # Volver al menu principal.
                break
            else:
                print("\nOpción no válida. Intente de nuevo.")
                try: input("[Enter] ")
                except: pass
        except: opcion : str = ""


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
            informe_disponibilidad()
        elif opcion == "2":
            # Informe de estadisticas (modulo informe).
            # TODO(TP - Req 8): verificar que incluya un reporte matricial.
            informe_estadisticas()
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
