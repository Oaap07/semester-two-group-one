# Documentación Técnica — Sistema de Gestión de Concesionaria

**Proyecto:** TPO – SPRINT (Programación I)
**Institución:** Facultad de Ingeniería Informática
**Tema:** Administración de una concesionaria (catálogo de autos + alquileres)
**Lenguaje:** Python 3
**Persistencia:** Archivos JSON

---

## 1. Descripción general

El sistema es una aplicación de consola que administra el catálogo de autos de una
concesionaria y permite alquilar y devolver vehículos. Está compuesto por varios
módulos de Python que comparten información a través de archivos JSON:

- El **catálogo** de autos se guarda en `autos.json`.
- Los **autos alquilados** se registran en `rentados.json`.

La aplicación ofrece:

- Un **CRUD completo** del catálogo (Crear, Leer, Actualizar, Eliminar).
- Un **menú de usuario** para alquilar y devolver autos.
- Un **menú de empresa** para consultar informes.
- Un **generador de precarga** de autos aleatorios (`informe_autos`).

---

## 2. Objetivo y requisitos del trabajo práctico

El enunciado (TPO – SPRINT) pide aplicar lo aprendido sobre **archivos/JSON** y
**manejo de excepciones**. Los requisitos mínimos son:

| # | Requisito | Estado en el código |
|---|-----------|---------------------|
| 1 | Manejo de excepciones en ingreso de datos, conversiones y archivos | **Parcial** (solo en `_pedir_float` y `cargar_rentados`) |
| 2 | Persistencia en JSON (CUD sobreescriben; Read lee) | **Cumplido** (`autos.json`, `rentados.json`) |
| 3 | Precarga desde archivo inicial (mínimo 5 registros) | **Cumplido** (`informe_autos` genera el archivo) |
| 4 | Uso de tupla o conjunto en la lógica | **Cumplido** (tuplas `MARCAS`, `CALIDAD`, etc.) |
| 5 | Al menos una lista por comprensión o lambda | **Cumplido** (comprensiones en `menu.py` e `informe.py`) |
| 6 | Entidad con diccionario de diccionarios y ≥ 5 atributos | **Cumplido** (6 atributos por auto) |
| 7 | Menú en consola con CRUD completo | **Cumplido** (`crud.py`) |
| 8 | Al menos un reporte matricial | **Pendiente** (ver sección 9) |

---

## 3. Estructura del proyecto

```
TP - semester-two-group-one/
├── menu.py          # Punto de entrada principal: menús de usuario y empresa.
├── crud.py          # CRUD del catálogo de autos (se ejecuta de forma independiente).
├── informe.py       # Generación de datos (precarga) e informes.
├── pruebas.py       # Script auxiliar de prueba (imprime las marcas del catálogo).
├── autos.json       # Datos del catálogo de autos (persistencia).
├── rentados.json    # Datos de los autos alquilados (persistencia).
└── documentacion/
    ├── DOCUMENTACION_TECNICA.md   # Este archivo.
    └── MANUAL_DE_USUARIO.md       # Manual para el usuario final.
```

### 3.1 Dependencias entre módulos

```
        menu.py  ──────import──────►  informe.py
           │                              │
           │ escribe/lee                  │ genera
           ▼                              ▼
     autos.json / rentados.json      autos.json
     (persistencia)                  (precarga aleatoria)

        crud.py  ──── lee/escribe ───►  autos.json
        (independiente de menu.py)

        pruebas.py ── lee ──► autos.json  (solo verificación)
```

**Aclaración importante:** `menu.py` y `crud.py` **no se importan entre sí**.
El CRUD se ejecuta por separado con `python crud.py`. `menu.py` es el programa
principal de alquileres e informes.

---

## 4. Modelo de datos y persistencia

### 4.1 Entidad principal: diccionario de diccionarios

El catálogo (`autos.json`) es un diccionario cuya **clave es la patente** del auto
y cuyo **valor es otro diccionario** con sus atributos. Cada auto tiene **6 atributos**
(se cumple el mínimo de 5 exigido por el TP).

```json
{
    "SVU580": {
        "marca": "fiat",
        "modelo": "fastback",
        "calidad": "nuevo",
        "año": 2007,
        "precio": 52,
        "categoria": "suv_crossover"
    }
}
```

| Atributo | Tipo | Descripción / valores válidos |
|----------|------|-------------------------------|
| `marca` | str | `toyota`, `renault`, `fiat`, `peugeot`, `chevrloet` |
| `modelo` | str | Modelo del auto (en minúsculas) |
| `calidad` | str | `nuevo`, `como nuevo`, `usado` |
| `año` | int | Entre 2000 y 2026 |
| `precio` | float/int | Precio en dólares (positivo) |
| `categoria` | str | `sedan_hatchback`, `suv_crossover`, `pickup`, `monovolumen_mpv` |

