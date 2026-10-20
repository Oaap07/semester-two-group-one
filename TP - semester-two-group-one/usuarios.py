"""
Requisitos del Trabajo Practico (TPO - SPRINT) - Programacion I
Facultad de Ingenieria Informatica

Modulo: usuarios.py - Ingreso y registro de usuarios.

Tema del trabajo: Administracion de una concesionaria (catalogo de autos + alquileres).

Ofrece las dos puertas de entrada al sistema desde el submenu de usuario:

  - ingresa_usuario() ... valida DNI y contraseña de un usuario ya registrado y
    devuelve su sesion [dni, nombre, autos_rentados].
  - registro_usuario() .. pide los datos de un usuario nuevo y lo guarda en
    usuarios.json.

Ambas usan "[0]" como salida rapida y validan la entrada con excepciones
especificas (ValueError, TypeError, KeyError).
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
    Pide DNI y contraseña y valida que el usuario exista.

    Args:
        lista (dict): Diccionario con la informacion de todos los usuarios.

    Returns:
        list | tuple | None: [dni, nombre, autos_rentados] si el ingreso es
        valido; una tupla vacia () si el DNI es invalido o el usuario no existe;
        None si el usuario cancela con "0". Tanto () como None son "falsy", por
        eso el llamador los trata igual (vuelve a pedir la opcion).
    """
    while True:
        limpiar()
        # Se piden el DNI y la contraseña; los errores de entrada se manejan abajo.
        print("--- INGRESO: USUARIOS ---")
        print("[0] en cualquier campo para salir.\n")
        try:

            dni_usu = int(input("Ingrese DNI de usuario: "))
            # Salida rapida: 0 corta; un valor no numerico cae en el except.
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

            # Bucle de validacion de la contraseña: se repite mientras no coincida.
            while True:
                # Permitir salir escribiendo "0".
                if clave_usu == "0": break
                elif dni_usu in lista and clave_usu != lista[dni_usu]["clave"]:
                    clave_usu = input("Contraseña incorrecta, intente de nuevo: ").lower()
                # Clave vacia: int("") lanza ValueError, que atrapa el except de abajo.
                elif clave_usu.strip() == "" : int(clave_usu)
                else: break
            break
        # Se capturan excepciones especificas: ValueError del int(input) y
        # TypeError/KeyError si 'lista' no es un diccionario valido.
        except (ValueError, TypeError, KeyError):
            print()
            print("[ERROR] Intente de nuevo.")
            try: input("[Enter] ")
            except: pass
        
    # Se retorna la sesion del usuario como lista:
    # indice [0] = dni, [1] = nombre, [2] = autos rentados.
    if dni_usu in lista and clave_usu == lista[dni_usu]["clave"]:
        limpiar()
        print("=" * 20)
        # Las comillas dobles anidadas en el f-string requieren Python 3.12+.
        print(f"Bienvenido/a {lista[dni_usu]["nombre"]}!")
        print("=" * 20)
        try: input("[Enter] ")
        except: pass
        return list((dni_usu, lista[dni_usu]["nombre"], lista[dni_usu]["autos_rentados"]))
    elif dni_usu == "0" or clave_usu == "0":
        return 

def registro_usuario(lista):
    """
    Pide los datos de un usuario nuevo y lo guarda en usuarios.json.

    Valida que el DNI tenga 8 digitos y que no este ya registrado, y que la
    contraseña se repita correctamente. Los usuarios precargados tienen la clave
    "1234". Si el archivo ya existe, se sobreescribe con el usuario agregado.

    Args:
        lista (dict): Diccionario con la informacion de todos los usuarios.

    Returns:
        None: el usuario nuevo queda guardado en el archivo de usuarios.

    Nota:
        Algunos caminos de salida cortan el registro antes de tener todos los datos
        (ver "problemas conocidos" en la documentacion tecnica).
    """
    while True:
        try:
            limpiar()
            # Se piden el DNI, el nombre y la contraseña; los errores de entrada
            # se manejan abajo.
            print("--- REGISTRO: USUARIOS ---")
            print("[0] en cualquier campo para salir.\n")
            while True:
                # Nota: "limpiar" sin parentesis no ejecuta la funcion (solo la
                # referencia); no tiene efecto sobre el programa.
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
                    
                    # Bucle de confirmacion: la clave se repite hasta coincidir.
                    while True:
                        if clave_usu == clave_usu2: break
                        elif clave_usu2 == "0": return
                        else: clave_usu2 = input("|| Clave incorrecta, intente de nuevo: ")
                # Sale del bucle interior tras un intento correcto.
                break
        # Se capturan excepciones especificas (ValueError, TypeError/KeyError si
        # 'lista' no es un diccionario valido).
        except (ValueError, TypeError, KeyError):
            print()
            print("[ERROR] Intente de nuevo.")
            try: input("[Enter] ")
            except: pass
        # Sale del bucle exterior (el registro corre una sola vez).
        break

    # Se agrega el usuario nuevo al diccionario: su DNI es la clave de acceso.
    lista[str(dni_usu)] = {
        "nombre": nombre_usu,
        "clave": clave_usu,
        "autos_rentados": []
    }

    # Se guarda el diccionario completo de usuarios en el archivo JSON. El
    # guardado se envuelve en try/except: si el archivo no se puede escribir se
    # informa y se sale sin anunciar un registro exitoso.
    try:
        with open(inf.RUTA_USUARIOS_JSON, "w", encoding="utf-8") as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)
    except OSError as e:
        print(f"/// No se pudo escribir el archivo de usuarios: {e} ///")
        return

    limpiar()
    print(f"||| ¡Usuario [{nombre_usu.capitalize()}] registrado exitosamente! |||")
    try: input("[Enter] ")
    except: pass
