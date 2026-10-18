# Documentación Técnica — Sistema de Gestión de Concesionaria

**Proyecto:** TPO – SPRINT (Programación I)
**Institución:** Facultad de Ingeniería Informática
**Tema:** Administración de una concesionaria (catálogo de autos + alquileres)
**Lenguaje:** Python 3
**Persistencia:** Archivos JSON (`autos.json` y `usuarios.json`)

---

## 1. Descripción general

Aplicación de consola que administra el catálogo de autos de una concesionaria y
permite alquilar y devolver vehículos. Está dividida en **cuatro módulos** de Python
que comparten datos a través de archivos JSON:

- `menu.py` — programa principal: menús de usuario y de empresa.
- `crud.py` — alta, baja, modificación y consulta del catálogo, más la persistencia.
- `usuarios.py` — ingreso (login) y registro de usuarios.
- `informe.py` — constantes compartidas, rutas de archivos y precarga de datos.

Archivos de datos (se crean en tiempo de ejecución con `python informe.py`):

- `autos.json` — el catálogo: `patente → {atributos del auto}`.
- `usuarios.json` — los usuarios: `dni → {nombre, clave, autos_rentados}`.

> Ya **no** existe `rentados.json`: los autos alquilados por cada usuario se guardan
> como una lista de patentes dentro de su registro en `usuarios.json`.

La aplicación ofrece:

- Un **CRUD completo** del catálogo (Crear, Leer, Actualizar, Eliminar).
- Un **menú de usuario** para ingresar/registrarse, alquilar y devolver autos.
- Un **menú de empresa** con informes (disponibilidad y estado de los autos
  rentados como tabla con pandas).
- Una **precarga** de autos aleatorios (`informe.informe_autos`).

---

## 2. Requisitos del trabajo práctico

| # | Requisito | Estado en el código |
|---|-----------|---------------------|
| 1 | Manejo de excepciones en ingreso de datos, conversiones y archivos | **Parcial** — hay `try/except` en las entradas y al abrir/guardar archivos, pero abundan los `except` genéricos y varias funciones devuelven `None` ante un error. |
| 2 | Persistencia en JSON (CUD sobreescriben; Read lee) | **Cumplido** (`autos.json`, `usuarios.json`). |
| 3 | Precarga desde archivo inicial (mínimo 5 registros) | **Cumplido** (`informe_autos` genera 25 autos; `informe_usuarios` deja 1 usuario de ejemplo). |
| 4 | Uso de tupla o conjunto en la lógica | **Cumplido** (tuplas `MARCAS`, `CALIDADES`, `CATEGORIAS`, `DISPONIBLE`, `ANIOS`; conjuntos en las comprensiones de `menu.py`). |
| 5 | Al menos una lista por comprensión o lambda | **Cumplido** (comprensiones en `menu.py` e `informe.py`). |
| 6 | Entidad con diccionario de diccionarios y ≥ 5 atributos | **Cumplido** (7 atributos por auto). |
| 7 | Menú en consola con CRUD completo | **Cumplido** (`crud.py`). |
| 8 | Al menos un reporte matricial | **Parcial** — `ver_stock` arma la tabla con pandas (DataFrame) y la reutilizan `informe_disponibilidad` y `estado_rentas`; `informe_estadisticas` sigue siendo un stub. |

---

## 3. Estructura del proyecto

```
TP - semester-two-group-one/
├── menu.py                # Punto de entrada: menús de usuario y empresa.
├── crud.py                # CRUD del catálogo + persistencia + ver_stock (pandas).
├── usuarios.py            # Ingreso y registro de usuarios.
├── informe.py             # Constantes, rutas y precarga (autos y usuarios).
├── pruebas.py             # Archivo vacío (placeholder, sin contenido).
├── tempCodeRunnerFile.py  # Resto de la extensión Code Runner (no es del proyecto).
├── autos.json             # Catálogo de autos (persistencia; se genera al ejecutar).
├── usuarios.json          # Usuarios (persistencia; se genera al ejecutar).
└── documentacion/
    ├── README.md                    # Índice de la documentación.
    ├── DOCUMENTACION_TECNICA.md     # Este archivo.
    ├── MANUAL_DE_USUARIO.md         # Manual para el usuario final.
    └── presentacion_rentar.html     # Presentación HTML del flujo de alquiler.
```

### 3.1 Dependencias entre módulos

```
informe.py   (constantes + rutas; no importa otros módulos del TP)
    ▲
    ├── crud.py       (import informe + pandas)
    ├── usuarios.py   (import informe)
    └── menu.py       (import informe, crud y usuarios)   ← programa principal
```

