"""
Un centro de salud necesita un sistema en consola para gestionar
el turno de atención de los pacientes a medida que van arribando a la
sala de espera. Deberemos implementar una estructura de datos de tipo
Cola (Queue) simulado con listas para gestionar la recepción y atención
de pacientes siguiendo un orden estrictamente secuencial (Primero en
Llegar, Primero en Ser Atendido). Trabajaremos con tres listas
sincronizadas, cada posición es un paciente único. La primer lista
almacena el dni, la segunda el primer nombre y la tercera el apellido.

En el programa debemos generar tres funciones: mostrar_lista_espera (la
cual nos muestra los pacientes en sala de espera pendientes en el orden 
en que serán atendidos), cargar_paciente (cargamos un paciente al final
de la cola) y atender_paciente (se anuncia el paciente que será atendido
y se lo elimina de la lista).Importante: si no hay pacientes, no podemos
eliminar de la lista, por lo que debemos validar que haya pacientes para
que no interrumpa el programa.
"""
def Cargar_Paciente(Db_Pacientes):
    Ingresar_DNI = input("Ingrese el DNI del paciente EJEMPLO:[xxxxxxx]: ")
    
    # Comprobar si el DNI ya existe en la lista de pacientes
    for paciente in Db_Pacientes:
        if paciente[0] == Ingresar_DNI:
            print("---------------------------")
            print("DNI ya registrado")
            print("---------------------------")
            return Db_Pacientes  # Cancela la carga sin modificar la lista

    nombre = input("Ingrese el Nombre del paciente: ")
    apellido = input("Ingrese el Apellido del paciente: ")

    Nuevo_Paciente = [Ingresar_DNI, nombre, apellido]
    Db_Pacientes.append(Nuevo_Paciente)

    return Db_Pacientes

def Mostrar_Paciente_espera(Db_Pacientes):
    
    contador_de_turnos = 0
    
    print("---------------------------")
    print("Mostrando Pacientes...")
    print("---------------------------")
    for Paciente in Db_Pacientes:
        contador_de_turnos += 1
        print(f""" Turno:{(contador_de_turnos)}
            DNI: {Paciente[0]} | Nombre: {Paciente[1]} | Apellido: {Paciente[2]}""")
        
        print()

def Atender_paciente(Db_Pacientes):
    
    print("---------------------------")
    print("Atendiendo Paciente...")
    print("---------------------------")
    print(f"DNI: {Db_Pacientes[0][0]} | Nombre: {Db_Pacientes[0][1]} | Apellido: {Db_Pacientes[0][2]}")
    Db_Pacientes.pop(0)
    print()

Db_Pacientes = []
aux = True

while aux:
    print()
    print("---------------------------")
    print("Menu De Administracion")
    print("---------------------------")
    print("""Opciones:
        [0]:Cerrar
        [1]:Agregar un paciente
        [2]:Mostrar lista de espera
        [3]:Atender paciente
        """)
    Opccion = input("Elección: ")

    if Opccion == "0":aux = False
    elif Opccion == "1": Cargar_Paciente(Db_Pacientes)
    elif Opccion == "2": Mostrar_Paciente_espera(Db_Pacientes)
    elif Opccion == "3": Atender_paciente(Db_Pacientes)