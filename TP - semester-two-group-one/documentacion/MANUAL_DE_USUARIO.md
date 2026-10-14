# Manual de Usuario — Sistema de Gestión de Concesionaria

**Proyecto:** TPO – SPRINT (Programación I)
**Tema:** Administración de una concesionaria (catálogo de autos + alquileres)
**Tipo de aplicación:** Programa de consola (línea de comandos)

Bienvenido al manual de usuario. Aquí se explica, paso a paso y sin tecnicismos,
cómo usar el sistema para administrar el catálogo de autos, alquilar vehículos y
consultar información.

---

## 1. ¿Qué hace este sistema?

El sistema permite:

- **Administrar el catálogo de autos**: ver, agregar, modificar y eliminar autos.
- **Alquilar autos** a clientes y registrar la operación.
- **Consultar informes** sobre las unidades disponibles (según se implementen).

Todos los datos quedan guardados en dos archivos:

- `autos.json` → el catálogo de autos.
- `rentados.json` → los autos que están alquilados.

---

## 2. Antes de empezar (requisitos)

- Tener instalado **Python 3** en la computadora.
- Abrir una terminal (CMD, PowerShell o Terminal) y ubicarse en la carpeta del
  proyecto:

```bash
cd "TP - semester-two-group-one"
```

---

## 3. Inicio rápido

El sistema tiene **dos programas** que se ejecutan por separado:

| Quiero... | Ejecutar |
|-----------|----------|
| Alquilar autos y ver informes | `python menu.py` |
| Administrar el catálogo (alta/baja/modificación) | `python crud.py` |

```bash
# Programa principal (usuario y empresa)
python menu.py

# Administrador del catálogo
python crud.py
```

> **Muy importante:** cada vez que se inicia `menu.py`, el sistema **regenera
> automáticamente** el archivo `autos.json` con 25 autos nuevos y aleatorios. Si
> cargaste tus propios autos con `crud.py`, ejecutá `crud.py` para administrarlos y
> evitá abrir `menu.py` si querés conservar ese catálogo.

---

## 4. Navegación: los menús

La aplicación funciona con **menús numerados**. Para elegir una opción, escribís el
número y presionás **Enter**.

### 4.1 Menú principal (`menu.py`)

```
--- MENÚ PRINCIPAL ---

[1] Menu de usuario.
[2] Menu de empresa.
-------------------------
[0] Salir.
```

- **[1] Menú de usuario:** alquilar y devolver autos.
- **[2] Menú de empresa:** ver informes.
- **[0] Salir:** cierra el programa.

### 4.2 Submenú de usuario

```
--- SUBMENÚ: MANEJO DE AUTOS ---

[1] Rentar auto.
[2] Devolver auto.
-------------------------
[0] Volver al menú principal
```

### 4.3 Submenú de empresa (informes)

```
--- SUBMENÚ: INFORMES ---

[1] Disponibilidad de unidades
[2] Estadisticas del mes
[3] Estado de autos rentados
[0] Volver al menú principal
```

> Las opciones **[1]** y **[2]** todavía están **en desarrollo**: al elegirlas el
> programa puede cerrarse con un error. La opción **[3]** también está incompleta.
> Revisá la sección 8 (Solución de problemas).

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

## 5. Guía de uso paso a paso (catálogo – `crud.py`)

### 5.1 Ver todo el catálogo — opción [1]

Muestra todos los autos guardados, con su ficha completa.

```
[SVU580]
	Marca: Fiat
	Modelo: Fastback
	Calidad: nuevo
	Año: 2007
	Precio: u$d 52.0
	Categoría: suv_crossover
```

Si no hay autos, el sistema avisa: *"No hay autos en el catálogo."*

### 5.2 Ver un auto — opción [2]

1. El sistema pide la **patente**.
2. Si existe, muestra su ficha. Si no, vuelve a pedirla hasta que ingreses una
   patente válida.

### 5.3 Agregar un auto — opción [3]

1. Ingresá la **patente**. No puede repetirse (debe ser única).
2. Completá los campos; el sistema valida cada uno:

