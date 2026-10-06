import json
import random

# Tuplas con datos de referencia para la generación aleatoria
NOMBRES = ("María", "Juan", "Sofía", "Lucas", "Valentina", "Mateo", "Camila", "Joaquín")
APELLIDOS = ("Pérez", "Gómez", "González", "Rodríguez", "López", "Martínez", "Fernández")
NACIONALIDADES = ("Argentina", "Uruguaya", "Chilena", "Paraguaya", "Boliviana")
ESTADOS_CIVILES = ("soltero", "casado", "divorciado")
ESTADOS_CURSADA = ("regular", "moroso", "pendiente")


def obtener_dias_mes(mes: int) -> int:
    if mes == 2:
        return 28
    elif mes in (4, 6, 9, 11):
        return 30
    return 31


def generar_fecha_nacimiento() -> str:
    anio = random.randint(1998, 2006)
    mes = random.randint(1, 12)
    dia = random.randint(1, obtener_dias_mes(mes))
    # Formato DD-MM-YY (ejemplo: 01-01-08)
    return f"{dia:02d}-{mes:02d}-{str(anio)[-2:]}"


def generar_alumnos_json(
    ruta_archivo: str = "alumnos.json", cantidad_registros: int = 10
) -> None:
    alumnos_dict = {}

    for i in range(1, cantidad_registros + 1):
        clave_id = str(i)  # Clave '1', '2', etc.

        alumnos_dict[clave_id] = {
            "nombre": random.choice(NOMBRES),
            "apellido": random.choice(APELLIDOS),
            "fecha_nac": generar_fecha_nacimiento(),
            "nacionalidad": random.choice(NACIONALIDADES),
            "estado_civil": random.choice(ESTADOS_CIVILES),
            "estado_cursada": random.choice(ESTADOS_CURSADA),
            "notas": [random.randint(4, 10) for _ in range(5)],  # Genera array de 5 notas
        }

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        # ensure_ascii=False permite guardar caracteres especiales como acentos y eñes correctamente
        json.dump(alumnos_dict, f, indent=4, ensure_ascii=False)

    print(
        f"[alumnos_json.py] Archivo '{ruta_archivo}' generado con éxito con {cantidad_registros} alumnos.\n"
    )


if __name__ == "__main__":
    generar_alumnos_json()
