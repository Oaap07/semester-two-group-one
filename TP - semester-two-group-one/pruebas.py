"""
Modulo: pruebas.py - Pruebas automaticas del Trabajo Practico (TPO - SPRINT).

Suite de pytest para el sistema de la concesionaria. Se puede ejecutar de dos formas:

    python -m pytest pruebas.py -v
    python pruebas.py

Cubre:
  - CRUD (Req 7): alta (con "estado"), lectura, modificacion de cada campo y
    borrado; y el catalogo tabulado con pandas (ver_stock) en sus tres modos,
    incluidos los avisos de listas vacias (Req 8).
  - Persistencia (Req 2): _cargar_autos / _guardar_autos, open_autos /
    open_usuarios y escribir_auto / escribir_usuario.
  - Excepciones y validaciones (Req 1): patente "0"/cancelacion, DNI no
    numerico, invalido o inexistente, archivos ausentes o corruptos, fin de
    entrada (EOF) y valores no serializables.
  - Usuarios (Req 2): ingreso (clave incorrecta, DNI invalido) y registro
    (cancelacion, DNI duplicado, claves distintas).
  - Alquiler (Req 2): rentar y devolver el mismo auto; el campo "estado" cambia
    a False y vuelve a True, y la patente entra y sale de "autos_rentados".
  - Navegacion: menu_principal, submenu_usuario, submenu_empresa y estado_rentas.
  - Generacion de datos (Req 3): informe_autos / informe_usuarios.

Cada prueba corre en un directorio temporal propio (fixture 'entorno'), asi no
toca los archivos reales del proyecto. La entrada por teclado se simula con el
helper 'guion()'.

Los bugs que quedan documentados en el codigo se registran como pruebas xfail
(se espera que fallen) para dejar constancia de ellos sin romper la suite.
"""

import json
import random
import sys
from pathlib import Path

import pytest

# Se agrega la carpeta del proyecto al path para poder importar los modulos.
RAIZ = Path(__file__).resolve().parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import crud  # noqa: E402
import informe as inf  # noqa: E402
import menu  # noqa: E402
import usuarios as us  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers y fixtures
# ---------------------------------------------------------------------------

# DNI de prueba (8 digitos, como exige el sistema).
DNI = "30000000"


def _sin_entrada(prompt=""):
    """Input por defecto: la entrada se cierra de inmediato (EOFError)."""
    raise EOFError


