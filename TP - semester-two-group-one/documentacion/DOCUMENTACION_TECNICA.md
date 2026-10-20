# Documentación Técnica — Sistema de Gestión de Concesionaria

**Proyecto:** TPO – SPRINT (Programación I)
**Institución:** Facultad de Ingeniería Informática
**Tema:** Administración de una concesionaria (catálogo de autos + alquileres)
**Lenguaje:** Python 3
**Persistencia:** Archivos JSON (`autos.json` y `usuarios.json`)

---

## 1. Descripción general

Aplicación de consola que administra el catálogo de autos de una concesionaria y
permite alquilar y devolver vehículos. Está dividida en **cinco módulos** de Python
que comparten datos a través de archivos JSON:

- `menu.py` — programa principal: menús de usuario y de empresa.
- `crud.py` — alta, baja, modificación y consulta del catálogo, más la persistencia.
- `usuarios.py` — ingreso (login) y registro de usuarios.
- `informe.py` — constantes compartidas, rutas de archivos, precarga y recaudación.
- `pruebas.py` — suite de pruebas automáticas con **pytest** (95 pruebas).

Archivos de datos (se crean en tiempo de ejecución con `python informe.py`):

- `autos.json` — el catálogo: `patente → {atributos del auto}`.
- `usuarios.json` — los usuarios: `dni → {nombre, clave, autos_rentados}`.

> Ya **no** existe `rentados.json`: los autos alquilados por cada usuario se guardan
> como una lista de patentes dentro de su registro en `usuarios.json`.

La aplicación ofrece:

- Un **CRUD completo** del catálogo (Crear, Leer, Actualizar, Eliminar).
- Un **menú de usuario** para ingresar/registrarse, alquilar y devolver autos.
- Un **menú de empresa** con informes: catálogo completo, disponibilidad, autos
  rentados y estadísticas generales (gráficos con pandas + matplotlib).
- Una **precarga** de autos y usuarios aleatorios (`informe.informe_autos` /
  `informe.informe_usuarios`).
- Una **suite de pruebas** (`pruebas.py`) que verifica el CRUD, la persistencia, las
  validaciones, el alquiler y los informes.

---

## 2. Estructura del proyecto

```
TP - semester-two-group-one/
├── menu.py                # Punto de entrada: menús de usuario y empresa.
├── crud.py                # CRUD del catálogo + persistencia + ver_stock (pandas).
├── usuarios.py            # Ingreso y registro de usuarios.
├── informe.py             # Constantes, rutas, precarga y recaudación (pozo).
├── pruebas.py             # Suite de pruebas automáticas (pytest).
├── autos.json             # Catálogo de autos (persistencia; se genera al ejecutar).
├── usuarios.json          # Usuarios (persistencia; se genera al ejecutar).
└── documentacion/
    ├── README.md                    # Índice de la documentación.
    ├── DOCUMENTACION_TECNICA.md     # Este archivo.
    ├── MANUAL_DE_USUARIO.md         # Manual para el usuario final.
    └── presentacion_rentar.html     # Presentación HTML del flujo de alquiler.
```

### 2.1 Dependencias entre módulos

```
informe.py   (constantes + rutas; no importa otros módulos del TP)
    ▲
    ├── crud.py       (import informe + pandas)
    ├── usuarios.py   (import informe)
    └── menu.py       (import informe, crud y usuarios)   ← programa principal
```

- `crud.py` se puede ejecutar solo (`python crud.py`) e importa `informe` y `pandas`.
- `menu.py` es el programa principal e importa `crud`, `usuarios` e `informe`.
- `informe.py` no depende de ningún otro módulo del TP.
- `pruebas.py` importa los cuatro módulos y corre con `pytest`.

---

## 3. Modelo de datos y persistencia

### 3.1 Catálogo de autos (`autos.json`)

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

> **Nota:** `agregar_auto()` crea el auto con las **7 claves del esquema** (incluido
> `"estado": True`), así que un auto dado de alta desde el CRUD queda disponible y se
> muestra sin problemas en `_mostrar_auto`, `ver_stock` y `rentar_auto`.

> **Nota (calidades):** `CALIDADES` es `("nuevo", "cuidado", "usado")` y con esos
> valores se precarga y se valida el catálogo.

### 3.2 Usuarios (`usuarios.json`)

Diccionario `dni → datos`. Cada usuario guarda su contraseña y la lista de patentes
que tiene alquiladas:

```json
{
    "95823279": {
        "nombre": "Jorge Adrian Gonzalez Padron",
        "clave": "1234",
        "autos_rentados": ["QRT509"]
    }
}
```

> Los alquileres ya **no** van a un archivo aparte: `rentar_auto` agrega la patente a
> `autos_rentados` del usuario y `devolver_auto` la quita.

### 3.3 Precarga (`informe_autos` / `informe_usuarios`)