- `crud.py` se puede ejecutar solo (`python crud.py`) e importa `informe` y `pandas`.
- `menu.py` es el programa principal e importa `crud` y `usuarios`.
- `informe.py` no depende de ningún otro módulo del TP.

---

## 4. Modelo de datos y persistencia

### 4.1 Catálogo de autos (`autos.json`)

Diccionario de diccionarios: la **clave es la patente** y el **valor** es otro
diccionario con los atributos del auto. Cada auto tiene **7 claves**:

```json
{
    "SVU580": {
        "marca": "fiat",
        "modelo": "fastback",
        "calidad": "nuevo",
        "año": 2007,
        "precio": 52,
        "categoria": "suv_crossover",
        "estado": true
    }
}
```

| Atributo | Tipo | Descripción / valores |
|----------|------|-----------------------|
| `marca` | str | `toyota`, `renault`, `fiat`, `peugeot`, `chevrolet` |
| `modelo` | str | Modelo (en minúsculas) |
| `calidad` | str | `nuevo`, `cuidado`, `usado` |
| `año` | int | Entre 2000 y 2026 |
| `precio` | int/float | Precio en dólares (positivo) |
| `categoria` | str | `sedan_hatchback`, `suv_crossover`, `pickup`, `monovolumen_mpv` |
| `estado` | bool | `true` = disponible; `false` = alquilado |

> **Nota (dato faltante):** `agregar_auto()` **no** crea la clave `estado`. Los autos
> dados de alta desde el CRUD quedan sin `estado`, y leerlos luego en
> `_mostrar_auto`, `ver_stock` o `rentar_auto` lanza `KeyError` (ver §9).

> **Nota (calidades):** la tupla `CALIDADES` es `("nuevo", "cuidado", "usado")`, pero
> algunos datos pueden contener `"como nuevo"`, que ya no está en la tupla; validar
> ese valor con el CRUD lo rechaza.

### 4.2 Usuarios (`usuarios.json`)

Diccionario `dni → datos`. Cada usuario guarda su contraseña y la lista de patentes
que tiene alquiladas:

```json
{
    "10101010": {
        "nombre": "Jorge",
        "clave": "1010",
        "autos_rentados": ["QRT509"]
    }
}
```

> Los alquileres ya **no** van a un archivo aparte: `rentar_auto` agrega la patente a
> `autos_rentados` del usuario y `devolver_auto` la quita.

### 4.3 Precarga (`informe_autos` / `informe_usuarios`)

La precarga no se escribe a mano: `informe.informe_autos(ruta, cant)` genera autos
aleatorios y **crea** el archivo **solo si no existe** (si ya existe, avisa y no lo
toca). Reglas de generación:

- Año aleatorio entre 2000 y 2026 (`ANIOS`).
- Patente: año ≥ 2016 → prefijo letras/dígitos (`AI119AS`); año < 2016 → 3 letras + 3 números (`QRT509`).
- Precio base 90, que baja **2.5** por cada año de antigüedad respecto de 2026.
- Marca y modelo al azar desde el diccionario `AUTOS`.
- La categoría se deduce buscando el modelo en `categorias_modelos`.
- `estado` inicial: `True` (disponible).

> **Importante:** `informe_autos` **ignora** el parámetro `cant_autos` y fuerza `25`
> internamente. `informe_usuarios` deja precargado un único usuario de ejemplo
> (DNI `10101010`, nombre `Jorge`, clave `1010`) para poder probar el ingreso.

---

## 5. Descripción de los módulos

### 5.1 `crud.py` — Catálogo y persistencia

| Función | Tipo | Descripción |
|---------|------|-------------|
| `_cargar_autos()` | Persistencia | Lee `autos.json` y lo devuelve como diccionario. |
| `_guardar_autos(autos)` | Persistencia | Sobreescribe `autos.json`. |
| `open_autos()` / `open_usuarios()` | Persistencia | Lecturas usadas por `menu.py` (devuelven `None` si falla). |
| `escribir_usuario(lista)` / `escribir_auto(lista)` | Persistencia | Sobreescriben `usuarios.json` / `autos.json`. |
| `_pedir_de_tupla`, `_pedir_entero`, `_pedir_float`, `_pedir_patente_existente` | Validación | Piden y validan datos. |
| `_mostrar_auto(patente, datos)` | Visualización | Imprime la ficha de un auto. |
| `ver_stock(base, rentados)` | **Read** | Tabla con pandas: `(1,0)` catálogo completo; `(0,1)` solo rentados. |
| `ver_auto()` | **Read** | Muestra la ficha de un auto según su patente. |
| `agregar_auto()` | **Create** | Da de alta un auto nuevo. |
| `modificar_estado_auto(patente, estado)` | **Update** | Marca un auto como disponible/no disponible en `autos.json`. |
| `modificar_auto()` | **Update** | Modifica campos de un auto existente. |
| `eliminar_auto()` | **Delete** | Elimina un auto por patente. |
| `menu_crud()` | Menú | Menú interactivo del CRUD. |

