# Manual de Usuario — Sistema de Gestión de Concesionaria

**Proyecto:** TPO – SPRINT (Programación I)
**Tema:** Administración de una concesionaria (catálogo de autos + alquileres)
**Tipo de aplicación:** Programa de consola (línea de comandos)

Bienvenido al manual de usuario. Aquí se explica, paso a paso y sin tecnicismos,
cómo usar el sistema para administrar el catálogo de autos, registrarte, alquilar
vehículos y consultar información.

---

## 1. ¿Qué hace este sistema?

El sistema permite:

- **Administrar el catálogo de autos**: ver, agregar, modificar y eliminar autos.
- **Registrarse e ingresar** como usuario.
- **Alquilar autos** y registrar la operación.
- **Devolver** los autos alquilados.
- **Consultar informes** sobre las unidades (disponibilidad y autos rentados).

Todos los datos quedan guardados en dos archivos:

- `autos.json` → el catálogo de autos.
- `usuarios.json` → los usuarios y los autos que tienen alquilados.

---

## 2. Antes de empezar (requisitos)

- Tener instalado **Python 3** (versión **3.12** o superior).
- Instalar la biblioteca **pandas** (se usa para las tablas de los informes). En una
  terminal, una sola vez:

```bash
pip install pandas
```

- Abrir una terminal (CMD, PowerShell o Terminal), ubicarse en la carpeta del
  proyecto y **generar los archivos de datos** (si no existen):

```bash
cd "TP - semester-two-group-one"
python informe.py
```

Al ejecutar `informe.py` se crean `autos.json` (con 25 autos) y `usuarios.json` (con
un usuario de ejemplo). Si los archivos ya existen, no se modifican.

---

## 3. Inicio rápido

El sistema tiene **dos programas** que se ejecutan por separado:

| Quiero... | Ejecutar |
|-----------|----------|
| Registrarme, alquilar, devolver y ver informes | `python menu.py` |
| Administrar el catálogo (alta/baja/modificación) | `python crud.py` |

```bash
# Programa principal (usuario y empresa)
python menu.py

# Administrador del catálogo
python crud.py
```

> **Importante:** `menu.py` **no** genera los datos. Si `autos.json` o `usuarios.json`
> no existen, el programa falla al ingresar o alquilar. Creá los archivos con
> `python informe.py` antes de usar `menu.py`.

> **Usuario de ejemplo:** si generaste los datos con `informe.py`, podés ingresar con
> el **DNI `10101010`** y la **contraseña `1010`**.

---

## 4. Navegación: los menús

La aplicación funciona con **menús numerados**. Para elegir una opción, escribís el
número y presionás **Enter**. En casi todos los pasos podés escribir **[0]** para
volver al menú anterior.

### 4.1 Menú principal (`menu.py`)

```
--- MENÚ PRINCIPAL ---

[1] Menu de usuario.
[2] Menu de empresa.
-------------------------
[0] Salir.
```

- **[1] Menú de usuario:** ingresar/registrarse, alquilar y devolver autos.
- **[2] Menú de empresa:** ver informes.
- **[0] Salir:** cierra el programa.

### 4.2 Submenú de usuario (ingreso)

```
--- SUBMENÚ: USUARIOS ---

[1] Ingresar
[2] Registrarse
-------------------------
[0] Volver al menú principal
```

Después de **ingresar correctamente**, aparece el submenú de manejo de autos:

```
--- |USUARIOS| MENÚ: MANEJO DE AUTOS ---  [TU NOMBRE]

[1] Rentar auto.
[2] Devolver auto.
-------------------------
[0] Volver al menú principal
```

> **Atención:** para alquilar o devolver **primero tenés que ingresar o registrarte**.
> Si elegís [1] o [2] sin haberte identificado, volvés a este submenú de ingreso.

### 4.3 Submenú de empresa (informes)

```
--- SUBMENÚ: INFORMES ---

[1] Disponibilidad de unidades
[2] Estadisticas del mes
[3] Estado de autos rentados
[0] Volver al menú principal
```