### 4.2 Autos rentados (`rentados.json`)

Es un diccionario con la misma forma: **patente → datos del auto**.

```json
{
    "QRT509": { "modelo": "yaris", "precio": 62, "año": 2012 }
}
```

> **Nota técnica (inconsistencia conocida):** `rentar_auto()` en `menu.py` copia la
> ficha **completa** del auto (6 atributos) al diccionario de rentados, mientras que
> el archivo actual `rentados.json` solo contiene 3 atributos (`modelo`, `precio`,
> `año`). No se debe asumir un conjunto fijo de claves al leer rentados sin validarlo.

### 4.3 Precarga (`informe_autos`)

La precarga **no** se escribe a mano: `informe.informe_autos(ruta, cant)` genera
autos aleatorios y **sobreescribe** el archivo indicado. Reglas de generación:

- Año aleatorio entre 2000 y 2026.
- Patente:
  - Año ≥ 2016 → prefijo de letras + dígitos (formato tipo `AI119AS`).
  - Año < 2016 → 3 letras + 3 números (formato tipo `QRT509`).
- Precio base 90, que baja 2 por cada año de antigüedad respecto de 2026.
- Marca y modelo elegidos al azar desde las tuplas `AUTOS`.
- La categoría se deduce buscando el modelo en el diccionario `categorías`.

> **Importante:** `informe_autos` fuerza `cant_autos = 25` internamente e
> **ignora** el valor del parámetro. Además, `menu.py` lo invoca al arrancar, por lo
> que **el catálogo se regenera al iniciar la aplicación** (ver sección 7).

---

## 5. Descripción de los módulos

### 5.1 `crud.py` — Gestión del catálogo

Implementa el CRUD completo. Funciones principales:

| Función | Tipo | Descripción |
|---------|------|-------------|
| `_cargar_autos()` | Persistencia | Lee `autos.json` y lo convierte a diccionario. |
| `_guardar_autos(autos)` | Persistencia | Sobreescribe `autos.json` con la última versión. |
| `_pedir_de_tupla(etiqueta, opciones)` | Validación | Pide un valor dentro de una tupla permitida. |
| `_pedir_entero(etiqueta, min, max)` | Validación | Pide un entero dentro de un rango. |
| `_pedir_float(etiqueta)` | Validación | Pide un decimal positivo (acepta coma o punto). |
| `_pedir_patente_existente(autos)` | Validación | Pide una patente ya existente. |
| `_mostrar_auto(patente, datos)` | Visualización | Imprime la ficha de un auto. |
| `ver_autos()` / `ver_auto()` | **Read** | Muestra todo el catálogo o un auto. |
| `agregar_auto()` | **Create** | Da de alta un auto nuevo. |
| `modificar_auto()` | **Update** | Modifica campos de un auto existente. |
| `eliminar_auto()` | **Delete** | Elimina un auto por patente. |
| `menu_crud()` | Menú | Menú interactivo del CRUD. |

### 5.2 `menu.py` — Menú principal y alquileres

| Función | Descripción |
|---------|-------------|
| `limpiar()` | Limpia la consola según el sistema operativo. |
| `cargar_rentados()` / `guardar_rentados()` | Persistencia de `rentados.json`. |
| `rentar_auto()` | Flujo de alquiler: categoría → modelo → patente. |
| `devolver_auto()` | Registra devolución (**incompleto**). |
| `estado_rentas()` | Muestra autos alquilados (**incompleto**). |
| `menu_principal()` | Menú principal (usuario / empresa / salir). |
| `submenu_usuario()` | Submenú de alquileres. |
| `submenu_empresa()` | Submenú de informes. |

**Flujo de `rentar_auto()`:**

1. Lista las categorías y pide una opción.
2. Filtra los **modelos** disponibles de esa categoría (excluyendo los ya rentados).
3. Filtra las **patentes** de ese modelo (excluyendo las ya rentadas).
4. Registra el alquiler en `rentados.json` y confirma.

Los filtros usan **comprensiones de listas/conjuntos**, lo que cumple el requisito 5
del TP (lista por comprensión).

### 5.3 `informe.py` — Generación de datos e informes

| Función | Estado | Descripción |
|---------|--------|-------------|
| `informe_autos(ruta_archivo, cant_autos)` | Implementada | Genera y guarda una precarga aleatoria de autos. |
| `informe_disponibilidad()` | **NO existe** | Es invocada por `menu.py` pero no está definida. |
| `informe_estadisticas()` | **NO existe** | Es invocada por `menu.py` pero no está definida. |