### 5.2 `menu.py` — Menú principal, alquileres e informes

| Función | Descripción |
|---------|-------------|
| `limpiar()` | Limpia la consola según el sistema operativo. |
| `rentar_auto(usu_info, lista_usu, lista_aut)` | Flujo de alquiler: categoría → modelo → patente. |
| `devolver_auto(usu_info, lista_usu)` | Registra la devolución de un auto alquilado. |
| `informe_disponibilidad()` | Tabla del catálogo completo (`cd.ver_stock(1,0)`). |
| `estado_rentas()` | Tabla de los autos rentados (`cd.ver_stock(0,1)`). |
| `informe_estadisticas()` | **Pendiente** (stub: imprime `"hola"`). |
| `menu_principal()` | Menú principal (usuario / empresa / salir). |
| `submenu_usuario()` | Ingresar / registrarse y luego alquilar / devolver. |
| `submenu_empresa()` | Submenú de informes. |

**Flujo de `rentar_auto()`:**

1. Lista las categorías y pide una opción.
2. Filtra los **modelos** disponibles de esa categoría (excluye los alquilados).
3. Filtra las **patentes** disponibles de ese modelo.
4. Marca el auto como no disponible (`modificar_estado_auto`) y agrega la patente a
   `autos_rentados` del usuario en `usuarios.json`.

Los filtros usan **listas/sets por comprensión** (Requisito 5).

**Flujo de `devolver_auto()`:** lista los autos del usuario, pide cuál devolver,
marca el auto como disponible y quita la patente de `autos_rentados`.

> **Carga de datos:** `submenu_usuario` recarga `usuarios.json` y `autos.json` desde
> disco antes de cada acción. Esto resolvió los bugs "error al ingresar" (usuario
> nuevo que no podía entrar) y "renta infinita" (auto que se podía alquilar dos veces
> en la misma sesión).

### 5.3 `usuarios.py` — Ingreso y registro

| Función | Descripción |
|---------|-------------|
| `ingresa_usuario(lista)` | Login por DNI + contraseña; devuelve `[dni, nombre, autos_rentados]`. |
| `registro_usuario(lista)` | Alta de un usuario nuevo en `usuarios.json`. |

### 5.4 `informe.py` — Constantes y precarga

| Elemento | Descripción |
|----------|-------------|
| `AUTOS`, `MARCAS`, `CALIDADES`, `DISPONIBLE`, `ANIOS`, `CATEGORIAS` | Constantes/tuplas compartidas. |
| `categorias_modelos`, `preset`, `letras`, `numeros` | Datos auxiliares de la precarga. |
| `RUTA_AUTOS_JSON`, `RUTA_USUARIOS_JSON` | Rutas relativas de los archivos de datos. |
| `informe_autos(ruta, cant)` | Genera 25 autos aleatorios (solo si el archivo no existe). |
| `informe_usuarios(ruta)` | Crea `usuarios.json` con 1 usuario de ejemplo (si no existe). |

---

## 6. Requisitos técnicos

- **Lenguaje:** Python 3. Las f-strings con comillas dobles anidadas
  (`f"...{lista[dni]["nombre"]}..."` en `usuarios.py`) requieren **Python 3.12+**.
- **Dependencia externa:** **pandas** (usada por `ver_stock`). Se instala con
  `pip install pandas`.
- **Biblioteca estándar:** `json`, `os`, `random`.
- **Sistema operativo:** multiplataforma (`limpiar()` usa `cls` en Windows y `clear`
  en Linux/macOS).
- **Archivos necesarios:** `autos.json` y `usuarios.json` en el mismo directorio
  desde donde se ejecuta el programa (se referencian por ruta relativa).

---

## 7. Instalación y ejecución