- **[1] Disponibilidad:** muestra el catálogo completo como tabla.
- **[2] Estadísticas:** **pendiente** (todavía no muestra información).
- **[3] Estado de autos rentados:** muestra como tabla los autos que están alquilados.

### 4.4 Menú del CRUD (`crud.py`)

```
--- CRUD DE AUTOS ---
[1] Ver catálogo
[2] Ver un auto
[3] Agregar auto
[4] Modificar auto
[5] Eliminar auto
[0] Salir
```

---

## 5. Registrarse e ingresar

### 5.1 Registrarse — submenú de usuario → [2]

1. **DNI:** 8 dígitos numéricos. No puede repetirse.
2. **Nombre.**
3. **Contraseña**, y luego la **comprobación** de la misma.

Al terminar: *"¡Usuario [NOMBRE] registrado exitosamente!"*. El usuario queda
guardado en `usuarios.json`.

### 5.2 Ingresar — submenú de usuario → [1]

1. **DNI** de usuario.
2. **Contraseña**.

Si los datos son correctos, aparece *"Bienvenido/a [NOMBRE]!"* y se abre el submenú
de manejo de autos. Para salir en cualquier campo, escribí `0`.

> **Nota:** las contraseñas se guardan y se leen en minúsculas, por lo que no
> distinguen mayúsculas de minúsculas.

---

## 6. Guía de uso paso a paso (alquileres – `menu.py`)

### 6.1 Rentar un auto — manejo de autos → [1]

El sistema guía en tres pasos:

1. **Elegir categoría**:
   ```
   [1] Sedán / Hatchback
   [2] SUV / Crossover
   [3] Pick-up
   [4] Monovolumen / Utilitario (MPV)
   [0] Para ir a Sub menú
   ```
2. **Elegir modelo** entre los disponibles de esa categoría (los ya alquilados no
   aparecen).
3. **Elegir el auto (patente)** entre los disponibles, viendo calidad, año y precio.

Al confirmar, el auto queda marcado como **no disponible** en `autos.json` y su
patente se agrega a tus **autos rentados** en `usuarios.json`.

### 6.2 Devolver un auto — manejo de autos → [2]

1. Se listan tus autos alquilados.
2. Elegís cuál devolver.
3. El auto vuelve a quedar **disponible** y se quita de tu lista.

> **Nota:** si escribís `0` volvés al menú anterior sin devolver nada.

### 6.3 Informes — submenú de empresa → [1] y [3]

- **[1] Disponibilidad de unidades:** tabla con **todos** los autos y su estado.
- **[3] Estado de autos rentados:** tabla con **solo** los autos alquilados.

Las tablas se generan con pandas (reporte matricial). La opción **[2] Estadísticas
del mes** todavía está pendiente.

---

## 7. Guía de uso paso a paso (catálogo – `crud.py`)

### 7.1 Ver todo el catálogo — opción [1]

Muestra todos los autos guardados como tabla, con su ficha completa.

```
[SVU580]
	Marca: Fiat
	Modelo: Fastback
	Calidad: nuevo
	Año: 2007
	Precio: u$d 52.0
	Categoría: suv_crossover
	Estado: True
```

Si no hay autos, el sistema avisa: *"No hay autos en el catálogo."*

### 7.2 Ver un auto — opción [2]

1. El sistema pide la **patente**.
2. Si existe, muestra su ficha; si no, vuelve a pedirla.

### 7.3 Agregar un auto — opción [3]

1. Ingresá la **patente**. No puede repetirse (debe ser única).
2. Completá los campos; el sistema valida cada uno:

| Campo | Qué ingresar |
|-------|--------------|
| Marca | Una de: `toyota`, `renault`, `fiat`, `peugeot`, `chevrolet` |
| Modelo | Texto libre (se guarda en minúsculas) |
| Calidad | Una de: `nuevo`, `cuidado`, `usado` |
| Año | Número entero entre 2000 y 2026 |
| Precio | Número positivo (podés usar coma o punto) |
| Categoría | Una de: `sedan_hatchback`, `suv_crossover`, `pickup`, `monovolumen_mpv` |