> **Advertencia:** las opciones `[1]` y `[2]` del submenú de empresa llaman a
> funciones inexistentes. Al elegirlas, el programa lanza `AttributeError` y se
> interrumpe. Estas funciones son las que deben implementar el **reporte matricial**
> (requisito 8).

### 5.4 `pruebas.py` — Script auxiliar

Script mínimo para verificar la lectura del catálogo: abre `autos.json` y muestra
la marca de cada auto. No forma parte del flujo principal.

---

## 6. Requisitos técnicos

- **Lenguaje:** Python 3 (se recomienda **3.10+**; requiere 3.9+ por las anotaciones
  de tipo como `dict[dict]`).
- **Dependencias del código:** solo la **biblioteca estándar**
  (`json`, `os`, `random`). No requiere instalación de paquetes.
- **Dependencias recomendadas (no usadas aún):** `NumPy`, `Pandas` y `Matplotlib`
  para construir el reporte matricial (requisito 8).
- **Sistema operativo:** multiplataforma. `limpiar()` usa `cls` en Windows y
  `clear` en Linux/macOS.
- **Archivos necesarios:** `autos.json` y `rentados.json` en el mismo directorio
  que los módulos (se referencian por ruta relativa).

---

## 7. Instalación y ejecución

No hay instalación de dependencias (solo librería estándar).

```bash
# 1) Ubicarse en la carpeta del proyecto
cd "TP - semester-two-group-one"

# 2) Ejecutar la aplicación principal (menús de usuario y empresa)
python menu.py

# 3) Ejecutar SOLO el CRUD del catálogo (programa independiente)
python crud.py

# 4) Script de verificación (muestra las marcas del catálogo)
python pruebas.py
```

> **Atención:** al iniciar `menu.py`, se ejecuta `informe.informe_autos("autos.json", 25)`,
> que **regenera y sobreescribe** `autos.json` con 25 autos aleatorios. Si se desea
> conservar un catálogo, ejecutar el CRUD con `python crud.py` en lugar de `menu.py`,
> o quitar temporalmente esa llamada de precarga.

---

## 8. Manejo de errores (estado actual)

| Ubicación | Manejo actual | Mejora pendiente |
|-----------|---------------|------------------|
| `_pedir_float` (crud) | `try/except ValueError` | Ok |
| `cargar_rentados` (menu) | `except FileNotFoundError` | Agregar `JSONDecodeError`, `OSError` |
| `_cargar_autos` / `_guardar_autos` | Sin `try/except` | Agregar manejo de archivo/JSON |
| `_pedir_entero` | Solo `.isdigit()` | Usar `try/except ValueError` |
| Lectura de `autos.json` en `menu.rentar_auto` | Sin `try/except` | Agregar manejo |
| Llamadas a `informe.*` | `except` genérico (mal uso) | Excepciones específicas |

---

## 9. Pendientes para cumplir el TP

1. **Requisito 1 — Manejo de excepciones:** envolver la carga/guardado de archivos
   y las conversiones en `try/except`.
2. **Requisito 8 — Reporte matricial:** implementar `informe_disponibilidad()` e
   `informe_estadisticas()` en `informe.py`, generando al menos un reporte matricial
   (lista de listas), idealmente con NumPy/Pandas/Matplotlib.
3. **Completar `devolver_auto()`:** listar rentados, pedir patente, eliminarla de
   `rentados.json` y confirmar.
4. **Completar `estado_rentas()`:** mostrar la ficha de cada auto rentado.
5. **Corregir la llamada a `informe_autos`:** respetar el parámetro `cant_autos`
   y/o evitar sobrescribir el catálogo al arrancar.
6. **Unificar la estructura de `rentados.json`** con la escrita por `rentar_auto()`.
7. **Corregir el error tipográfico** `chevrloet` (debería ser `chevrolet`) de forma
   consistente en `crud.py` e `informe.py`.

---

## 10. Ejemplo de reporte matricial (formato esperado)

Un reporte matricial representa información procesada en forma de tabla. Por ejemplo,
conteo de autos por categoría:

```
+------------------------+----------+
| Categoría              | Cantidad |
+------------------------+----------+
| sedan_hatchback        |        9 |
| suv_crossover          |       11 |
| pickup                 |        3 |
| monovolumen_mpv        |        3 |
+------------------------+----------+
```

En código, esa matriz se arma como una **lista de listas**:

```python
matriz = [
    ["Categoría", "Cantidad"],
    ["sedan_hatchback", 9],
    ["suv_crossover", 11],
    ["pickup", 3],
    ["monovolumen_mpv", 3],
]
```

> Los valores de la tabla son ilustrativos del conjunto de datos actual y cambian
> según el contenido de `autos.json`.
