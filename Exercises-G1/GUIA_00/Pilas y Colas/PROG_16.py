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