"""
Requisitos del Trabajo Practico (TPO - SPRINT) - Programacion I
Facultad de Ingenieria Informatica

Modulo: menu.py - Menu principal, alquileres y navegacion.
Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).

Es el PROGRAMA PRINCIPAL del sistema:
- menu_principal() ........ entrada: deriva al submenu de usuario o de empresa.
- submenu_usuario() ....... ingreso/registro y luego alquilar/devolver.
- submenu_empresa() ....... informes sobre el catalogo.
- rentar_auto() / devolver_auto() .... flujo de alquiler (tres niveles:
    categoria -> modelo -> patente).
- ver_catalogo() / informe_disponibilidad() / estado_rentas() .... tablas con
    pandas, delegan en crud.ver_stock().
- informe_estadisticas() ... estadisticas generales del catalogo.

Se apoya en crud.py (lee y modifica autos.json) y usuarios.py (login/registro).
Los modelos y las patentes se filtran con listas y conjuntos por comprension
(Requisito 5).
"""

import crud as cd
import usuarios as us
import informe as inf
import matplotlib.pyplot as plt
from pathlib import Path



# Mapeo de la opcion de menu a la categoria interna usada en autos.json.
categ_preset = {
    "1": "sedan_hatchback",
    "2": "suv_crossover",
    "3": "pickup",
    "4": "monovolumen_mpv"
}



def rentar_auto(usu_info, lista_usu, lista_aut, pozo):
    """
    Flujo completo para alquilar un auto disponible.

    El flujo esta anidado en tres niveles con bucles while, para poder volver al
    nivel anterior (Categorias -> Modelos -> Patentes):

        Nivel 1 - categoria: una de las cuatro categorias (ver `categ_preset`).
        Nivel 2 - modelo: los modelos disponibles de esa categoria; se guardan
            en un conjunto (set) para no repetirlos.
        Nivel 3 - patente: las patentes disponibles de ese modelo y confirmacion.

    Al confirmar:
    - agrega la patente a `autos_rentados` del usuario en `usuarios.json`;
    - marca el auto como no disponible (rentado) en `autos.json`;
    - acumula en `pozo` (de informe.py) los dias por el precio diario.

    Args:
        usu_info (list): [dni, nombre, autos_rentados] del usuario logueado.
        lista_usu (dict): Todos los usuarios (para guardar el alquiler).
        lista_aut (dict): Catalogo de autos (para filtrar los disponibles).
        pozo (float): Recaudacion acumulada de alquileres del sistema.

    Returns:
        float | None: `pozo` actualizado al concretar el alquiler; o None si el
        usuario cancela con [0].

    Notas (Req 5 del TP):
        Los modelos y las patentes se filtran con listas por comprension y se
        guardan en conjuntos (set) para quitar los duplicados.
    """
    # Se relee el archivo para trabajar siempre sobre los datos mas recientes.
    cd.open_usuarios()
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

                # Comprension (Req 5): conjunto de modelos de la categoria elegida cuyo
                # estado es disponible (True). El set quita los modelos repetidos y el dict
                # final los numera ("1", "2", ...) para que el usuario los elija.
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

                            # Comprension (Req 5): patentes de ese modelo que siguen disponibles.
                            # Se normaliza con capitalize() para que no importe como este
                            # escrito el modelo en el JSON.
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
                                # Se registra la patente elegida en los autos rentados del
                                # usuario y se muestra el detalle de la renta.
                                patente_elegida = patentes[int(opcion3)-1]
                                precio_unitario = lista_aut[patente_elegida]["precio"]
                                lista_usu[usu_info[0]]["autos_rentados"].append(patente_elegida)
                                print('--- DETALLE DE LA RENTA ---')
                                print(f'vehiculo: {lista_aut[patente_elegida]["marca"]} {lista_aut[patente_elegida]["modelo"]} (patente: {patente_elegida})')
                                print(f'Precio diario: u$d {precio_unitario:.1f}')

                                # Bucle de validacion: los dias deben ser un entero mayor a 0.
                                while True:
                                    try:
                                        dias = int(input("Ingrese cuantos dias desea rentar su auto : "))
                                        if dias > 0:
                                            break
                                        print('La cantidad debe ser mayor a 0 ')
                                    except ValueError:
                                        print('Por favor, ingrese un numero entero valido')
                                inf.pozo += dias * precio_unitario

                                # Persiste el alquiler en usuarios.json y marca el auto como
                                # no disponible en autos.json.
                                cd.escribir_usuario(lista_usu)
                                cd.modificar_estado_auto(patente_elegida, True)
                                return pozo
                    except (KeyError, IndexError, TypeError, ValueError) as e: input(e)

