import informes
import precarga
import json
'''
def generar_alumnos_json(
    ruta_archivo: str = "alumnos.json", cantidad_registros: int = 10
)
'''
RUTA_ARCHIVO = "alumnos.json"

# ==========================================
# FUNCIONES STUB (VACÍAS PARA DESARROLLAR)
# ==========================================

def menu_principal():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
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
            print("Opción no válida. Intente de nuevo.")

def rentar_auto():
    with open("autos.json", 'r', encoding="utf-8") as archivo:
        lista = json.load(archivo)
        for i in lista.keys():
            dict = lista[i]
            for k, v in dict.items():
                print(f"[{lista[i]}]", )
                print(f"\t CALIDAD: {elemento["calidad"]} | AÑO: {elemento["año"]} | PRECIO: {elemento["precio"]}")

    

    



# ==========================================
# MENÚS Y SUBMENÚS DE NAVEGACIÓN
# ==========================================

def submenu_usuario():
    while True:
        print("\n--- SUBMENÚ: MODIFICAR ALUMNO ---")
        print("1. rentar auto.")
        print("2. devolver auto.")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            rentar_auto()
        elif opcion == "2":
            devolver_auto()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")


def submenu_empresa():
    while True:
        print("\n--- SUBMENÚ: INFORMES ---")
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
            print("Opción no válida. Intente de nuevo.")


def menu_principal():
    while True:
        print("\n" + "="*35)
        print("    SISTEMA DE RENTA DE AUTOS")
        print("="*35)
        print("1. Agregar alumno")
        print("2. Modificar alumno")
        print("3. Ver datos de un alumno")
        print("4. Eliminar un alumno")
        print("5. Informes")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            agregar_alumno()
        elif opcion == "2":
            submenu_modificar()
        elif opcion == "3":
            ver_alumno()
        elif opcion == "4":
            eliminar_alumno()
        elif opcion == "5":
            submenu_informes()
        elif opcion == "0":
            print("¡Gracias por utilizar el sistema!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    precarga.generar_alumnos_json("alumnos.json", 15)
    menu_principal()
