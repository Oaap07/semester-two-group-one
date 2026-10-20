# Documentación del Proyecto — TPO SPRINT

Índice de la documentación del sistema de gestión de concesionaria (Programación I).

| Documento | Contenido | Audiencia |
|-----------|-----------|-----------|
| [DOCUMENTACION_TECNICA.md](./DOCUMENTACION_TECNICA.md) | Descripción del sistema, estructura de módulos, modelo de datos, persistencia, requisitos técnicos, instalación/ejecución, manejo de errores y problemas conocidos. | Desarrolladores / docentes |
| [MANUAL_DE_USUARIO.md](./MANUAL_DE_USUARIO.md) | Guía de uso paso a paso: inicio rápido, navegación de menús, registro e ingreso, gestión del catálogo, alquileres, validaciones y solución de problemas. | Usuarios finales |
| [presentacion_rentar.html](./presentacion_rentar.html) | Presentación HTML del flujo de alquiler. | Usuarios / docentes |

## Resumen rápido

- **Punto de entrada principal:** `python menu.py`
- **Administración del catálogo (CRUD):** `python crud.py`
- **Generar los datos (si no existen):** `python informe.py`
- **Pruebas automáticas (pytest):** `python pruebas.py`
- **Persistencia:** `autos.json` (catálogo) y `usuarios.json` (usuarios y sus alquileres)
- **Lenguaje:** Python 3.12+ (requiere `pandas` para las tablas de los informes)

> La documentación técnica incluye una sección de **pruebas automáticas** (§11) con el
> detalle de la suite `pruebas.py` (94 pruebas).
