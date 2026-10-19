"""
Modulo: pruebas.py - Pruebas del Trabajo Practico (TPO - SPRINT).

Estado: VACIO. Todavia no hay pruebas automaticas ni manuales registradas.

RECOMENDACION (Req 1 / Req 8 del SPRINT): usar este archivo para dejar registradas
y poder reejecutar las pruebas del sistema, por ejemplo:

  - CRUD (Req 7): alta con y sin "estado", ver_stock en modo (1,0) y (0,1),
    modificar y eliminar una patente inexistente.
  - Alquiler (Req 2): rentar y devolver el mismo auto; verificar que el campo
    "estado" cambia a False y luego a True, y que la patente entra y sale de
    "autos_rentados" del usuario.
  - Excepciones (Req 1): patente "0", DNI no numerico, autos.json o
    usuarios.json ausentes o corruptos (json.JSONDecodeError).
  - Informes (Req 8): verificar que el reporte matricial se imprime completo y
    que no rompe con autos sin la clave "estado".

TODO(TP): completar este archivo con las pruebas del sprint.
"""
