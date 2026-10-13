import informe
import json
import os


'''
def generar_alumnos_json(
    ruta_archivo: str = "alumnos.json", cantidad_registros: int = 10
)
'''
RUTA_ARCHIVO = "alumnos.json"

# ==========================================
# FUNCIONES STUB (VACÍAS PARA DESARROLLAR)
# ==========================================

def limpiar(): os.system('cls' if os.name == 'nt' else 'clear') #  Limpia la terminal

def rentar_auto():
    limpiar()
    categorías = {
        '1' : {"sedan_hatchback" : ["etios", "yaris", "corolla", "clio", "sandero", 
                             "argo", "cronos", "206", "208", "408", "onix", "cruze"]},
        '2' : {"suv_crossover" : ["rav4", "kardian", "duster", "pulse",
                           "fastback", "2008", "3008", "tracker"]},
        '3' : {"pickup" : ["hilux", "toro", "montana"]},

        '4' : {"monovolumen_mpv" : ["kangoo", "spin"]}
    }

    with open("autos.json", 'r', encoding="utf-8") as archivo:
        lista = json.load(archivo)

        while True:
            limpiar()
            res = input(" --- Escoja una categoría ---\n"
                            "[1] Sedán / Hatchback\n"
                            "[2] SUV / Crossover\n"
                            "[3] Pick-up\n"
                            "[4] Monovolumen / Utilitario (MPV)\n"
                            "-------------------------\n"
                            "[0] Para ir a Sub menú\n"
                            "Seleccione una opción: ")

            if res == '0':
                break
            elif res not in list(map(str, list(range(1,5)))):
                print("\nOpción no válida. Intente de nuevo.")
                input("[Enter]")
            else:
                while True:
                    limpiar()
                    print(" --- Modelos disponibles ---")
                    [print(f"{j}-", i[j].capitalize()) for i in (categorías[res].values()) for j in range(len(i))]
                    print("-------------------------\n"
                          "[0] Para ir a categorías")
                    res2 = input("Seleccione una opción: ")

                    if res2 == '0':
                        break
                    elif res2 not in list(map(str, list(range(len(list(categorías[res].values())[0]))))):
                        print(list(range(len(list(categorías[res].values())[0]))))
                        print("\nOpción no válida. Intente de nuevo.")
                        input("[Enter]")
                    else:
                        limpiar()
                        print(f"\n### Auto rentado!: '{(list(categorías[res].values()))[0][int(res2)].capitalize()}' ###\n")
                        input("[Enter]") #  TODO: En este else sólo se printea el mensaje, solucionar seguimiento del auto seleccionado y 
                                         #        printear con todos lo datos del auto seleccionado.
                                         

def devolver_auto():
    limpiar()
    pass

# ==========================================
# MENÚS Y SUBMENÚS DE NAVEGACIÓN
# ==========================================

def menu_principal():
    while True:
        limpiar()
        print("--- MENÚ PRINCIPAL ---")
        print("1. Menu de usuario.")
        print("2. Menu de empresa.")
        print("0. Salir.")
        opcion = input("Seleccione una opción: ").strip()
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
        print("--- SUBMENÚ: MANEJO DE AUTOS ---")
        print("1. Rentar auto.")
        print("2. Devolver auto.")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
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
        print("--- SUBMENÚ: INFORMES ---")
        print("1. Promedio del curso")
        print("2. Alumno con mejor promedio")
        print("0. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ").strip()
        
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