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
            dicc = {
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
                    print(" --- Modelos disponibles ---")
                    filtrados = {str(i+1): j.capitalize() for i ,j in enumerate(list({lista[i]["modelo"] for i in lista if lista[i]["categoria"] == dicc[res]}))}
                    [print(i,j) for i, j in filtrados.items()]
                    res1 = input("Seleccione el modelo que desea: ")
                    if res1 == '0':
                            break
                    elif res1 not in filtrados.keys():
                        print("\nOpción no válida. Intente de nuevo.")
                        input("[Enter]")
                    else:
                        while True:
                            limpiar()
                            print(f"PATENTES seleccionadas para Modelo: {filtrados[res1]}")
                            [print(f"{i}, Calidad: {lista[i]['calidad']}, Año: {lista[i]['año']}, Precio: u$d {lista[i]['precio']:.1f} ") for i in lista if lista[i]["modelo"].capitalize() == filtrados[res1]]
                            
                            res2 = input("Seleccione el auto que desea: ")
                            if res1 == '0':
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