import informe
import json
import os

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_rentados():
    try:
        with open("rentados.json", 'r', encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}

def guardar_rentados(rentados):
    with open("rentados.json", 'w', encoding="utf-8") as archivo:
        json.dump(rentados, archivo, indent=4)

def rentar_auto():
    limpiar()
    
    with open("autos.json", 'r', encoding="utf-8") as archivo:
        lista = json.load(archivo)

    while True:
        limpiar()
        res = input(" --- Escoja una categoría ---\n\n"
                        "[1] Sedán / Hatchback\n"
                        "[2] SUV / Crossover\n"
                        "[3] Pick-up\n"
                        "[4] Monovolumen / Utilitario (MPV)\n"
                        "-------------------------\n"
                        "[0] Para ir a Sub menú\n"
                        "\nSeleccione una opción: ")
        categ_preset = {
            "1": "sedan_hatchback",
            "2": "suv_crossover",
            "3": "pickup",
            "4": "monovolumen_mpv"
        }
        if res == '0':
            break
        elif res not in list(map(str, list(range(1,5)))):
            print("\nOpción no válida. Intente de nuevo.")
            input("[Enter]")
        else:
            while True:
                limpiar()
                print("--- Modelos disponibles ---\n")
                
                rentados = cargar_rentados()
                
                filtrados = {str(i+1): j.capitalize() for i ,j in enumerate(list({lista[i]["modelo"] for i in lista if lista[i]["categoria"] == categ_preset[res] and i not in rentados}))}
                
                if not filtrados:
                    print("No hay autos disponibles en esta categoría.")
                    input("\n[Enter]")
                    break

                [print(f"[{i}] {j}") for i, j in filtrados.items()]
                print("-------------------------")
                print("[0] Para salir a Categorías")
                res1 = input("\nSeleccione el modelo que desea: ")
                if res1 == '0':
                        break
                elif res1 not in filtrados.keys():
                    print("\nOpción no válida. Intente de nuevo.")
                    input("[Enter]")
                else:
                    while True:
                        limpiar()
                        print(f"--- PATENTES con Modelo: {filtrados[res1]}---")
                        
                        patentes = [i for i in lista if lista[i]["modelo"].capitalize() == filtrados[res1] and i not in rentados]
                        
                        for i, j in enumerate(patentes):
                            print(f"\n[{i+1}]: {j}\n"
                                f"\tCalidad: {lista[j]['calidad']}\n"\
                                f"\tAño: {lista[j]['año']}\n"\
                                f"\tPrecio: u$d {lista[j]['precio']:.1f}")
                        print("-------------------------")
                        print("[0] Para salir a Modelos")
                        res2 = input("\nSeleccione el auto que desea: ")
                        if res2 == '0':
                            break
                        elif res2 not in list(map(str, list(range(1, len(patentes)+1)))):
                            print("\nOpción no válida. Intente de nuevo.")
                            input("\n[Enter]")
                        else:
                            limpiar()
                            patente_elegida = patentes[int(res2)-1]
                            print(f"\n¡Auto con patente: {patente_elegida} RENTADO!")
                            
                            rentados[patente_elegida] = lista[patente_elegida]
                            guardar_rentados(rentados)
                            
                            input("\n[Enter]")
                            break
                    break

def devolver_auto():
    limpiar()
    rentados = cargar_rentados()
    
    if not rentados:
        print("No hay autos rentados actualmente.")
        input("\n[Enter]")

    print("¿Que auto desea devolver?")
    print("="*15)
    input("\n[Enter]")

def estado_rentas():
    limpiar()
    rentados = cargar_rentados()
    print("--- ESTADO DE AUTOS RENTADOS ---\n")
    input("\n[Enter]")

def menu_principal():
    while True:
        limpiar()
        print("--- MENÚ PRINCIPAL ---\n")
        print("[1] Menu de usuario.")
        print("[2] Menu de empresa.")
        print("-------------------------")
        print("[0] Salir.")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":
            submenu_usuario()
        elif opcion == "2":
            submenu_empresa()
        elif opcion == "0":
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
            input("[Enter] ")

def submenu_usuario():
    while True:
        limpiar()
        print("--- SUBMENÚ: MANEJO DE AUTOS ---\n")
        print("[1] Rentar auto.")
        print("[2] Devolver auto.")
        print("-------------------------")
        print("[0] Volver al menú principal")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":
            rentar_auto()
        elif opcion == "2":
            devolver_auto()
        elif opcion == "0":
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")
            input("[Enter] ")

def submenu_empresa():
    while True:
        limpiar()
        print("--- SUBMENÚ: INFORMES ---\n")
        print("[1] Disponibilidad de unidades")
        print("[2] Estadisticas del mes")
        print("[3] Estado de autos rentados")
        print("[0] Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            informe.informe_disponibilidad()
        elif opcion == "2":
            informe.informe_estadisticas()
        elif opcion == "3":
            estado_rentas()
        elif opcion == "0":
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")

if __name__ == "__main__":
    try:
        informe.informe_autos("autos.json", 25)
    except:
        pass
    limpiar()
    menu_principal()
    limpiar()