@pytest.fixture(autouse=True)
def entorno(tmp_path, monkeypatch):
    """Aisla cada prueba: directorio temporal propio y sin datos de entrada."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("builtins.input", _sin_entrada)
    return tmp_path


def guion(monkeypatch, respuestas):
    """Instala un input simulado que devuelve 'respuestas' y luego lanza EOFError."""
    pendientes = list(respuestas)

    def falso_input(prompt=""):
        if not pendientes:
            raise EOFError
        return pendientes.pop(0)

    monkeypatch.setattr("builtins.input", falso_input)
    return falso_input


def escribir(nombre, datos):
    """Guarda 'datos' como JSON en 'nombre' (en el directorio temporal actual)."""
    with open(nombre, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def leer(nombre):
    """Lee y devuelve el JSON guardado en 'nombre'."""
    with open(nombre, encoding="utf-8") as f:
        return json.load(f)


def auto_disponible(modelo="corolla", categoria="sedan_hatchback"):
    """Auto de prueba con los 7 atributos del esquema y estado disponible."""
    return {
        "marca": crud.MARCA[0],
        "modelo": modelo,
        "calidad": "nuevo",
        "año": 2015,
        "precio": 15000,
        "categoria": categoria,
        "estado": True,
    }


def auto_rentado(modelo="etios", categoria="sedan_hatchback"):
    """Auto de prueba con estado no disponible (rentado)."""
    return {**auto_disponible(modelo=modelo, categoria=categoria), "estado": False}


def usuario_rentado(patentes=()):
    """Usuario de prueba con la lista de autos rentados indicada."""
    return {"nombre": "Juan", "clave": "1234", "autos_rentados": list(patentes)}


# ---------------------------------------------------------------------------
# Persistencia y validacion de archivos (Req 1 y 2)
# ---------------------------------------------------------------------------

class TestPersistencia:
    def test_archivo_ausente_devuelve_dict_vacio(self):
        assert crud._cargar_autos() == {}

    def test_json_corrupto_devuelve_dict_vacio(self, monkeypatch):
        with open("autos.json", "w", encoding="utf-8") as f:
            f.write("{ esto no es json")
        guion(monkeypatch, [""])  # la funcion espera un [Enter]
        assert crud._cargar_autos() == {}

    def test_json_que_no_es_diccionario_devuelve_vacio(self):
        escribir("autos.json", [1, 2, 3])
        assert crud._cargar_autos() == {}

    def test_guardar_rechaza_lo_que_no_es_dict(self):
        assert crud._guardar_autos("no soy un dict") is False

    def test_guardar_rechaza_valores_no_serializables(self):
        assert crud._guardar_autos({"X1": {1, 2, 3}}) is False

    def test_guardar_y_cargar_roundtrip(self):
        catalogo = {"AAA111": auto_disponible()}
        assert crud._guardar_autos(catalogo) is True
        assert crud._cargar_autos() == catalogo

    def test_open_autos_ausente_devuelve_dict_vacio(self):
        assert crud.open_autos() == {}

    def test_open_autos_json_corrupto_devuelve_dict_vacio(self, monkeypatch):
        with open("autos.json", "w", encoding="utf-8") as f:
            f.write("{ roto")
        guion(monkeypatch, [""])
        assert crud.open_autos() == {}

    def test_open_autos_no_dict_devuelve_dict_vacio(self):
        escribir("autos.json", [1, 2, 3])
        assert crud.open_autos() == {}

    def test_open_usuarios_ausente_devuelve_dict_vacio(self):
        assert crud.open_usuarios() == {}

    def test_open_usuarios_roundtrip(self):
        usuarios = {DNI: usuario_rentado()}
        escribir("usuarios.json", usuarios)
        assert crud.open_usuarios() == usuarios

    def test_escribir_auto_guarda_y_rechaza_no_dict(self):
        catalogo = {"AAA111": auto_disponible()}
        assert crud.escribir_auto(catalogo) is True
        assert leer("autos.json") == catalogo
        assert crud.escribir_auto("no soy un dict") is False

    def test_escribir_usuario_guarda_y_rechaza_no_dict(self):
        usuarios = {DNI: usuario_rentado()}
        assert crud.escribir_usuario(usuarios) is True
        assert leer("usuarios.json") == usuarios
        assert crud.escribir_usuario("no soy un dict") is False


# ---------------------------------------------------------------------------
# Validaciones de entrada (Req 1)
# ---------------------------------------------------------------------------

class TestValidacionesDeEntrada:
    def test_entrada_recorta_espacios(self, monkeypatch):
        guion(monkeypatch, ["  hola  "])
        assert crud._entrada("x") == "hola"

    def test_entrada_con_eof_devuelve_none(self, monkeypatch):
        guion(monkeypatch, [])
        assert crud._entrada("x") is None

    def test_patente_cancelada_con_cero_devuelve_none(self, monkeypatch):
        guion(monkeypatch, ["0"])
        assert crud._pedir_patente_existente({"AAA111": auto_disponible()}) is None

    def test_patente_devuelve_mayusculas(self, monkeypatch):
        guion(monkeypatch, ["aaa111"])
        assert crud._pedir_patente_existente({"AAA111": auto_disponible()}) == "AAA111"

    def test_patente_reintenta_hasta_encontrar(self, monkeypatch):
        guion(monkeypatch, ["nope", "AAA111"])
        assert crud._pedir_patente_existente({"AAA111": auto_disponible()}) == "AAA111"

    def test_patente_con_eof_devuelve_none(self, monkeypatch):
        guion(monkeypatch, [])
        assert crud._pedir_patente_existente({"AAA111": auto_disponible()}) is None

    def test_patente_con_catalogo_vacio_devuelve_none(self, monkeypatch):
        guion(monkeypatch, [""])
        assert crud._pedir_patente_existente({}) is None

    def test_patente_con_catalogo_no_dict_devuelve_none(self, monkeypatch):
        guion(monkeypatch, [""])
        assert crud._pedir_patente_existente([1, 2, 3]) is None

    def test_entero_reintenta_hasta_valor_valido(self, monkeypatch):
        guion(monkeypatch, ["abc", "2005"])
        assert crud._pedir_entero("Anio", 2000, 2026) == 2005

    def test_entero_con_eof_devuelve_none(self, monkeypatch):
        guion(monkeypatch, [])
        assert crud._pedir_entero("Anio", 2000, 2026) is None

    def test_entero_con_rango_invalido_devuelve_none(self):
        assert crud._pedir_entero("Anio", 10, 1) is None

    def test_entero_con_minimo_no_entero_devuelve_none(self):
        assert crud._pedir_entero("Anio", "2000", 2026) is None

    def test_float_acepta_coma(self, monkeypatch):
        guion(monkeypatch, ["15000,5"])
        assert crud._pedir_float("Precio") == 15000.5

    def test_float_rechaza_negativos(self, monkeypatch):
        guion(monkeypatch, ["-5", "10"])
        assert crud._pedir_float("Precio") == 10

    def test_float_con_eof_devuelve_none(self, monkeypatch):
        guion(monkeypatch, [])
        assert crud._pedir_float("Precio") is None

    def test_tupla_estado_se_convierte_a_bool(self, monkeypatch):
        guion(monkeypatch, ["true"])
        assert crud._pedir_de_tupla("estado", crud.ESTADO) is True

    def test_tupla_estado_false_se_convierte_a_bool(self, monkeypatch):
        guion(monkeypatch, ["false"])
        assert crud._pedir_de_tupla("estado", crud.ESTADO) is False

    def test_tupla_con_eof_devuelve_none(self, monkeypatch):
        guion(monkeypatch, [])
        assert crud._pedir_de_tupla("Marca", crud.MARCA) is None

    def test_tupla_con_opciones_vacias_devuelve_none(self):
        assert crud._pedir_de_tupla("Marca", ()) is None

    def test_tupla_con_opciones_no_str_devuelve_none(self):
        assert crud._pedir_de_tupla("Marca", (1, 2)) is None


# ---------------------------------------------------------------------------
# Lecturas: ver_stock (Req 8) y ver_auto (Req 7)
# ---------------------------------------------------------------------------

class TestLecturas:
    def test_ver_stock_catalogo_completo(self, monkeypatch, capsys):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, [""])
        crud.ver_stock(1, 0)
        salida = capsys.readouterr().out
        assert "CATALOGO DE AUTOS" in salida
        assert "AAA111" in salida

    def test_ver_stock_solo_disponibles(self, monkeypatch, capsys):
        escribir("autos.json", {"DISP01": auto_disponible(), "RENT01": auto_rentado()})
        guion(monkeypatch, [""])
        crud.ver_stock(1, 1)
        salida = capsys.readouterr().out
        assert "DISP01" in salida
        assert "RENT01" not in salida

    def test_ver_stock_solo_rentados(self, monkeypatch, capsys):
        escribir("autos.json", {"DISP01": auto_disponible(), "RENT01": auto_rentado()})
        guion(monkeypatch, [""])
        crud.ver_stock(0, 1)
        salida = capsys.readouterr().out
        assert "RENT01" in salida
        assert "DISP01" not in salida

    def test_ver_stock_sin_rentados_avisa(self, monkeypatch, capsys):
        escribir("autos.json", {"DISP01": auto_disponible()})
        guion(monkeypatch, [""])
        crud.ver_stock(0, 1)
        assert "No hay autos rentados" in capsys.readouterr().out

    def test_ver_stock_sin_disponibles_avisa(self, monkeypatch, capsys):
        escribir("autos.json", {"RENT01": auto_rentado()})
        guion(monkeypatch, [""])
        crud.ver_stock(1, 1)
        assert "No hay autos disponibles" in capsys.readouterr().out

    def test_ver_stock_catalogo_vacio_avisa(self, monkeypatch, capsys):
        escribir("autos.json", {})
        guion(monkeypatch, [""])
        crud.ver_stock(1, 0)
        assert "No hay autos" in capsys.readouterr().out

    def test_ver_auto_muestra_la_ficha(self, monkeypatch, capsys):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["AAA111", ""])
        crud.ver_auto()
        salida = capsys.readouterr().out
        assert "AAA111" in salida
        assert "Marca:" in salida

    def test_ver_auto_cancelado_no_lanza_keyerror(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["0"])
        crud.ver_auto()  # antes: KeyError al indexar con la patente "0"

    def test_ver_auto_catalogo_vacio_avisa(self, monkeypatch, capsys):
        escribir("autos.json", {})
        guion(monkeypatch, [""])
        crud.ver_auto()
        assert "No hay autos" in capsys.readouterr().out

    def test_mostrar_auto_ficha_completa(self, capsys):
        crud._mostrar_auto("AAA111", auto_disponible())
        salida = capsys.readouterr().out
        assert "Marca:" in salida
        assert "Modelo:" in salida
        assert "Estado:" in salida

    def test_mostrar_auto_avisa_dato_faltante(self, capsys):
        crud._mostrar_auto("X1", {"marca": "fiat"})
        assert "Falta un dato" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Create / Update / Delete (Req 6 y 7)
# ---------------------------------------------------------------------------

class TestCreateUpdateDelete:
    def test_agregar_auto_crea_los_7_atributos(self, monkeypatch):
        escribir("autos.json", {})
        guion(monkeypatch, [
            "test99",            # patente
            crud.MARCA[0],       # marca
            "Corolla",           # modelo
            "nuevo",             # calidad
            "2015",              # anio
            "15000",             # precio
            crud.CATEGORIA[0],   # categoria
        ])
        crud.agregar_auto()
        auto = leer("autos.json")["TEST99"]
        assert set(auto) == {"marca", "modelo", "calidad", "año", "precio", "categoria", "estado"}
        assert auto["estado"] is True
        assert auto["modelo"] == "corolla"

    def test_agregar_auto_rechaza_patente_duplicada(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, [
            "AAA111",            # ya existe: debe reintentar
            "bbb222",            # patente nueva
            crud.MARCA[0], "Etios", "usado", "2010", "9000", crud.CATEGORIA[0],
        ])
        crud.agregar_auto()
        datos = leer("autos.json")
        assert "BBB222" in datos
        assert "AAA111" in datos

    def test_agregar_auto_rechaza_patente_vacia(self, monkeypatch):
        escribir("autos.json", {})
        guion(monkeypatch, [
            "",                  # vacia: debe reintentar
            "ccc333",
            crud.MARCA[0], "Etios", "nuevo", "2012", "8000", crud.CATEGORIA[0],
        ])
        crud.agregar_auto()
        assert "CCC333" in leer("autos.json")

    def test_agregar_auto_aborta_si_se_corta_la_entrada(self, monkeypatch):
        escribir("autos.json", {})
        guion(monkeypatch, [])  # EOF en la patente
        crud.agregar_auto()
        assert leer("autos.json") == {}

    def test_modificar_auto_cambia_marca(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["AAA111", "1", crud.MARCA[1], "0"])
        crud.modificar_auto()
        assert leer("autos.json")["AAA111"]["marca"] == crud.MARCA[1]

    def test_modificar_auto_cambia_el_modelo(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["AAA111", "2", "Civic", "0"])
        crud.modificar_auto()
        assert leer("autos.json")["AAA111"]["modelo"] == "civic"

    def test_modificar_auto_cambia_calidad(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["AAA111", "3", "usado", "0"])
        crud.modificar_auto()
        assert leer("autos.json")["AAA111"]["calidad"] == "usado"

    def test_modificar_auto_cambia_el_anio(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["AAA111", "4", "2018", "0"])
        crud.modificar_auto()
        assert leer("autos.json")["AAA111"]["año"] == 2018

    def test_modificar_auto_cambia_el_precio(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["AAA111", "5", "20000", "0"])
        crud.modificar_auto()
        assert leer("autos.json")["AAA111"]["precio"] == 20000.0

    def test_modificar_auto_cambia_la_categoria(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["AAA111", "6", crud.CATEGORIA[1], "0"])
        crud.modificar_auto()
        assert leer("autos.json")["AAA111"]["categoria"] == crud.CATEGORIA[1]

    def test_modificar_auto_cambia_el_estado(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["AAA111", "7", "false", "0"])
        crud.modificar_auto()
        assert leer("autos.json")["AAA111"]["estado"] is False

    def test_modificar_auto_ignora_opcion_no_numerica(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["AAA111", "xyz", "0"])
        crud.modificar_auto()  # antes: ValueError en int(opcion)
        assert leer("autos.json")["AAA111"]["modelo"] == "corolla"

    def test_modificar_auto_ignora_opcion_fuera_de_rango(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["AAA111", "99", "0"])
        crud.modificar_auto()
        assert leer("autos.json")["AAA111"]["modelo"] == "corolla"

    def test_modificar_auto_catalogo_vacio_avisa(self, monkeypatch, capsys):
        escribir("autos.json", {})
        guion(monkeypatch, [""])
        crud.modificar_auto()
        assert "No hay autos" in capsys.readouterr().out

    def test_eliminar_auto_cancelado_conserva_el_auto(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["0"])
        crud.eliminar_auto()  # antes: KeyError con la patente "0"
        assert "AAA111" in leer("autos.json")

    def test_eliminar_auto_borra_la_patente(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, ["AAA111"])
        crud.eliminar_auto()
        assert "AAA111" not in leer("autos.json")

    def test_eliminar_auto_catalogo_vacio_avisa(self, monkeypatch, capsys):
        escribir("autos.json", {})
        guion(monkeypatch, [""])
        crud.eliminar_auto()
        assert "No hay autos" in capsys.readouterr().out

    def test_modificar_estado_auto_invierte_el_estado(self):
        escribir("autos.json", {"AAA111": auto_disponible()})
        assert crud.modificar_estado_auto("AAA111", True) is True
        assert leer("autos.json")["AAA111"]["estado"] is False

    def test_modificar_estado_auto_lo_vuelve_disponible(self):
        escribir("autos.json", {"AAA111": auto_rentado()})
        assert crud.modificar_estado_auto("AAA111", False) is True
        assert leer("autos.json")["AAA111"]["estado"] is True

    def test_modificar_estado_auto_patente_inexistente(self):
        escribir("autos.json", {"AAA111": auto_disponible()})
        assert crud.modificar_estado_auto("ZZZ999", True) is False

    def test_modificar_estado_auto_rechaza_no_bool(self):
        escribir("autos.json", {"AAA111": auto_disponible()})
        assert crud.modificar_estado_auto("AAA111", "true") is False


# ---------------------------------------------------------------------------
# Usuarios (Req 2): ingreso y registro
# ---------------------------------------------------------------------------

class TestUsuarios:
    def test_ingreso_valido_devuelve_la_lista_del_usuario(self, monkeypatch):
        lista = {DNI: usuario_rentado()}
        guion(monkeypatch, [DNI, "1234"])
        resultado = us.ingresa_usuario(lista)
        assert resultado == [DNI, "Juan", []]

    def test_ingreso_clave_incorrecta_reintenta(self, monkeypatch):
        lista = {DNI: usuario_rentado()}
        guion(monkeypatch, [DNI, "mala", "1234"])
        assert us.ingresa_usuario(lista) == [DNI, "Juan", []]

    def test_ingreso_dni_inexistente_devuelve_tupla_vacia(self, monkeypatch):
        lista = {DNI: usuario_rentado()}
        guion(monkeypatch, ["99999999"])
        assert us.ingresa_usuario(lista) == ()

    def test_ingreso_dni_invalido_devuelve_tupla_vacia(self, monkeypatch):
        lista = {DNI: usuario_rentado()}
        guion(monkeypatch, ["123"])
        assert us.ingresa_usuario(lista) == ()

    def test_ingreso_no_numerico_reintenta_y_cancela(self, monkeypatch):
        lista = {DNI: usuario_rentado()}
        guion(monkeypatch, ["abc", "", "0"])
        assert us.ingresa_usuario(lista) is None

    def test_ingreso_cancelado_con_cero_devuelve_none(self, monkeypatch):
        lista = {DNI: usuario_rentado()}
        guion(monkeypatch, ["0"])
        assert us.ingresa_usuario(lista) is None

    def test_registro_guarda_usuario_nuevo(self, monkeypatch):
        guion(monkeypatch, ["40000000", "Ana", "clave1", "clave1"])
        us.registro_usuario({})
        datos = leer(inf.RUTA_USUARIOS_JSON)
        assert datos["40000000"]["nombre"] == "Ana"
        assert datos["40000000"]["autos_rentados"] == []

    def test_registro_reintenta_si_las_claves_no_coinciden(self, monkeypatch):
        guion(monkeypatch, ["40000000", "Ana", "clave1", "mala", "clave1"])
        us.registro_usuario({})
        assert leer(inf.RUTA_USUARIOS_JSON)["40000000"]["clave"] == "clave1"

    def test_registro_cancelado_con_cero_no_guarda(self, monkeypatch):
        guion(monkeypatch, ["0"])
        us.registro_usuario({})
        assert not Path(inf.RUTA_USUARIOS_JSON).exists()

    def test_registro_dni_duplicado_no_guarda(self, monkeypatch):
        guion(monkeypatch, [DNI])
        us.registro_usuario({DNI: usuario_rentado()})
        assert not Path(inf.RUTA_USUARIOS_JSON).exists()


# ---------------------------------------------------------------------------
# Alquiler (Req 2): rentar, devolver y navegacion
# ---------------------------------------------------------------------------

class TestAlquiler:
    def test_rentar_auto_marca_no_disponible_y_guarda(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        escribir("usuarios.json", {DNI: usuario_rentado()})
        lista_usu = leer("usuarios.json")
        lista_aut = crud.open_autos()
        usu_info = [DNI, "Juan", lista_usu[DNI]["autos_rentados"]]

        # categoria "1" -> modelo "1" -> patente "1"
        guion(monkeypatch, ["1", "1", "1"])
        menu.rentar_auto(usu_info, lista_usu, lista_aut)

        assert leer("autos.json")["AAA111"]["estado"] is False
        assert "AAA111" in leer("usuarios.json")[DNI]["autos_rentados"]

    def test_rentar_auto_cancelado_no_cambia_nada(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_disponible()})
        escribir("usuarios.json", {DNI: usuario_rentado()})
        lista_usu = leer("usuarios.json")
        lista_aut = crud.open_autos()

        guion(monkeypatch, ["0"])
        menu.rentar_auto([DNI, "Juan", []], lista_usu, lista_aut)

        assert leer("autos.json")["AAA111"]["estado"] is True
        assert leer("usuarios.json")[DNI]["autos_rentados"] == []

    def test_rentar_auto_sin_disponibles_avisa(self, monkeypatch, capsys):
        escribir("usuarios.json", {DNI: usuario_rentado()})
        lista_usu = leer("usuarios.json")

        guion(monkeypatch, ["1", "", "0"])
        menu.rentar_auto([DNI, "Juan", []], lista_usu, {})

        assert "No hay autos disponibles" in capsys.readouterr().out

    def test_devolver_auto_lo_deja_disponible(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_rentado()})
        escribir("usuarios.json", {DNI: usuario_rentado(["AAA111"])})
        lista_usu = leer("usuarios.json")
        usu_info = [DNI, "Juan", lista_usu[DNI]["autos_rentados"]]

        guion(monkeypatch, ["1"])
        menu.devolver_auto(usu_info, lista_usu)

        assert leer("autos.json")["AAA111"]["estado"] is True
        assert leer("usuarios.json")[DNI]["autos_rentados"] == []

    def test_devolver_auto_cancelado_no_cambia_nada(self, monkeypatch):
        escribir("autos.json", {"AAA111": auto_rentado()})
        escribir("usuarios.json", {DNI: usuario_rentado(["AAA111"])})
        lista_usu = leer("usuarios.json")

        guion(monkeypatch, ["0"])
        menu.devolver_auto([DNI, "Juan", ["AAA111"]], lista_usu)

        assert leer("autos.json")["AAA111"]["estado"] is False
        assert leer("usuarios.json")[DNI]["autos_rentados"] == ["AAA111"]

    def test_devolver_auto_sin_rentados_no_rompe(self, monkeypatch):
        escribir("autos.json", {})
        escribir("usuarios.json", {DNI: usuario_rentado()})
        lista_usu = leer("usuarios.json")

        guion(monkeypatch, ["0"])
        menu.devolver_auto([DNI, "Juan", []], lista_usu)

        assert leer("usuarios.json")[DNI]["autos_rentados"] == []

    def test_ver_catalogo_imprime_la_tabla(self, monkeypatch, capsys):
        escribir("autos.json", {"AAA111": auto_disponible()})
        guion(monkeypatch, [""])
        menu.ver_catalogo()
        assert "CATALOGO DE AUTOS" in capsys.readouterr().out

    def test_menu_principal_sale_con_cero(self, monkeypatch):
        guion(monkeypatch, ["0"])
        menu.menu_principal()

    def test_menu_principal_opcion_invalida_y_sale(self, monkeypatch, capsys):
        guion(monkeypatch, ["x", "", "0"])
        menu.menu_principal()
        assert "no válida" in capsys.readouterr().out

    def test_submenu_usuario_sale_con_cero(self, monkeypatch):
        guion(monkeypatch, ["0"])
        menu.submenu_usuario()

    def test_submenu_empresa_sale_con_cero(self, monkeypatch):
        guion(monkeypatch, ["0"])
        menu.submenu_empresa()

    def test_submenu_empresa_opcion_estadisticas(self, monkeypatch, capsys):
        guion(monkeypatch, ["4", "0"])
        menu.submenu_empresa()
        assert "hola" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Informes (Req 8) y generacion de datos (Req 3)
# ---------------------------------------------------------------------------

class TestInformes:
    def test_informe_disponibilidad_muestra_disponibles(self, monkeypatch, capsys):
        escribir("autos.json", {"DISP01": auto_disponible(), "RENT01": auto_rentado()})
        guion(monkeypatch, [""])
        menu.informe_disponibilidad()
        salida = capsys.readouterr().out
        assert "DISP01" in salida
        assert "RENT01" not in salida

    def test_informe_disponibilidad_sin_autos_avisa(self, monkeypatch, capsys):
        escribir("autos.json", {})
        guion(monkeypatch, [""])
        menu.informe_disponibilidad()
        assert "No hay autos" in capsys.readouterr().out

    def test_estado_rentas_muestra_rentados(self, monkeypatch, capsys):
        escribir("autos.json", {"DISP01": auto_disponible(), "RENT01": auto_rentado()})
        guion(monkeypatch, [""])
        menu.estado_rentas()
        salida = capsys.readouterr().out
        assert "RENT01" in salida
        assert "DISP01" not in salida

    def test_estado_rentas_sin_rentados_avisa(self, monkeypatch, capsys):
        escribir("autos.json", {"DISP01": auto_disponible()})
        guion(monkeypatch, [""])
        menu.estado_rentas()
        assert "No hay autos rentados" in capsys.readouterr().out

    def test_informe_estadisticas_sigue_siendo_un_stub(self, capsys):
        menu.informe_estadisticas()
        assert capsys.readouterr().out.strip() == "hola"

    def test_informe_autos_genera_los_registros_del_esquema(self, monkeypatch):
        random.seed(1234)  # determinismo para que la prueba no sea flaky
        guion(monkeypatch, [""])
        inf.informe_autos("autos_gen.json", 5)
        datos = leer("autos_gen.json")
        assert len(datos) == 25  # el parametro se ignora y siempre son 25
        for auto in datos.values():
            assert set(auto) == {"marca", "modelo", "calidad", "año", "precio", "categoria", "estado"}
            assert auto["estado"] is True

    def test_informe_usuarios_precarga_ejemplos(self, monkeypatch):
        guion(monkeypatch, [""])
        inf.informe_usuarios("usuarios_gen.json")
        datos = leer("usuarios_gen.json")
        assert "95823279" in datos
        assert datos["95823279"]["autos_rentados"] == []


# ---------------------------------------------------------------------------
# Bugs documentados (se espera que fallen: xfail)
# ---------------------------------------------------------------------------

class TestBugsDocumentados:
    @pytest.mark.xfail(
        strict=True,
        reason="BUG en ver_stock (modo 1,0): accede a autos[i]['estado'] sin .get()",
    )
    def test_ver_stock_rompe_con_auto_sin_clave_estado(self, monkeypatch):
        sin_estado = {"marca": crud.MARCA[0], "modelo": "corolla", "calidad": "nuevo",
                      "año": 2010, "precio": 100, "categoria": "sedan_hatchback"}
        escribir("autos.json", {"X1": sin_estado})
        guion(monkeypatch, [""])
        crud.ver_stock(1, 0)

    @pytest.mark.xfail(
        strict=True,
        reason="BUG en registro_usuario: tras un DNI invalido sigue y usa variables sin definir (NameError)",
    )
    def test_registro_con_dni_invalido_no_deberia_continuar(self, monkeypatch):
        guion(monkeypatch, ["1234567", ""])  # 7 digitos: DNI invalido
        us.registro_usuario({})


if __name__ == "__main__":
    # Permite ejecutar la suite directamente: python pruebas.py
    raise SystemExit(pytest.main([__file__, "-v"]))