| Campo | Qué ingresar |
|-------|--------------|
| Marca | Una de: `toyota`, `renault`, `fiat`, `peugeot`, `chevrloet` |
| Modelo | Texto libre (se guarda en minúsculas) |
| Calidad | Una de: `nuevo`, `como nuevo`, `usado` |
| Año | Número entero entre 2000 y 2026 |
| Precio | Número positivo (podés usar coma o punto) |
| Categoría | Una de: `sedan_hatchback`, `suv_crossover`, `pickup`, `monovolumen_mpv` |

Al terminar: *"Auto [PATENTE] agregado correctamente."*

### 5.4 Modificar un auto — opción [4]

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
[0] Terminar
```

3. Elegí el número del campo a cambiar e ingresá el nuevo valor.
4. Podés modificar varios campos seguidos; cuando termines, elegí **[0] Terminar**.

### 5.5 Eliminar un auto — opción [5]

1. Ingresá la patente del auto a eliminar.
2. El sistema lo borra y confirma: *"Auto [PATENTE] eliminado correctamente."*

> **Cuidado:** la eliminación no se puede deshacer.

---

## 6. Guía de uso paso a paso (alquileres – `menu.py`)

### 6.1 Rentar un auto — submenú de usuario → [1]

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

Al confirmar, el sistema muestra *"¡Auto con patente: [PATENTE] RENTADO!"* y lo
guarda en `rentados.json`.

> En cualquier paso podés escribir **[0]** para volver al menú anterior.

### 6.2 Devolver un auto — submenú de usuario → [2]

Esta función está **pendiente de implementación**. Por ahora solo muestra el
mensaje *"¿Que auto desea devolver?"* sin completar la operación.

### 6.3 Estado de autos rentados — submenú de empresa → [3]

Función **pendiente**: actualmente muestra el título *"ESTADO DE AUTOS RENTADOS"*
pero no lista los autos todavía.

### 6.4 Informes — submenú de empresa → [1] y [2]

Funciones **pendientes de implementación** (disponibilidad y estadísticas del mes).
Serán las que muestren los **reportes matriciales** (tablas de resumen).

---

## 7. Reglas de validación de datos

El sistema evita datos incorrectos:

- **Patentes:** se convierten a mayúsculas y no pueden repetirse.
- **Marca / Calidad / Categoría:** solo aceptan los valores predefinidos.
- **Año:** obligatorio entero entre 2000 y 2026.
- **Precio:** número positivo (se acepta `50,5` o `50.5`).
- **Opciones de menú:** si ingresás una opción inválida, el sistema la rechaza y
  vuelve a pedir el dato.

---

## 8. Solución de problemas (Preguntas frecuentes)

**No aparece el menú / se ve "raro" la pantalla.**
El sistema limpia la consola automáticamente. Si se ve desordenado, presioná Enter
o volvé a ejecutar el programa.

**Cargué autos con `crud.py` y desaparecieron.**
Probablemente abriste `menu.py`, que **regenera** `autos.json` con 25 autos
aleatorios. Administrá el catálogo siempre con `crud.py`.

**Al elegir "Disponibilidad de unidades" o "Estadísticas del mes" el programa falla.**
Esas funciones todavía no están implementadas (ver sección 9 del documento técnico).

**Quiero devolver un auto y no pasa nada.**
La devolución aún no está terminada; es una tarea pendiente del proyecto.

**Un modelo de una categoría no aparece al alquilar.**
Puede estar ya alquilado (no se muestran los autos rentados) o no pertenecer a la
categoría elegida.

---

## 9. Glosario

| Término | Significado |
|---------|-------------|
| **CRUD** | Crear, Leer, Actualizar y Eliminar (Create, Read, Update, Delete). |
| **Patente** | Identificador único de cada auto. |
| **Catálogo** | Conjunto de todos los autos registrados. |
| **Persistencia** | Guardar los datos en un archivo para no perderlos al cerrar. |
| **JSON** | Formato de archivo de texto usado para guardar los datos. |
| **Reporte matricial** | Tabla (lista de listas) con información procesada. |
