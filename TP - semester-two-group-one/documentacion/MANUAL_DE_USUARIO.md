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
- **Consultar informes** sobre las unidades (catálogo completo, disponibles y autos
  rentados).

Todos los datos quedan guardados en dos archivos:

- `autos.json` → el catálogo de autos.
- `usuarios.json` → los usuarios y los autos que tienen alquilados.

---

## 2. Antes de empezar (requisitos)

- Tener instalado **Python 3** (versión **3.12** o superior).
- Instalar las bibliotecas **pandas** y **matplotlib** (se usan para las tablas y los
  gráficos de los informes). En una terminal, una sola vez:

```bash
pip install pandas matplotlib
```

- Abrir una terminal (CMD, PowerShell o Terminal), ubicarse en la carpeta del
  proyecto y **generar los archivos de datos** (si no existen):

```bash
cd "TP - semester-two-group-one"
python informe.py
```

Al ejecutar `informe.py` se crean `autos.json` (con 25 autos) y `usuarios.json` (con
tres usuarios de ejemplo). Si los archivos ya existen, no se modifican.---

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

> **Importante:** al iniciarse, `menu.py` precarga `autos.json` y `usuarios.json` si
> no existen (o si están vacíos) y luego abre el menú principal. También podés
> generarlos a mano con `python informe.py` antes de usar `menu.py`.

> **Usuarios de ejemplo:** si generaste los datos con `informe.py`, podés ingresar con
> cualquiera de estos DNI, todos con la **contraseña `1234`**:
> `95823279`, `4817866` y `46280291`.

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

[1] Ver STOCK completo
[2] Autos Disponibles
[3] Autos rentados
[4] Estadísticas generales
-------------------------------
[0] Volver al menú principal
```

- **[1] Ver STOCK completo:** muestra todo el catálogo como tabla.
- **[2] Autos Disponibles:** tabla con **solo** los autos disponibles.
- **[3] Autos rentados:** tabla con **solo** los autos alquilados.
- **[4] Estadísticas generales:** gráficos del catálogo (barras de autos disponibles por
  marca y torta de disponibles vs. rentados).

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

### 6.3 Informes — submenú de empresa

- **[1] Ver STOCK completo:** tabla con **todos** los autos y su estado.
- **[2] Autos Disponibles:** tabla con **solo** los autos disponibles.
- **[3] Autos rentados:** tabla con **solo** los autos alquilados.
- **[4] Estadísticas generales:** abre una ventana con los gráficos del catálogo (una
  barra por marca con los autos disponibles y una torta de disponibles vs. rentados).

Las tablas se generan con pandas (reporte matricial) y los gráficos con matplotlib.

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

1. Ingresá el **año** (número entero entre 2000 y 2026).
2. Ingresá la **patente**. El formato depende del año:
   - año ≤ 2016 → 3 letras + 3 números (ej. `ABC123`);
   - año > 2016 → 2 letras + 3 números + 2 letras (ej. `AA123AA`).
   No puede repetirse (debe ser única).
3. Completá el resto de los campos; el sistema valida cada uno:

| Campo | Qué ingresar |
|-------|--------------|
| Marca | Una de: `toyota`, `renault`, `fiat`, `peugeot`, `chevrolet` |
| Modelo | Uno de los modelos de la marca elegida (ej. `etios`, `corolla`) |
| Calidad | Una de: `nuevo`, `cuidado`, `usado` |
| Precio | Número positivo (podés usar coma o punto) |
| Categoría | Una de: `sedan_hatchback`, `suv_crossover`, `pickup`, `monovolumen_mpv` |

Al terminar: *"Auto [PATENTE] agregado correctamente."*

> **Buen dato:** el auto se guarda con las 7 claves del esquema (incluido `estado`,
> que queda como disponible), así que se puede ver y alquilar de inmediato.

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

- **Patentes:** se convierten a mayúsculas y no pueden repetirse. El formato depende
  del año: `ABC123` (año ≤ 2016) o `AA123AA` (año > 2016).
- **Marca / Calidad / Categoría:** solo aceptan los valores predefinidos.
- **Modelo:** debe ser uno de los modelos de la marca elegida.
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
`python informe.py`) o el DNI no está registrado. Podés usar un usuario de ejemplo
(contraseña `1234`): DNI `95823279`, `4817866` o `46280291`; o registrarte con [2].

**El programa falla al abrir / no encuentra pandas o matplotlib.**
Faltan instalar las dependencias: `pip install pandas matplotlib`.

**Cargué autos con `crud.py` y desaparecieron.**
Verificá que estás usando la misma carpeta (los archivos son relativos al directorio
actual).

**Al elegir "Rentar" o "Devolver" vuelvo al mismo menú sin hacer nada.**
Asegurate de haber ingresado o registrado antes: para alquilar o devolver primero hay
que iniciar sesión.

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
