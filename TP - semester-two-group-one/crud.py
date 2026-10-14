import json

# ==========================================
# CRUD DEL CATÁLOGO DE AUTOS
# ==========================================

RUTA_AUTOS = "autos.json"

CALIDADES = ("nuevo", "como nuevo", "usado")
MARCAS = ("toyota", "renault", "fiat", "peugeot", "chevrloet")
CATEGORIAS = ("sedan_hatchback", "suv_crossover", "pickup", "monovolumen_mpv")

# Opción de menú(clave en el JSON)
CAMPOS = {
    "1": ("marca", "Marca"),
    "2": ("modelo", "Modelo"),
    "3": ("calidad", "Calidad"),
    "4": ("año", "Año"),
    "5": ("precio", "Precio"),
    "6": ("categoria", "Categoría"),
}


# ---------- Persistencia ----------

def _cargar_autos():
    """Lee el catálogo de autos desde el archivo JSON."""
    with open(RUTA_AUTOS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def _guardar_autos(autos):
    """Escribe el catálogo de autos en el archivo JSON."""
    with open(RUTA_AUTOS, "w", encoding="utf-8") as archivo:
        json.dump(autos, archivo, indent=4, ensure_ascii=False)


# ---------- Validaciones de entrada ----------

def _pedir_de_tupla(etiqueta, opciones):
    """Pide un valor que obligatoriamente debe estar dentro de 'opciones'."""
    print(f"{etiqueta} (opciones: {', '.join(opciones)}): ")
    valor = input().strip().lower()
    while valor not in opciones:
        print(f"Valor inválido. {etiqueta} debe ser una de: {', '.join(opciones)}")
        valor = input().strip().lower()
    return valor


def _pedir_entero(etiqueta, minimo, maximo):
    """Pide un número entero dentro de un rango."""
    valor = input(f"{etiqueta} ({minimo}-{maximo}): ").strip()
    while not valor.isdigit() or not (minimo <= int(valor) <= maximo):
        valor = input(f"Inválido. {etiqueta} debe ser un número entre {minimo} y {maximo}: ").strip()
    return int(valor)


def _pedir_float(etiqueta):
    """Pide un número decimal positivo (acepta coma o punto)."""
    valor = input(f"{etiqueta}: ").strip().replace(",", ".")
    while True:
        try:
            numero = float(valor)
            if numero > 0:
                return numero
        except ValueError:
            pass
        valor = input(f"Inválido. {etiqueta} debe ser un número positivo: ").strip().replace(",", ".")


def _pedir_patente_existente(autos):
    """Pide una patente y valida que ya exista en el catálogo."""
    patente = input("Ingrese la patente del auto: ").strip().upper()
    while patente not in autos:
        patente = input("Patente no encontrada. Ingrese una patente válida: ").strip().upper()
    return patente


# ---------- Mostrar ----------

def _mostrar_auto(patente, datos):
    print(f"\n[{patente}]")
    print(f"\tMarca: {datos['marca'].capitalize()}")
    print(f"\tModelo: {datos['modelo'].capitalize()}")
    print(f"\tCalidad: {datos['calidad']}")
    print(f"\tAño: {datos['año']}")
    print(f"\tPrecio: u$d {datos['precio']:.1f}")
    print(f"\tCategoría: {datos['categoria']}")


# ---------- READ ----------

def ver_autos():
    """Muestra todo el catálogo."""
    autos = _cargar_autos()
    if not autos:
        print("\nNo hay autos en el catálogo.")
        return
    print("\n--- CATÁLOGO DE AUTOS ---")
    for patente, datos in autos.items():
        _mostrar_auto(patente, datos)


def ver_auto():
    """Muestra un auto según su patente."""
    autos = _cargar_autos()
    if not autos:
        print("\nNo hay autos en el catálogo.")
        return
    patente = _pedir_patente_existente(autos)
    _mostrar_auto(patente, autos[patente])


# ---------- CREATE ----------

def agregar_auto():
    """Da de alta un auto nuevo (valida que la patente no exista)."""
    autos = _cargar_autos()

    patente = input("Patente del nuevo auto: ").strip().upper()
    while patente in autos:
        patente = input("Esa patente ya existe. Ingrese otra: ").strip().upper()

    marca = _pedir_de_tupla("Marca", MARCAS)
    modelo = input("Modelo: ").strip().lower()
    calidad = _pedir_de_tupla("Calidad", CALIDADES)
    anio = _pedir_entero("Año", 2000, 2026)
    precio = _pedir_float("Precio (u$d)")
    categoria = _pedir_de_tupla("Categoría", CATEGORIAS)

    autos[patente] = {
        "marca": marca,
        "modelo": modelo,
        "calidad": calidad,
        "año": anio,
        "precio": precio,
        "categoria": categoria,
    }
    _guardar_autos(autos)
    print(f"\nAuto {patente} agregado correctamente.")


# ---------- UPDATE ----------

def modificar_auto():
    """Modifica uno o más campos de un auto existente."""
    autos = _cargar_autos()
    if not autos:
        print("\nNo hay autos para modificar.")
        return

    patente = _pedir_patente_existente(autos)

    while True:
        print(f"\n--- Modificar auto [{patente}] ---")
        for clave, (campo, nombre) in CAMPOS.items():
            print(f"[{clave}] {nombre}: {autos[patente][campo]}")
        print("[0] Terminar")

        opcion = input("\n¿Qué campo desea modificar?: ").strip()

        if opcion == "0":
            break
        elif opcion not in CAMPOS:
            print("\nOpción no válida. Intente de nuevo.")
            continue

        campo, nombre = CAMPOS[opcion]

        if campo == "marca":
            autos[patente]["marca"] = _pedir_de_tupla("Marca", MARCAS)
        elif campo == "modelo":
            autos[patente]["modelo"] = input("Nuevo modelo: ").strip().lower()
        elif campo == "calidad":
            autos[patente]["calidad"] = _pedir_de_tupla("Calidad", CALIDADES)
        elif campo == "año":
            autos[patente]["año"] = _pedir_entero("Año", 2000, 2026)
        elif campo == "precio":
            autos[patente]["precio"] = _pedir_float("Nuevo precio (u$d)")
        elif campo == "categoria":
            autos[patente]["categoria"] = _pedir_de_tupla("Categoría", CATEGORIAS)

        _guardar_autos(autos)
        print(f"\n{nombre} actualizado correctamente.")


# ---------- DELETE ----------

def eliminar_auto():
    """Elimina un auto del catálogo según su patente."""
    autos = _cargar_autos()
    if not autos:
        print("\nNo hay autos para eliminar.")
        return

    patente = _pedir_patente_existente(autos)
    del autos[patente]
    _guardar_autos(autos)
    print(f"\nAuto {patente} eliminado correctamente.")


# ---------- Menú ----------

def menu_crud():
    while True:
        print("\n--- CRUD DE AUTOS ---")
        print("[1] Ver catálogo")
        print("[2] Ver un auto")
        print("[3] Agregar auto")
        print("[4] Modificar auto")
        print("[5] Eliminar auto")
        print("[0] Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ver_autos()
        elif opcion == "2":
            ver_auto()
        elif opcion == "3":
            agregar_auto()
        elif opcion == "4":
            modificar_auto()
        elif opcion == "5":
            eliminar_auto()
        elif opcion == "0":
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu_crud()
