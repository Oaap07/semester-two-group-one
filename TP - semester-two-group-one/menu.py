"""
Requisitos del Trabajo Practico (TPO - SPRINT) - Programacion I
Facultad de Ingenieria Informatica

Modulo: menu.py - Menu principal, alquileres y navegacion.
Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).
"""
# ------------------------------------------------------------------
# CUMPLIMIENTO DEL SPRINT - requisitos que aporta ESTE modulo:
#   Req 1 (excepciones especificas) ....... PARCIAL (sobran except genericos)
#   Req 4 (tuplas / conjuntos) ............ CUMPLIDO (sets en rentar_auto)
#   Req 5 (listas por comprension) ........ CUMPLIDO (filtros de modelos y patentes)
#   Req 7 (menu con CRUD completo) ........ CUMPLIDO (menu_principal y submenus)
#   Req 8 (reporte matricial) ............. PARCIAL (falta informe_estadisticas)
# Los trabajos pendientes estan marcados en el codigo como "TODO(TP - Req N)" y las mejoras sugeridas como
# "RECOMENDACION (Req N)".
# ------------------------------------------------------------------

# NOTA (imports sin uso): 'json' y 'informe as inf' no se usan en este modulo
# (se podrian quitar). 'os' si se usa en limpiar().
# RECOMENDACION: quitar 'json' e 'informe as inf' (imports sin uso) al cerrar el sprint.
import crud as cd
import usuarios as us
import informe as inf
from pathlib import Path


# Mapeo de la opcion de menu a la categoria interna usada en autos.json.
categ_preset = {
    "1": "sedan_hatchback",
    "2": "suv_crossover",
    "3": "pickup",
    "4": "monovolumen_mpv"
}



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
        cd.limpiar()
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
                cd.limpiar()
                print(f"--- Modelos disponibles --- [{usu_info[1]}]\n")

                # Filtra modelos unicos disponibles de la categoria elegida. Se considera "disponible" si pertenece a la
                # categoria y su patente NO esta en 'rentados'. Es una lista por comprension que alimenta un conjunto
                # (set) para eliminar duplicados.
                # TODO(TP - Req 5): esta comprension es un uso valido del requisito.
                # BUG (KeyError): si un auto no tiene la clave "estado" (por ejemplo, uno dado de alta con
                # `agregar_auto`) o "categoria", esta comprension lanza KeyError. Ademas, si 'lista_aut' es None, lanza
                # TypeError.
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
                            cd.limpiar()
                            print(f"--- PATENTES con Modelo: {filtrados[opcion2]}---  [{usu_info[1]}]")

                            # Lista por comprension: patentes de ese modelo que todavia no estan rentadas.
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
                                cd.limpiar()
                                # El usuario eligio un numero; se obtiene la patente.
                                patente_elegida = patentes[int(opcion3)-1]
                                # Marca el auto como no disponible (rentado) en autos.json.
                                cd.modificar_estado_auto(patente_elegida, True)
                                # Agrega la patente a los autos rentados del usuario
                                # (usu_info[0] es el DNI, que es la clave en lista_usu).
                                lista_usu[usu_info[0]]["autos_rentados"].append(patente_elegida)
                                # NOTA (bug "renta infinita" - RESUELTO): antes 'lista_aut'
                                # quedaba desactualizado en memoria y el auto se podia
                                # volver a rentar en la misma sesion. Ahora submenu_usuario
                                # recarga el catalogo desde disco (cd.open_autos()) antes de
                                # cada operacion, por lo que el cambio ya se refleja.
                                # Persiste los usuarios (con el nuevo alquiler).
                                cd.escribir_usuario(lista_usu)
                                # Salir del bucle de patentes tras alquilar.
                                return 
                    # RESUELTO (Req 1): en lugar de 'except Exception' se capturan las excepciones esperadas del
                    # bloque (KeyError, IndexError, TypeError, ValueError).
                    except (KeyError, IndexError, TypeError, ValueError) as e: input(e)

