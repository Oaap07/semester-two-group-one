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

# Mapeo de la opcion de menu a la categoria interna usada en autos.json.
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

def rentar_auto(usu_info, lista_usu, lista_aut):
    """
    Flujo completo para alquilar un auto disponible.

    Pasos:
    1. Muestra las categorias de autos.
    2. Filtra los modelos disponibles de esa categoria, excluyendo los ya rentados.
    3. Muestra las patentes de ese modelo, tambien excluyendo los ya rentados.
    4. Confirma el alquiler: marca el auto como no disponible en `autos.json` y
       agrega la patente a `autos_rentados` del usuario en `usuarios.json`.

    El flujo esta anidado con bucles while para poder volver entre niveles
    (Categorias -> Modelos -> Patentes).

    Args:
        usu_info (list): [dni, nombre, autos_rentados] del usuario logueado.
        lista_usu (dict): Todos los usuarios (para guardar el alquiler).
        lista_aut (dict): Catalogo de autos (para filtrar los disponibles).

    Notas (Req 5 del TP):
        Se usan listas por comprension y conjuntos (set) para filtrar los datos.
        Se documentan explicitamente las listas por comprension utilizadas.
    """

    while True:
        limpiar()
        # --- NIVEL 1: seleccion de categoria ---
        print(f" --- Escoja una categoría --- [{usu_info[1]}]\n\n"
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
                print(f"--- Modelos disponibles --- [{usu_info[1]}]\n")

                # Filtra modelos unicos disponibles de la categoria elegida.
                # Se considera "disponible" si pertenece a la categoria y su
                # patente NO esta en 'rentados'. Es una lista por comprension
                # que alimenta un conjunto (set) para eliminar duplicados.
                # TODO(TP - Req 5): esta comprension es un uso valido del requisito.
                filtrados = {str(i+1): j.capitalize() for i ,j in enumerate(list({lista_aut[i]["modelo"] for i in lista_aut if lista_aut[i]["categoria"] == categ_preset[opcion] and lista_aut[i]["estado"] == True }))}

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
                    try:
                        while True:
                            limpiar()
                            print(f"--- PATENTES con Modelo: {filtrados[opcion2]}---  [{usu_info[1]}]")

                            # Lista por comprension: patentes de ese modelo que
                            # todavia no estan rentadas.
                            # TODO(TP - Req 5): otro uso de lista por comprension.
                            patentes = [i for i in lista_aut.keys() if lista_aut[i]["modelo"].capitalize() == filtrados[opcion2] and lista_aut[i]["estado"] == True]

                            # Muestra la ficha resumida de cada patente disponible.
                            for i, j in enumerate(patentes):
                                
                                print(f"\n[{i+1}]: {j}\n"
                                    f"\tCalidad: {lista_aut[j]['calidad']}\n"\
                                    f"\tAño: {lista_aut[j]['año']}\n"\
                                    f"\tPrecio: u$d {lista_aut[j]['precio']:.1f}")
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
                                # El usuario eligio un numero; se obtiene la patente.
                                patente_elegida = patentes[int(opcion3)-1]
                                # Marca el auto como no disponible (rentado) en autos.json.
                                cd.modificar_estado_auto(patente_elegida, True)
                                # Agrega la patente a los autos rentados del usuario
                                # (usu_info[0] es el DNI, que es la clave en lista_usu).
                                lista_usu[usu_info[0]]["autos_rentados"].append(patente_elegida)
                                # NOTA (bug conocido "renta infinita"): modificar_estado_auto
                                # escribe el cambio en autos.json, pero 'lista_aut' en memoria
                                # no se actualiza; el auto sigue con estado True y se puede
                                # volver a rentar en la misma sesion.
                                # Persiste los usuarios (con el nuevo alquiler).
                                cd.escribir_usuario(lista_usu)
                                # Salir del bucle de patentes tras alquilar.
                                return 
                    # NOTA (manejo generico): atrapa cualquier excepcion y la
                    # muestra con input(e). El Req 1 del TP pide excepciones
                    # especificas en lugar de un except generico.
                    except Exception as e: input(e)

def devolver_auto(usu_info, lista_usu, lista_aut):
    """
    Interfaz para registrar la devolucion de un auto rentado.

    Lista los autos que el usuario tiene rentados, pide cual devolver y, al
    confirmar:
        - marca el auto como disponible otra vez en `autos.json`;
        - quita la patente de `autos_rentados` del usuario en `usuarios.json`.

    Args:
        usu_info (list): [dni, nombre, autos_rentados] del usuario logueado.
        lista_usu (dict): Todos los usuarios (para guardar la devolucion).
        lista_aut (dict): Catalogo de autos (no se usa por ahora).

    NOTA (docstring actualizado): el texto anterior decia que estaba incompleto;
    esta version ya devuelve el auto.
    """
    limpiar()
    # TODO(TP - Req 1): manejar excepciones al cargar.
    #en desarrollo
    while True:
        limpiar()
        print(f"--- Autos rentados --- [{usu_info[1]}]\n")
        for i, j in enumerate(lista_usu[usu_info[0]]["autos_rentados"]):
            print(f"\n[{i+1}]:Patente[{j}]\n")
        print("-------------------------")
        print("[0] Para salir a Modelos")

        try: opcion4 : str = input("\nSeleccione una patente: ").strip()
        except: opcion4 : str = ""
        
        if opcion4 == '0':
            # Volver al nivel de modelos.
            break
        elif opcion4 not in list(map(str, list(range(1, len(lista_usu[usu_info[0]]["autos_rentados"])+1)))):
            # Validacion: la opcion debe corresponder a una patente mostrada.
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass
        else:
            # --- Confirmacion y registro del alquiler ---
            limpiar()
            # Se obtiene la patente elegida de la lista de autos rentados.
            patente_elegida = lista_usu[usu_info[0]]["autos_rentados"][int(opcion4)-1]
            # Marca el auto como disponible otra vez en autos.json.
            cd.modificar_estado_auto(patente_elegida, False)
            # Quita la patente de la lista de autos rentados del usuario.
            lista_usu[usu_info[0]]["autos_rentados"].pop(int(opcion4)-1)
            # Persiste los usuarios (sin ese auto rentado).
            cd.escribir_usuario(lista_usu)
            print(f"\n¡Auto con patente: {patente_elegida} DEVUELTO!")
            try: input("[Enter] ")
            except: pass
            # Salir del bucle de patentes tras alquilar.
            return 

# Muestra autos disponibles aplicando filtros por categoria/modelo.
# NOTA (funcion incompleta / placeholder): el cuerpo es solo un print de prueba
# ("sdsdsd"); falta implementar el informe real. El texto "(contexto global:
# lista, opcion, opcion2)" del comentario original quedo de una version vieja.
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
    # TODO(TP - Req 8): implementar el informe de disponibilidad real.
    limpiar()
    cd.ver_stock(1,0)

def estado_rentas():
    """
    Muestra el estado de los autos rentados.

    NOTA (funcion incompleta / placeholder): por ahora solo imprime "hola";
    falta implementar el listado de autos alquilados.

    Returns:
        None
    """
    # TODO(TP - Req 8): recorrer los autos rentados y mostrar su ficha.
    limpiar()
    cd.ver_stock(0,1)

def informe_estadisticas():
    """
    Muestra estadisticas del catalogo de autos.

    NOTA (funcion incompleta / placeholder): por ahora solo imprime "hola";
    falta implementarla (Req 8 del TP: reporte matricial).

    Returns:
        None
    """
    # TODO(TP - Req 8): calcular y mostrar las estadisticas.
    print("hola")

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
    # Carga en memoria los usuarios y el catalogo de autos (se usan durante
    # todo el submenu: alquilar y devolver).
    lista_usu = cd.open_usuarios()
    lista_aut = cd.open_autos()

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
                usu_info = us.ingresa_usuario(lista_usu)
                # NOTA (linea sin efecto): "if not usu_info: usu_info" no hace
                # nada; el "else" corta el bucle cuando el ingreso fue valido.
                if not usu_info: usu_info
                else: break
            elif opcion == "2":
                # NOTA (posible error): se recarga el archivo en 'usu_info'
                # (nombre confuso) y NO se actualiza 'lista_usu' en memoria; el
                # registro igual se guarda porque registro_usuario escribe en disco.
                usu_info = cd.open_usuarios()
                us.registro_usuario(usu_info)
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
        print(f"  [{usu_info[1]}]\n")
        print("[1] Rentar auto.")
        print("[2] Devolver auto.")
        print("-------------------------")
        print("[0] Volver al menú principal")

        try: 
            opcion : str = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                rentar_auto(usu_info, lista_usu, lista_aut)
            elif opcion == "2":
                devolver_auto(usu_info, lista_usu, lista_aut)
            elif opcion == "0":
                # Volver al menu principal.
                break
            else:
                print("\nOpción no válida. Intente de nuevo.")
                try: input("[Enter] ")
                except: pass
        except: 
            opcion : str = ""

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
