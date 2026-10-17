"""
Requisitos del Trabajo Practico (TPO - SPRINT) - Programacion I
Facultad de Ingenieria Informatica

Modulo: usuarios.py - Logica de ingreso y registro de usuarios.
Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).
"""

import json, os
import informe as inf

def limpiar():
    """
    Limpia la consola segun el sistema operativo.

    En Windows usa 'cls'; en Linux/macOS usa 'clear'. Sirve para mantener la
    interfaz ordenada entre pantallas del menu.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def ingresa_usuario(lista):
    """
    Interfaz para el ingreso de un usuario ya registrado.

    Args:
        lista (list): Diccionario con la información de todos los usuarios.
    
    Returns:
        tupla: Con el Nombre y Autos rentados del usuario
    """
    while True:
        limpiar()
        #  Manejo de excepciones en inputs.
        #  Se pide el DNI y la contraseña al usuario.
        print("--- REGISTRO: USUARIOS ---")
        print("[0] en cualquier campo para salir.\n")
        try: 

            dni_usu = int(input("Ingrese DNI de usuario: "))
            dni_usu = str(dni_usu)

            if len(dni_usu) != 8 and dni_usu != "0":
                print("\nDNI inválido, intente de nuevo")
                try: input("[Enter] ")
                except: pass
                return ()
            elif dni_usu not in lista and dni_usu != "0":
                print("\nUsuario inexistente, regístrese.")
                try: input("[Enter] ")
                except: pass
                return ()
            
            clave_usu : str = input("Ingrese contraseña: ").lower()

            while True:
                if clave_usu == "0": break
                elif dni_usu in lista and clave_usu != lista[dni_usu]["clave"]:
                    clave_usu = input("Contraseña incorrecta, intente de nuevo: ").lower()
                elif clave_usu.strip() == "" : int(clave_usu)
                else: break
            break
        except:
            print()
            print("[ERROR] Intente de nuevo.")
            try: input("[Enter] ")
            except: pass
        
    #  Se retorna el Nombre y una lista con los autos que rentó
    if dni_usu in lista and clave_usu == lista[dni_usu]["clave"]:
        limpiar()
        print("=" * 20)
        print(f"Bienvenido/a {lista[dni_usu]["nombre"]}!")
        print("=" * 20)
        try: input("[Enter] ")
        except: pass
        return list((dni_usu, lista[dni_usu]["nombre"], lista[dni_usu]["autos_rentados"]))
    elif dni_usu == "0" or clave_usu == "0":
        return 

def registro_usuario(lista):
    """
    Interfaz para el registro de usuarios nuevos.

    Args:
        lista (list): Diccionario con la información de todos los usuarios.
    
    Returns:
        
    """
    while True:
        try:
            limpiar()
            #  Manejo de excepciones en inputs.
            #  Se pide el DNI y la contraseña al usuario.
            print("--- REGISTRO: USUARIOS ---")
            print("[0] en cualquier campo para salir.\n")
            while True:
                limpiar

                try: dni_usu = int(input("Ingrese su DNI: "))
                except: print("\nError, sólo se permiten números"); input("[Enter] "); break
                
                if dni_usu == 0: return
                elif len(str(dni_usu)) != 8:
                    print("\nDNI inválido, intente de nuevo.")
                    try: input("[Enter] ")
                    except: pass
                    break
                elif str(dni_usu) in lista:
                    print("\nDNI ya existente, vaya a 'INGRESAR'")
                    try: input("[Enter] ")
                    except: pass
                    return ()
                else:
                    nombre_usu : str = input("Ingrese su nombre: ")
                    clave_usu : str = input("Ingrese una contraseña: ").lower()
                    
                    if clave_usu == "0" or nombre_usu == "0": return ()
                    clave_usu2 : str = input("Comprueba contraseña: ").lower()
                    
                    while True:
                        if clave_usu == clave_usu2: break
                        elif clave_usu2 == "0": return
                        else: clave_usu2 = input("|| Clave incorrecta, intente de nuevo: ")
                break  
        except:
            print()
            print("[ERROR] Intente de nuevo.")
            try: input("[Enter] ")
            except: pass
        break

    lista[str(dni_usu)] = {
        "nombre": nombre_usu,
        "clave": clave_usu,
        "autos_rentados": []
    }

    with open(inf.RUTA_USUARIOS_JSON, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)
    
    limpiar()
    print(f"||| ¡Usuario [{nombre_usu.capitalize()}] registrado exitosamente! |||")
    try: input("[Enter] ")
    except: pass  

    #  Se retorna el Nombre y una lista con los autos que rentó