La precarga no se escribe a mano: `informe.informe_autos(ruta, cant)` genera autos
aleatorios y **crea** el archivo **solo si no existe** (si ya existe, avisa y no lo
toca). Reglas de generación:

- Año aleatorio entre 2000 y 2026 (`ANIOS`).
- Patente: año ≥ 2016 → prefijo letras/dígitos (`AI119AS`); año < 2016 → 3 letras + 3 números (`QRT509`).
- Precio base 90, que baja **2.5** por cada año de antigüedad respecto de 2026.
- Marca y modelo al azar desde el diccionario `AUTOS`.
- La categoría se deduce buscando el modelo en `categorias_modelos`.
- `estado` inicial: `True` (disponible).

> **Precarga:** `informe_autos` genera un catálogo fijo de **25 autos**.
> `informe_usuarios` deja precargados **3 usuarios de ejemplo**, todos con clave
> `1234` (DNI `95823279`, `4817866` y `46280291`), para poder probar el ingreso.

---

## 4. Descripción de los módulos

### 4.1 `crud.py` — Catálogo y persistencia

| Función | Tipo | Descripción |
|---------|------|-------------|
| `_cargar_autos()` | Persistencia | Lee `autos.json` y lo devuelve como diccionario (`{}` si falla). |
| `_guardar_autos(autos)` | Persistencia | Sobreescribe `autos.json`. |
| `open_autos()` / `open_usuarios()` | Persistencia | Lecturas usadas por `menu.py` (devuelven `{}` si falla). |
| `escribir_usuario(lista)` / `escribir_auto(lista)` | Persistencia | Sobreescriben `usuarios.json` / `autos.json`. |
| `_pedir_de_tupla`, `_pedir_entero`, `_pedir_float`, `_pedir_patente_existente` | Validación | Piden y validan datos. |
| `_mostrar_auto(patente, datos)` | Visualización | Imprime la ficha de un auto. |
| `ver_stock(base, rentados)` | **Read** | Tabla con pandas: `(1,0)` catálogo completo; `(1,1)` solo disponibles; `(0,1)` solo rentados. |
| `ver_auto()` | **Read** | Muestra la ficha de un auto según su patente. |
| `agregar_auto()` | **Create** | Da de alta un auto nuevo (con las 7 claves). |
| `modificar_estado_auto(patente, estado)` | **Update** | Invierte el estado de un auto en `autos.json`. |
| `modificar_auto()` | **Update** | Modifica campos de un auto existente. |
| `eliminar_auto()` | **Delete** | Elimina un auto por patente. |
| `menu_crud()` | Menú | Menú interactivo del CRUD. |

### 4.2 `menu.py` — Menú principal, alquileres e informes

| Función | Descripción |
|---------|-------------|
| `limpiar()` | Limpia la consola según el sistema operativo. |
| `rentar_auto(usu_info, lista_usu, lista_aut, pozo)` | Flujo de alquiler: categoría → modelo → patente; acumula en `pozo`. |
| `devolver_auto(usu_info, lista_usu)` | Registra la devolución de un auto alquilado. |
| `ver_catalogo()` | Tabla del catálogo completo (`cd.ver_stock(1,0)`). |
| `informe_disponibilidad()` | Tabla de los autos disponibles (`cd.ver_stock(1,1)`). |
| `estado_rentas()` | Tabla de los autos rentados (`cd.ver_stock(0,1)`). |
| `informe_estadisticas()` | Gráficos del catálogo: barras de autos disponibles por marca y torta disponible/rentado (pandas + matplotlib). |
| `menu_principal()` | Menú principal (usuario / empresa / salir). |
| `submenu_usuario()` | Ingresar / registrarse y luego alquilar / devolver. |
| `submenu_empresa()` | Submenú de informes (4 opciones). |

**Flujo de `rentar_auto()`:**

1. Lista las categorías y pide una opción.
2. Filtra los **modelos** disponibles de esa categoría (excluye los alquilados).
3. Filtra las **patentes** disponibles de ese modelo.
4. Pide los días de alquiler, acumula `días × precio` en `pozo`, marca el auto como no
   disponible (`modificar_estado_auto`) y agrega la patente a `autos_rentados` del
   usuario en `usuarios.json`.

Los filtros usan **listas/sets por comprensión**. La recaudación vive en
`informe.pozo` y se le pasa a la función como cuarto argumento.

**Flujo de `devolver_auto()`:** lista los autos del usuario, pide cuál devolver,
marca el auto como disponible y quita la patente de `autos_rentados`.

> **Carga de datos:** `submenu_usuario` recarga `usuarios.json` y `autos.json` desde
> disco antes de cada acción, para trabajar siempre con el estado más reciente de los
> archivos.

### 4.3 `usuarios.py` — Ingreso y registro

| Función | Descripción |
|---------|-------------|
| `ingresa_usuario(lista)` | Login por DNI + contraseña; devuelve `[dni, nombre, autos_rentados]`. |
| `registro_usuario(lista)` | Alta de un usuario nuevo en `usuarios.json`. |

