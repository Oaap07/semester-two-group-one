"""
PROG_17: El centro de salud ha decidido implementar un protocolo de
atención rápida para pacientes prioritarios (embarazadas, personas con
movilidad reducida o adultos mayores). Al programa anterior, le haremos la
siguiente mejora: Al registrar un paciente, el sistema preguntará si se
trata de un caso Prioritario. Comportamiento en la cola:
    (dificultad intermedia)
    
        - Si la cola está vacía, el paciente prioritario ingresa normalmente.
        
        - Si ya hay personas esperando, el paciente prioritario se ubica
            inmediatamente en el segundo puesto de la cola (es decir, justo
            detrás de la persona que está a punto de ser llamada, respetando
            la atención de quien ya estaba esperando al frente).
            
    (dificultad avanzada: opcional)
        - Si ingresa un nuevo paciente prioritario y ya hay otro en el
            segundo puesto, el nuevo se ubica detrás de los prioritarios
            existentes, pero delante de la lista general.
"""

def Cargar_Paciente(Db_Pacientes):
    Ingresar_DNI = input("Ingrese el DNI del paciente EJEMPLO:[xxxxxxx]: ")
    
    # Comprobar si el DNI ya existe en la lista de pacientes
    for paciente in Db_Pacientes:
        if paciente[0] == Ingresar_DNI:
            print("---------------------------")
            print("DNI ya registrado")
            print("---------------------------")
            return Db_Pacientes

    nombre = input("Ingrese el Nombre del paciente: ")
    apellido = input("Ingrese el Apellido del paciente: ")
    prioridad = input("El Paciente es prioritario? [Embarazada, movilidad reducida, Adulto mayor]-Y[si]/N[no]: ").upper

    Nuevo_Paciente = [Ingresar_DNI, nombre, apellido, prioridad]

    if prioridad == "Y":
        if len(Db_Pacientes) == 0:
            Db_Pacientes.append(Nuevo_Paciente)
        else:
            # Buscar el puesto tras el último prioritario en espera
            posicion = 1
            while posicion < len(Db_Pacientes) and Db_Pacientes[posicion][3] == "Y":
                posicion += 1
            Db_Pacientes.insert(posicion, Nuevo_Paciente)
    else:
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

while True:
    print()
    print("---------------------------")
    print("Menu De Administracion")
    print("---------------------------")
    print("""Opcciones:
        [0]:Cerrar
        [1]:Agregar un paciente
        [2]:Mostrar lista de espera
        [3]:Atender paciente
        """)
    Opccion = input("Eleccion: ")

    if Opccion == "0":break
    elif Opccion == "1": Cargar_Paciente(Db_Pacientes)
    elif Opccion == "2": Mostrar_Paciente_espera(Db_Pacientes)
    elif Opccion == "3": Atender_paciente(Db_Pacientes)