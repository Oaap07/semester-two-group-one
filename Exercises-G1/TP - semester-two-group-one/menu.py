import json
import precarga
import crud
'''
def generar_alumnos_json(
    ruta_archivo: str = "alumnos.json", cantidad_registros: int = 10
)
'''
RUTA_ARCHIVO = "alumnos.json"

# ==========================================
# FUNCIONES STUB (VACÍAS PARA DESARROLLAR)
# ==========================================

def agregar_alumno():
    """Opción 1: Agregar un nuevo alumno al archivo JSON"""
    pass

def modificar_estado_civil():
    crud.modificar_estado_civil()
    return

def modificar_estado_cursada():
    """Subopción 2.2: Cambiar el estado de cursada de un alumno"""
    pass

def modificar_notas():
    """Subopción 2.3: Cambiar la lista de notas de un alumno"""
    pass

def ver_alumno():
    """Opción 3: Mostrar los datos de un alumno por ID"""
    pass

def eliminar_alumno():
    """Opción 4: Eliminar un alumno por ID"""
    pass

def informe_promedio_curso():
    """Subopción 5.1: Calcular y mostrar el promedio general del curso"""
    pass

def informe_mejor_promedio():
    """Subopción 5.2: Encontrar y mostrar el alumno con el mejor promedio"""
    pass


# ==========================================
# MENÚS Y SUBMENÚS DE NAVEGACIÓN
# ==========================================

def submenu_modificar():
    while True:
        print("\n--- SUBMENÚ: MODIFICAR ALUMNO ---")
        print("1. Cambiar estado civil")
        print("2. Cambiar estado cursada")
        print("3. Cambiar notas")
        print("0. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            modificar_estado_civil()
        elif opcion == "2":
            modificar_estado_cursada()
        elif opcion == "3":
            modificar_notas()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")


def submenu_informes():
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