def devolver_auto(usu_info, lista_usu):
    """
    Interfaz para registrar la devolucion de un auto rentado.

    Lista las patentes que el usuario tiene rentadas, pide cual devolver y, al
    confirmar:
        - marca el auto como disponible otra vez en `autos.json`;
        - quita la patente de `autos_rentados` del usuario en `usuarios.json`.

    Args:
        usu_info (list): [dni, nombre, autos_rentados] del usuario logueado.
        lista_usu (dict): Todos los usuarios (para guardar la devolucion).

    Returns:
        None: al devolver un auto corta con return; con [0] vuelve al submenu.
    """
    cd.limpiar()
    # El guardado se delega en cd.escribir_usuario(), que ya maneja el OSError.
    while True:
        cd.limpiar()
        print(f"--- Autos rentados --- [{usu_info[1]}]\n")
        # Se numeran (1, 2, ...) las patentes que el usuario tiene rentadas.
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
            # Persiste los usuarios (ya sin ese auto rentado).
            cd.escribir_usuario(lista_usu)
            print(f"\n¡Auto con patente: {patente_elegida} DEVUELTO!")
            try: input("[Enter] ")
            except: pass
            # Salir del bucle de patentes tras devolver.
            return 

def ver_catalogo():
    """
    Muestra el catalogo completo de autos como tabla.

    Delega en `cd.ver_stock(1, 0)`, que arma con pandas el catalogo completo
    (Req 8 del TP: reporte matricial).

    Returns:
        None
    """
    cd.limpiar()
    cd.ver_stock(1,0)

def informe_disponibilidad():
    """
    Muestra solo los autos disponibles como tabla.

    Delega en `cd.ver_stock(1, 1)`, que arma con pandas el listado filtrado de
    los autos que no estan rentados (Req 8 del TP: reporte matricial).

    Returns:
        None
    """
    cd.limpiar()
    cd.ver_stock(1,1)

def estado_rentas():
    """
    Muestra solo los autos rentados como tabla.

    Delega en `cd.ver_stock(0, 1)`, que arma con pandas el listado de los autos
    no disponibles (Req 8 del TP: reporte matricial).

    Returns:
        None
    """
    cd.limpiar()
    cd.ver_stock(0,1)

def informe_estadisticas():
    """
    Muestra estadisticas del catalogo de autos.
    """
    cd.limpiar()
    datos : dict = cd._cargar_autos()
    autos_excel_modificado = (cd.pd.DataFrame(datos)).T
    
    midf_true = autos_excel_modificado[autos_excel_modificado["estado"] == True].groupby(autos_excel_modificado["marca"]).size()
    lista_estados_totales = autos_excel_modificado["estado"].value_counts()

    colores_barras = [
    "#4D96FF",
    "#FF6B6B",
    "#6BCB77",
    "#FFD93D",
    "#9B51E0",
    "#FF9F45",
    "#2EC4B6",
    ]      

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.bar(midf_true.index.str.capitalize(), 
            midf_true.values,
            color=colores_barras,)
    ax1.set_title("Autos disponibles (por marcas)", 
                fontsize=16,
                fontweight="bold",
                loc="center",
                )
    
    ax2.pie(lista_estados_totales, 
            # labels="Disponibles" for i in lista_estados_totales if i == True else "Ocupados",
            autopct="%0.1f%%",
            colors=["#6BCB77","#FF6B6B"],
            textprops={"fontsize": 20,
            "fontfamily": "sans-serif",},)
    ax2.set_title("Autos disponibles y rentados", 
                fontsize=16,
                fontweight="bold",
                loc="center",
                )
    
    plt.tight_layout()
    plt.show()
    
    input("Enter para salir: ")