def devolver_auto(usu_info, lista_usu):
    """
    Interfaz para registrar la devolucion de un auto rentado.

    Lista los autos que el usuario tiene rentados, pide cual devolver y, al
    confirmar:
        - marca el auto como disponible otra vez en `autos.json`;
        - quita la patente de `autos_rentados` del usuario en `usuarios.json`.

    Args:
        usu_info (list): [dni, nombre, autos_rentados] del usuario logueado.
        lista_usu (dict): Todos los usuarios (para guardar la devolucion).

    NOTA: la version anterior tambien recibia 'lista_aut' (el
    catalogo), pero ya no se usa porque el estado se cambia directo en el archivo.
    submenu_usuario ya la llama con los 2 argumentos correctos.

    NOTA (docstring actualizado): el texto anterior decia que estaba incompleto;
    esta version ya devuelve el auto.
    """
    cd.limpiar()
    # RESUELTO (Req 1): el guardado se delega en cd.escribir_usuario(), que ya maneja las excepciones (OSError).
    while True:
        cd.limpiar()
        print(f"--- Autos rentados --- [{usu_info[1]}]\n")
        # BUG (KeyError): si el DNI ('usu_info[0]') no esta en 'lista_usu', o al usuario le falta la clave
        # "autos_rentados", este acceso lanza KeyError.
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
            # --- Confirmacion y registro de la devolucion ---
            cd.limpiar()
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
            # Salir del bucle de patentes tras devolver.
            return 

# Muestra la disponibilidad de unidades (informe para la empresa).
# NOTA (implementado): ahora delega en cd.ver_stock(1, 0), que arma con pandas
# el catalogo completo. El texto viejo sobre "(contexto global: lista, opcion,
# opcion2)" ya no aplica.
def informe_disponibilidad():
    """
    Muestra la disponibilidad de unidades.

    Reutiliza `cd.ver_stock(1, 0)`, que arma con pandas el catalogo completo
    como tabla (Req 8 del TP: reporte matricial).

    Returns:
        None
    """
    # Limpia la pantalla y delega en el CRUD para mostrar el catalogo.
    cd.limpiar()
    cd.ver_stock(1,0)

def estado_rentas():
    """
    Muestra el estado de los autos rentados.

    Reutiliza `cd.ver_stock(0, 1)`, que arma con pandas el listado de los autos
    no disponibles (rentados).

    Returns:
        None
    """
    # Limpia la pantalla y delega en el CRUD para mostrar solo los rentados.
    cd.limpiar()
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
    # RECOMENDACION (Req 8): armar la matriz con pandas igual que en ver_stock, por ejemplo un DataFrame con filas =
    # categoria y columnas = cantidad de autos disponibles y rentados, impreso con .T (reporte matricial).
    print("hola")

def menu_principal():   
    """
    Menu principal del sistema.

    Permite acceder al submenu de usuario o al submenu de empresa.
    El bucle termina cuando se selecciona [0] Salir.
    """
    
    while True:
        cd.limpiar()
        print("--- MENÚ PRINCIPAL ---\n")
        print("[1] Menu de usuario.")
        print("[2] Menu de empresa.")
        print("-------------------------")
        print("[0] Salir.")
        
        # RESUELTO (Req 1): se captura solo EOFError al leer la opcion (en lugar de un 'except' generico que tragaba
        # cualquier fallo); el despacho quedo fuera del try para no ocultar errores de los submenus.
        try:
            opcion : str = input("\nSeleccione una opción: ").strip()
        except EOFError:
            break
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
            except EOFError: pass

