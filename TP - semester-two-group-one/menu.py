"""
Requisitos del Trabajo Practico (TPO - SPRINT) - Programacion I
Facultad de Ingenieria Informatica

Modulo: menu.py - Menu principal, alquileres y navegacion.
Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).
"""

import json, os
import informe as inf
import crud as cd

def limpiar():
    """
    Limpia la consola segun el sistema operativo.

    En Windows usa 'cls'; en Linux/macOS usa 'clear'. Sirve para mantener la
    interfaz ordenada entre pantallas del menu.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def ingresa_usuario(lista):
    """
    Interfaz para el ingreso de un usuario ya registrado.

    Args:
        lista (list): Diccionario con la información de todos los usuarios.
    
    Returns:
        tupla: Con el Nombre y Autos rentados del usuario
    """
    while True:
        limpiar()
        #  Manejo de excepciones en inputs.
        #  Se pide el DNI y la contraseña al usuario.
        print("--- REGISTRO: USUARIOS ---")
        print("[0] en cualquier campo para salir.\n")
        try: 

            dni_usu = int(input("Ingrese DNI de usuario: "))
            dni_usu = str(dni_usu)

            if len(dni_usu) != 8 and dni_usu != "0":
                print("\nDNI inválido, intente de nuevo")
                try: input("[Enter] ")
                except: pass
                return ()
            elif dni_usu not in lista and dni_usu != "0":
                print("\nUsuario inexistente, regístrese.")
                try: input("[Enter] ")
                except: pass  
                return ()
            
            clave_usu : str = input("Ingrese contraseña: ").lower()

            while True:
                if dni_usu in lista and clave_usu != lista[dni_usu]["clave"]:
                    clave_usu = input("Contraseña incorrecta, intente de nuevo: ").lower()
                elif clave_usu == "0": break
                elif clave_usu.strip() == "" : int(clave_usu)
                else: break
            break
        except:
            print()
            print("[ERROR] Intente de nuevo.")
            try: input("[Enter] ")
            except: pass
        
    #  Se retorna el Nombre y una lista con los autos que rentó
    if dni_usu in lista and clave_usu == lista[dni_usu]["clave"]:
        limpiar()
        print("=" * 20)
        print(f"Bienvenido/a {lista[dni_usu]["nombre"]}!")
        print("=" * 20)
        try: input("[Enter] ")
        except: pass
        return (lista[dni_usu]["nombre"], lista[dni_usu]["autos_rentados"])
    elif dni_usu == "0" or clave_usu == "0":
        return 

def registro_usuario(lista):
    """
    Interfaz para el registro de usuarios nuevos.

    Args:
        lista (list): Diccionario con la información de todos los usuarios.
    
    Returns:
        
    """
    while True:
        limpiar()
        #  Manejo de excepciones en inputs.
        #  Se pide el DNI y la contraseña al usuario.
        try: 
            print("--- REGISTRO: USUARIOS ---")
            print("[0] en cualquier campo para salir.\n")
            
            dni_usu = int(input("Ingrese su DNI: "))

            if len(dni_usu) != 9:
                print("\nDNI inválido, intente de nuevo.")
                try: input("[Enter] ")
                except: pass
                return ()
            elif dni_usu in lista:
                print("\nDNI ya existente, vaya a 'INGRESAR'")
                try: input("[Enter] ")
                except: pass   
                return ()

            nombre_usu : str = input("Ingrese su nombre: ")
            clave_usu : str = input("Ingrese una nueva contraseña: ").lower()
            
            if clave_usu == "0" or dni_usu == "0" or nombre_usu == "0": return ()
            while True:
                
                clave_usu2 : str = input("Comprueba contraseña: ").lower()
                
                if clave_usu == clave_usu2: break
                elif clave_usu2 == "0": return ()
                else: limpiar(), print("| Clave incorrecta, intente de nuevo |")
            break

        except:
            print()
            print("[ERROR] Intente de nuevo.")
            try: input("[Enter] ")
            except: pass    

    lista[str(dni_usu)] = {
        "nombre": nombre_usu,
        "clave": clave_usu,
        "autos_rentados": [],
    }
    
    with open(inf.RUTA_USUARIOS_JSON, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)
    print(f"||| ¡Usuario [{nombre_usu.capitalize()}] registrado exitosamente! |||")
    try: input("[Enter] ")
    except: pass  

    #  Se retorna el Nombre y una lista con los autos que rentó

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
                            cd.modificar_estado_auto(patente_elegida)
                            print(f"\n¡Auto con patente: {patente_elegida} RENTADO!")
                            try: input("[Enter] ")
                            except: pass
                            # Salir del bucle de patentes tras alquilar.
                            return 

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
    print("¿Que auto desea devolver?")
    print("="*15)
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
                usu_info : tuple = ingresa_usuario(lista)
                if not usu_info: usu_info
                else: break
            elif opcion == "2":
                registro_usuario(lista)
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
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass

if __name__ == "__main__":
    # Inicio de la aplicacion.
    # TODO(TP - Req 3): confirmar que autos.json tenga al menos 5 registros (precarga).
    limpiar()
    menu_principal()
    limpiar()