Al terminar: *"Auto [PATENTE] agregado correctamente."*

> **Nota (bug conocido):** el alta del CRUD **no** guarda el campo `estado`, por lo
> que ese auto puede fallar al verse en el catálogo o al intentar alquilarlo. Está
> documentado en la documentación técnica.

### 7.4 Modificar un auto — opción [4]

1. Ingresá la patente del auto a modificar.
2. Se muestra el menú de campos con sus valores actuales:

```
--- Modificar auto [SVU580] ---
[1] Marca: fiat
[2] Modelo: fastback
[3] Calidad: nuevo
[4] Año: 2007
[5] Precio: 52
[6] Categoría: suv_crossover
[7] Estado: True
[0] Terminar
```

3. Elegí el número del campo a cambiar e ingresá el nuevo valor.
4. Podés modificar varios campos seguidos; cuando termines, elegí **[0] Terminar**.

### 7.5 Eliminar un auto — opción [5]

1. Ingresá la patente del auto a eliminar.
2. El sistema lo borra y confirma: *"Auto [PATENTE] eliminado correctamente."*

> **Cuidado:** la eliminación no se puede deshacer.

---

## 8. Reglas de validación de datos

El sistema evita datos incorrectos:

- **Patentes:** se convierten a mayúsculas y no pueden repetirse.
- **Marca / Calidad / Categoría:** solo aceptan los valores predefinidos.
- **Año:** obligatorio entero entre 2000 y 2026.
- **Precio:** número positivo (se acepta `50,5` o `50.5`).
- **DNI:** 8 dígitos numéricos.
- **Opciones de menú:** si ingresás una opción inválida, el sistema la rechaza y
  vuelve a pedir el dato.

---

## 9. Solución de problemas (Preguntas frecuentes)

**No aparece el menú / se ve "raro" la pantalla.**
El sistema limpia la consola automáticamente. Si se ve desordenado, presioná Enter o
volvé a ejecutar el programa.

**No puedo ingresar (dice "Usuario inexistente").**
Los archivos `usuarios.json`/`autos.json` pueden no existir (generálos con
`python informe.py`) o el DNI no está registrado. Podés usar el usuario de ejemplo:
DNI `10101010`, clave `1010`, o registrarte con la opción [2].

**El programa falla al abrir / no encuentra pandas.**
Falta instalar la dependencia: `pip install pandas`.

**Cargué autos con `crud.py` y desaparecieron.**
Ya no debería pasar: `menu.py` **no** regenera el catálogo. Verificá que estás usando
la misma carpeta (los archivos son relativos al directorio actual).

**Al elegir "Estadísticas del mes" no pasa nada de utilidad.**
Esa función todavía no está implementada (ver documentación técnica).

**Al elegir "Rentar" o "Devolver" volvía al mismo menú sin hacer nada.**
Era un `TypeError` por llamar a las funciones con un número equivocado de argumentos
(ya corregido). Si te pasa, actualizá `menu.py`.

**Un modelo de una categoría no aparece al alquilar.**
Puede estar ya alquilado (no se muestran los autos rentados) o no pertenecer a la
categoría elegida.

---

## 10. Glosario

| Término | Significado |
|---------|-------------|
| **CRUD** | Crear, Leer, Actualizar y Eliminar (Create, Read, Update, Delete). |
| **Patente** | Identificador único de cada auto. |
| **Catálogo** | Conjunto de todos los autos registrados. |
| **Persistencia** | Guardar los datos en un archivo para no perderlos al cerrar. |
| **JSON** | Formato de archivo de texto usado para guardar los datos. |
| **Reporte matricial** | Tabla (lista de listas / DataFrame) con información procesada. |
