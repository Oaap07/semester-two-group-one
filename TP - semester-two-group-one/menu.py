import informe
import json
import os

# ==========================================
# FUNCIONES STUB (VACÍAS PARA DESARROLLAR)
# ==========================================

def limpiar(): os.system('cls' if os.name == 'nt' else 'clear') #  Limpia la terminal

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
                    filtrados = {str(i+1): j.capitalize() for i ,j in enumerate(list({lista[i]["modelo"] for i in lista if lista[i]["categoria"] == categ_preset[res]}))}
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
                            patentes = [i for i in lista if lista[i]["modelo"].capitalize() == filtrados[res1]]
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
                                print(f"\n¡Auto con patente: {patentes[int(res2)-1]} RENTADO!")
                                input("\n[Enter]")
                                break
                        break
                break
                    
def devolver_auto():
    limpiar()
    pass

# ==========================================
# MENÚS Y SUBMENÚS DE NAVEGACIÓN
# ==========================================


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
        print("[1] Promedio del curso")
        print("[2] Alumno con mejor promedio")
        print("[0] Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            informe_promedio_curso()
        elif opcion == "2":
            informe_mejor_promedio()
        elif opcion == "0":
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")

if __name__ == "__main__":
    informe.informe_autos("autos.json", 25)
    limpiar()
    menu_principal()
    limpiar()