### 4.4 `informe.py` — Constantes y precarga

| Elemento | Descripción |
|----------|-------------|
| `AUTOS`, `MARCAS`, `CALIDADES`, `DISPONIBLE`, `ANIOS`, `CATEGORIAS` | Constantes/tuplas compartidas. |
| `categorias_modelos`, `preset`, `letras`, `numeros` | Datos auxiliares de la precarga. |
| `RUTA_AUTOS_JSON`, `RUTA_USUARIOS_JSON` | Rutas relativas de los archivos de datos. |
| `pozo` | Recaudación acumulada de los alquileres (la actualiza `rentar_auto`). |
| `informe_autos(ruta, cant)` | Genera 25 autos aleatorios (solo si el archivo no existe). |
| `informe_usuarios(ruta)` | Crea `usuarios.json` con 3 usuarios de ejemplo (si no existe). |

---

## 5. Requisitos técnicos

- **Lenguaje:** Python 3. Las f-strings con comillas dobles anidadas
  (`f"...{lista[dni]["nombre"]}..."` en `usuarios.py`) requieren **Python 3.12+**.
- **Dependencias externas:** **pandas** (tablas de los informes) y **matplotlib**
  (gráficos de `informe_estadisticas`). Se instalan con
  `pip install pandas matplotlib`.
- **Biblioteca estándar:** `json`, `os`, `random`.
- **Sistema operativo:** multiplataforma (`limpiar()` usa `cls` en Windows y `clear`
  en Linux/macOS).
- **Archivos necesarios:** `autos.json` y `usuarios.json` en el mismo directorio
  desde donde se ejecuta el programa (se referencian por ruta relativa).

---

## 6. Instalación y ejecución

```bash
# 1) Ubicarse en la carpeta del proyecto
cd "TP - semester-two-group-one"

# 2) Instalar las dependencias (solo la primera vez)
pip install pandas matplotlib

# 3) Generar los archivos de datos (si no existen)
python informe.py

# 4) Ejecutar la aplicación principal (usuario y empresa)
python menu.py

# 5) Ejecutar SOLO el CRUD del catálogo (programa independiente)
python crud.py

# 6) Correr la suite de pruebas
python pruebas.py
```

> **Datos de arranque:** al iniciarse, `menu.py` precarga `usuarios.json` y
> `autos.json` si no existen (o si están vacíos), y luego abre el menú principal.
> También se pueden generar a mano con `python informe.py`, o cargar el catálogo con
> `python crud.py`. Si faltan, las lecturas devuelven `{}` y el programa sigue
> funcionando, simplemente sin datos.

---

## 7. Ejemplo de reporte matricial

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

---

## 8. Pruebas automáticas (`pruebas.py`)

La suite usa **pytest** y aísla cada prueba en un directorio temporal propio (fixture
`entorno`), así que **no** toca los archivos reales del proyecto. La entrada por teclado
se simula con el helper `guion()`. Las pruebas de los gráficos usan el backend `Agg`
de matplotlib (sin ventana).

Estado actual: **95 pruebas que pasan** y **2 casos límite marcados como `xfail`**.

```bash
pip install pytest
python -m pytest pruebas.py -v   # o simplemente: python pruebas.py
```

Cobertura por área:

| Área | Qué verifica |
|------|--------------|
| Persistencia | `_cargar_autos` / `_guardar_autos`, `open_autos` / `open_usuarios`, `escribir_auto` / `escribir_usuario`, archivos ausentes/corruptos/no diccionario. |
| Validaciones | `_entrada`, `_pedir_patente_existente` (cancelar con `"0"`), `_pedir_entero`, `_pedir_float`, `_pedir_de_tupla`. |
| Lecturas | `ver_stock` en sus tres modos (incluidos los avisos de listas vacías), `ver_auto`, `_mostrar_auto`. |
| CRUD | Alta con las 7 claves, patente duplicada/vacía, modificación de cada campo, borrado, `modificar_estado_auto`. |
| Usuarios | Ingreso (clave incorrecta, DNI inexistente/inválido, cancelación) y registro (claves distintas, DNI duplicado, cancelación). |
| Alquiler | `rentar_auto` y `devolver_auto`: el estado pasa a `False` y vuelve a `True`, y la patente entra/sale de `autos_rentados`. |
| Navegación | `menu_principal`, `submenu_usuario`, `submenu_empresa`, `estado_rentas`. |
| Informes/datos | `informe_disponibilidad`, `estado_rentas`, `informe_estadisticas` (con catálogo y con catálogo vacío), `informe_autos`, `informe_usuarios`. |
| Casos límite | `ver_stock` con un auto sin la clave `estado` y `registro_usuario` con un DNI de menos de 8 dígitos (marcados como `xfail`). |