def submenu_usuario():
    """
    Submenu destinado al usuario final.

    Ofrece acciones de alquiler: ingresar, registrarse, rentar auto o devolver auto.
    Permite volver al menu principal con [0].
    """
    # NOTA (cambio): antes se cargaban 'lista_usu' y 'lista_aut' una sola vez al
    # entrar al submenu. Ahora se recargan desde disco antes de cada accion
    # (Ingresar, Registrarse, Rentar, Devolver) para reflejar los cambios: esto es
    # lo que resolvio los bugs "error al ingresar" y "renta infinita".
    while True:
        cd.limpiar()
        print("--- SUBMENÚ: USUARIOS ---\n")
        print("[1] Ingresar")
        print("[2] Registrarse")
        print("-------------------------")
        print("[0] Volver al menú principal")
        # RESUELTO (Req 1): se captura solo EOFError al leer la opcion (en lugar de un 'except' generico que ocultaba
        # los errores). Ademas, open_usuarios() ya no devuelve None, asi ingresa_usuario() no recibe None y desaparece
        # el bucle de "[ERROR] Intente de nuevo.".
        try:
            opcion : str = input("\nSeleccione una opción: ").strip()
        except EOFError:
            break

        if opcion == "1":
            lista_usu = cd.open_usuarios()
            usu_info = us.ingresa_usuario(lista_usu)
            # NOTA (linea sin efecto): "if not usu_info: usu_info" no hace
            # nada; el "else" corta el bucle cuando el ingreso fue valido.
            if not usu_info: usu_info
            else: break
        elif opcion == "2":
            # NOTA (bug "error al ingresar" - RESUELTO): antes NO se recargaba
            # 'lista_usu' tras registrarse y el usuario nuevo no podia ingresar
            # hasta reiniciar. Ahora se relee el archivo, igual que en [1].
            lista_usu = cd.open_usuarios()
            # NOTA (nombre confuso): 'usu_info' aca NO es el usuario logueado,
            # sino el diccionario completo de usuarios que necesita
            # registro_usuario(). Conviene renombrarlo (por ejemplo 'usuarios').
            usu_info = cd.open_usuarios()
            us.registro_usuario(usu_info)
        elif opcion == "0":
            return
        else:
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except EOFError: pass


    

    while True:
        cd.limpiar()
        print("--- |USUARIOS| MENÚ: MANEJO DE AUTOS ---", end="")
        print(f"  [{usu_info[1]}]\n")
        print("[1] Rentar auto.")
        print("[2] Devolver auto.")
        print("-------------------------")
        print("[0] Volver al menú principal")

        # RESUELTO (Req 1): se captura solo EOFError al leer la opcion; antes el 'except' generico tragaba los errores
        # de rentar_auto() / devolver_auto().
        try:
            opcion : str = input("\nSeleccione una opción: ").strip()
        except EOFError:
            break

        if opcion == "1":
            lista_aut = cd.open_autos()
            rentar_auto(usu_info, lista_usu, lista_aut)
        elif opcion == "2":
            devolver_auto(usu_info, lista_usu)
        elif opcion == "0":
            # Volver al menu principal.
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except EOFError: pass

def submenu_empresa():
    """
    Submenu destinado a la empresa (gestion e informes).

    Llama a las funciones de informe definidas en ESTE modulo:
    - informe_disponibilidad(): catalogo completo (via cd.ver_stock(1,0)).
    - informe_estadisticas(): SIGUE PENDIENTE (stub, imprime "hola").
    - estado_rentas(): solo autos rentados (via cd.ver_stock(0,1)).
    Permite volver al menu principal con [0].

    Importante (Req 8 del TP): los informes usan pandas (DataFrame) para generar
    el reporte matricial.
    """
    while True:
        cd.limpiar()
        print("--- SUBMENÚ: INFORMES ---\n")
        print("[1] Disponibilidad de unidades")
        print("[2] Estadisticas del mes")
        print("[3] Estado de autos rentados")
        print("[0] Volver al menú principal")

        try: opcion : str = input("\nSeleccione una opción: ").strip()
        except: opcion : str = ""

        if opcion == "1":
            # Disponibilidad: ya arma un reporte matricial con pandas (Req 8).
            informe_disponibilidad()
        elif opcion == "2":
            # NOTA (pendiente): informe_estadisticas() sigue siendo un stub
            # (imprime "hola"); falta el reporte matricial (Req 8).
            informe_estadisticas()
        elif opcion == "3":
            # Estado de los autos rentados: usa pandas (Req 8).
            estado_rentas()
        elif opcion == "0":
            # Volver al menu principal.
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass

if __name__ == "__main__":
    cd.limpiar()
    ruta_archivo1 = "usuarios.json"
    ruta_archivo2 = "autos.json"
    archivo1 = Path(ruta_archivo1)
    archivo2 = Path(ruta_archivo2)
    if archivo1.is_file():
        print("Es un archivo usuarios ya existente.")
    else:
        inf.informe_usuarios(archivo1)
    if archivo2.is_file():
        print("Es un archivo autos ya existente.")
    else:
        inf.informe_autos(archivo2, 25)
    menu_principal()
    cd.limpiar()
