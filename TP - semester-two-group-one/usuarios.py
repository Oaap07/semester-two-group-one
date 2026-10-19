"""
Requisitos del Trabajo Practico (TPO - SPRINT) - Programacion I
Facultad de Ingenieria Informatica

Modulo: usuarios.py - Logica de ingreso y registro de usuarios.
Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).
"""
# ------------------------------------------------------------------
# CUMPLIMIENTO DEL SPRINT - requisitos que aporta ESTE modulo:
#   Req 1 (excepciones especificas) ....... PARCIAL (except genericos en el
#                                             login y en el registro)
#   Req 2 (persistencia en JSON) .......... CUMPLIDO (escribe usuarios.json)
# Los trabajos pendientes estan marcados en el codigo como "TODO(TP - Req N)" y las mejoras sugeridas como
# "RECOMENDACION (Req N)".
# ------------------------------------------------------------------

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
        lista (dict): Diccionario con la informacion de todos los usuarios.
    
    Returns:
        list: [dni, nombre, autos_rentados] del usuario validado; None si se
        cancela con "0" (NOTA: antes devolvia una tupla de 2 valores).
        NOTA (inconsistencia): en los rechazos devuelve la tupla vacia () (no
        None); ambos son "falsy", por eso el llamador los trata igual.
    """
    while True:
        limpiar()
        #  Manejo de excepciones en inputs.
        #  Se pide el DNI y la contraseña al usuario.
        print("--- INGRESO: USUARIOS ---")
        print("[0] en cualquier campo para salir.\n")
        try: 

            dni_usu = int(input("Ingrese DNI de usuario: "))
            # Salida rapida: 0 (o un valor no numerico, que cae en el except) corta.
            if dni_usu == 0: return 
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

            # Bucle de validacion de la contraseña.
            while True:
                # Permitir salir escribiendo "0".
                if clave_usu == "0": break
                elif dni_usu in lista and clave_usu != lista[dni_usu]["clave"]:
                    clave_usu = input("Contraseña incorrecta, intente de nuevo: ").lower()
                # NOTA (linea rara): int(clave_usu) con la clave vacia lanzaria
                # ValueError (lo atrapa el except de mas abajo); la linea no
                # valida realmente el campo vacio.
                elif clave_usu.strip() == "" : int(clave_usu)
                else: break
            break
        # TODO(TP - Req 1): capturar excepciones especificas (ValueError para int(input), TypeError si 'lista' es None);
        # el except generico oculta cualquier fallo y solo muestra "[ERROR] Intente de nuevo.".
        except:
            print()
            print("[ERROR] Intente de nuevo.")
            try: input("[Enter] ")
            except: pass
        
    #  Se retorna el dni, el Nombre y una lista con los autos que rento
    #  (indice [0] = dni, [1] = nombre, [2] = autos rentados).
    if dni_usu in lista and clave_usu == lista[dni_usu]["clave"]:
        limpiar()
        print("=" * 20)
        # NOTA (compatibilidad): las comillas dobles anidadas dentro del f-string
        # requieren Python 3.12 o superior.
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
        lista (dict): Diccionario con la informacion de todos los usuarios.
    
    Returns:
        None: el usuario nuevo queda guardado en usuarios.json.
    """
    while True:
        try:
            limpiar()
            #  Manejo de excepciones en inputs.
            #  Se pide el DNI y la contraseña al usuario.
            print("--- REGISTRO: USUARIOS ---")
            print("[0] en cualquier campo para salir.\n")
            while True:
                # BUG (logica): "limpiar" sin parentesis NO ejecuta la funcion; solo se referencia el objeto funcion;
                # falta limpiar().
                limpiar

                # NOTA (posible error): si el ingreso no es numerico se corta el
                # bucle y se sigue hacia el registro (mas abajo), con lo que
                # "dni_usu" puede quedar sin definir (NameError).
                try: dni_usu = int(input("Ingrese su DNI: "))
                except: print("\nError, sólo se permiten números"); input("[Enter] "); break
                
                if dni_usu == 0: return
                elif len(str(dni_usu)) != 8:
                    # BUG (logica): tras avisar, el "break" corta el bucle pero NO sale de la funcion; el registro de
                    # mas abajo corre igual y guarda un DNI invalido (por ejemplo, de 7 digitos).
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
                # Sale del bucle interior tras un intento correcto.
                break  
        # TODO(TP - Req 1): except generico; capturar excepciones especificas (ValueError para int(input)) en lugar de
        # tragar cualquier error.
        except:
            print()
            print("[ERROR] Intente de nuevo.")
            try: input("[Enter] ")
            except: pass
        # Sale del bucle exterior (el registro corre una sola vez).
        break

    # BUG (NameError): si se salio por los "break" anteriores, "dni_usu", "nombre_usu" y/o "clave_usu" pueden no existir
    # y esto lanza NameError.
    lista[str(dni_usu)] = {
        "nombre": nombre_usu,
        "clave": clave_usu,
        "autos_rentados": []
    }

    # Guarda el diccionario completo de usuarios en el archivo JSON.
    # BUG (OSError): sin try/except; si el archivo no se puede escribir, el OSError se propaga y corta el programa.
    # TODO(TP - Req 1): envolver en try/except (OSError) para el guardado.
    with open(inf.RUTA_USUARIOS_JSON, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)
    
    limpiar()
    print(f"||| ¡Usuario [{nombre_usu.capitalize()}] registrado exitosamente! |||")
    try: input("[Enter] ")
    except: pass  

    # NOTA (comentario huerfano): quedo el texto "se retorna el Nombre y una
    # lista con los autos que rento", pero esta funcion no retorna nada: solo
    # guarda el usuario nuevo en el archivo.