def menu_principal():
    """
    Menu principal del sistema.

    Permite entrar al submenu de usuario (alquileres) o al de empresa (informes).
    El bucle termina al elegir [0] Salir o al cortarse la entrada (EOFError).

    Returns:
        None
    """
    while True:
        cd.limpiar()
        print("--- MENÚ PRINCIPAL ---\n")
        print("[1] Menu de usuario.")
        print("[2] Menu de empresa.")
        print("-------------------------")
        print("[0] Salir.")
        
        # Solo se captura EOFError al leer la opcion; el despacho queda fuera del
        # try para no ocultar los errores de los submenus.
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

    Primero el ingreso o registro; una vez identificado, permite alquilar y
    devolver autos. Permite volver al menu principal con [0].

    Las listas `lista_usu` y `lista_aut` se recargan desde disco antes de cada
    accion para trabajar siempre con los datos actualizados del archivo.

    Returns:
        None
    """
    while True:
        cd.limpiar()
        print("--- SUBMENÚ: USUARIOS ---\n")
        print("[1] Ingresar")
        print("[2] Registrarse")
        print("-------------------------")
        print("[0] Volver al menú principal")
        # Solo se captura EOFError al leer la opcion. open_usuarios() devuelve
        # siempre un diccionario (nunca None), asi que el ingreso no recibe None.
        try:
            opcion : str = input("\nSeleccione una opción: ").strip()
        except EOFError:
            break

        if opcion == "1":
            # Se relee usuarios.json y se pasa la sesion a ingresa_usuario().
            lista_usu = cd.open_usuarios()
            usu_info = us.ingresa_usuario(lista_usu)
            # Si el ingreso fue valido (usu_info no vacio) se sale al submenu de
            # autos; si no, se vuelve a pedir la opcion.
            if not usu_info: usu_info
            else: break
        elif opcion == "2":
            # Se relee el archivo para que el usuario recien registrado quede
            # disponible de inmediato (sin reiniciar el programa).
            lista_usu = cd.open_usuarios()
            usu_info = cd.open_usuarios()
            us.registro_usuario(usu_info)
        elif opcion == "0":
            return
        else:
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except EOFError: pass


    

    # Submenu de autos (ya con el usuario identificado en usu_info).
    while True:
        cd.limpiar()
        print("--- |USUARIOS| MENÚ: MANEJO DE AUTOS ---", end="")
        print(f"  [{usu_info[1]}]\n")
        print("[1] Rentar auto.")
        print("[2] Devolver auto.")
        print("-------------------------")
        print("[0] Volver al menú principal")

        # Solo se captura EOFError al leer la opcion, para no ocultar los errores
        # que puedan lanzar rentar_auto() / devolver_auto().
        try:
            opcion : str = input("\nSeleccione una opción: ").strip()
        except EOFError:
            break

        if opcion == "1":
            lista_aut = cd.open_autos()
            # Se pasa el pozo (recaudacion acumulada) que vive en informe.py.
            rentar_auto(usu_info, lista_usu, lista_aut, inf.pozo)
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
    Submenu destinado a la empresa (informes del catalogo).

    Llama a las funciones de informe de ESTE modulo:
        [1] ver_catalogo() ............. catalogo completo (cd.ver_stock(1,0)).
        [2] informe_disponibilidad() ... solo disponibles (cd.ver_stock(1,1)).
        [3] estado_rentas() ............ solo rentados (cd.ver_stock(0,1)).
        [4] informe_estadisticas() ..... resumen estadistico.

    Las tablas se arman con pandas (DataFrame), que es el reporte matricial del
    Req 8. Permite volver al menu principal con [0].

    Returns:
        None
    """
    while True:
        cd.limpiar()
        print("--- SUBMENÚ: INFORMES ---\n")
        print("[1] Ver STOCK completo")
        print("[2] Autos Disponibles")
        print("[3] Autos rentados")
        print("[4] Estadísticas generales")
        print("-------------------------------")
        print("[0] Volver al menú principal")

        try: opcion : str = input("\nSeleccione una opción: ").strip()
        except: opcion : str = ""

        if opcion == "1":
            # Catalogo completo: tabla con pandas (Req 8).
            ver_catalogo()
        elif opcion == "2":
            # Solo disponibles: tabla con pandas (Req 8).
            informe_disponibilidad()
        elif opcion == "3":
            # Solo rentados: tabla con pandas (Req 8).
            estado_rentas()
        elif opcion == "4":
            # Estadisticas generales del catalogo.
            informe_estadisticas()
        elif opcion == "0":
            # Volver al menu principal.
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
            try: input("[Enter] ")
            except: pass

if __name__ == "__main__":
    # Punto de entrada: si faltan los archivos de datos, los precarga; luego abre
    # el menu principal.
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