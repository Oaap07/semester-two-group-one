import json

def modificar_estado_civil():
    with open("alumnos.json", 'r', encoding="utf-8") as archivo:
        diccionario = json.load(archivo)
    ESTADOS_CIVILES = ("soltero", "casado", "divorciado")
    print('Ingresa el ID', diccionario.keys())
    alumno_id = input()
    while alumno_id not in diccionario.keys():
        print('Ingresa el ID', diccionario.keys())
        alumno_id = input()
    print('Elige la nueva opción')
    for estado in ESTADOS_CIVILES:
        print(estado)
    nuevo_estado = input()
    while nuevo_estado not in ESTADOS_CIVILES:
        nuevo_estado = input('Invalido, vuelve a intentar')
        
    diccionario[alumno_id]["estado_civil"] = nuevo_estado
    with open("alumnos.json", "w", encoding="utf-8") as archivo:
        json.dump(diccionario, archivo, indent=4, ensure_ascii=False)