```bash
# 1) Ubicarse en la carpeta del proyecto
cd "TP - semester-two-group-one"

# 2) Instalar la dependencia (solo la primera vez)
pip install pandas

# 3) Generar los archivos de datos (si no existen)
python informe.py

# 4) Ejecutar la aplicación principal (usuario y empresa)
python menu.py

# 5) Ejecutar SOLO el CRUD del catálogo (programa independiente)
python crud.py
```

> **Atención:** `menu.py` **no** genera los datos. Si `autos.json` o `usuarios.json`
> no existen, las lecturas devuelven `None` y el programa falla al ingresar o
> alquilar. Ejecutá `python informe.py` una vez para crearlos, o cargá el catálogo con
> `python crud.py`.

---

## 8. Manejo de errores (estado actual)

| Ubicación | Manejo actual | Mejora pendiente |
|-----------|---------------|------------------|
| `_pedir_float` (crud) | `try/except ValueError` | Ok |
| `_cargar_autos` (crud) | `try/except FileNotFoundError / OSError` | Devuelve `None` en `OSError` |
| `_guardar_autos` (crud) | `try/except FileNotFoundError / OSError` | Ok (avisa por pantalla) |
| `open_autos` / `open_usuarios` (crud) | `except OSError` | Devuelve `None`; el consumidor debería validarlo |
| `escribir_usuario` / `escribir_auto` (crud) | Sin `try/except` | Agregar manejo de `OSError` |
| `_pedir_entero` (crud) | Solo `.isdigit()` | Usar `try/except ValueError` |
| `ingresa_usuario` / `registro_usuario` (usuarios) | `except` genérico | Excepciones específicas |
| Menús de `menu.py` | `except` genérico | Excepciones específicas |

---

## 9. Problemas conocidos y pendientes

1. **~~`devolver_auto` / `rentar_auto` rotos por la firma~~ (RESUELTO).**
   `submenu_usuario` llamaba a `devolver_auto` con 3 argumentos (recibe 2) y a
   `rentar_auto` con 2 (recibe 3); los `TypeError` quedaban ocultos por el `except`
   del submenú, así que las opciones [1] y [2] "no hacían nada". Ya están corregidas
   ambas llamadas.
2. **`agregar_auto` no guarda `estado`.** Los autos creados desde el CRUD quedan sin
   esa clave y luego `_mostrar_auto`, `ver_stock` y `rentar_auto` lanzan `KeyError`.
3. **`informe_estadisticas()` es un stub** (imprime `"hola"`); falta el reporte
   matricial (Requisito 8).
4. **`modificar_estado_auto`** escribe en la ruta `"autos.json"` escrita a mano, en
   lugar de usar la constante `RUTA_AUTOS`, y lanza `KeyError` si la patente no existe.
5. **`_pedir_patente_existente`** devuelve `"0"` (o `None` si el catálogo está vacío);
   con ese valor, `ver_auto`, `modificar_auto` y `eliminar_auto` acceden a una clave
   inexistente y lanzan `KeyError`.
6. **`modificar_auto`**: `int(opcion)` lanza `ValueError` con entradas no numéricas, y
   el mapeo de campos es fijo (1–7) aunque el auto tenga menos claves.
7. **`except` genéricos** en varios puntos (el Requisito 1 pide manejo específico).
8. **Sin archivos de datos** `open_autos`/`open_usuarios` devuelven `None`.
9. **`CALIDADES`** no incluye `"como nuevo"`, presente en algunos datos.
10. **`DISPONIBLE`** usa textos (`"true"`/`"false"`) mientras que `estado` se guarda
    como booleano; conviven ambos formatos.
11. **`import informe as inf` (y `json`) sin uso** en `menu.py`.
12. **`limpiar` sin paréntesis** en `registro_usuario` (`usuarios.py`): no limpia.
13. **Archivos ajenos al código**: `tempCodeRunnerFile.py` (resto de Code Runner),
    `pruebas.py` (vacío) y los `__pycache__/*.pyc` versionados.

---

## 10. Ejemplo de reporte matricial

`ver_stock` arma la tabla con pandas y la imprime transpuesta (una fila por auto):

```
------------- CATALOGO DE AUTOS -------------
              SVU580        ...
marca         fiat
modelo        fastback
calidad       nuevo
año           2007
precio        $52
categoria     suv_crossover
estado        disponible
---------------------------------------------
```

En su forma más simple, una matriz es una **lista de listas**:

```python
matriz = [
    ["Categoría", "Cantidad"],
    ["sedan_hatchback", 9],
    ["suv_crossover", 11],
    ["pickup", 3],
    ["monovolumen_mpv", 3],
]
```

> Los valores son ilustrativos y cambian según el contenido de `autos.json`.
