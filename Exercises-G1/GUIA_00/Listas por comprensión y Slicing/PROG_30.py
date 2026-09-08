"""
PROG_30: La Agencia de Administración Gubernamental de Ingresos Públicos
(AGIP) nos solicita procesar parcelas representadas en una matriz de
5x5 píxeles. Cada celda de la imagen representa un tipo de terreno o
edificación:
- 'CH': Hogares con techo de chapa (ABL mensual: $2.000)
- 'TE': Hogares con techo de tejas (ABL mensual: $2.500)
* 'LO': Hogares con techo de losa/cemento (ABL mensual: $3.500)
* 'AV': Vía pública / Avenidas (No paga impuesto)

A partir del mapa satelital provisto:
1. Recorrer la imagen e ir contabilizando en un diccionario
conteo_hogares la cantidad de parcelas pertenecientes a cada categoría
de construcción.
2. Calcular el subtotal acumulado a cobrar en un diccionario
recaudacion_subtotal multiplicando el conteo por el impuesto
correspondiente.
3. Calcular e imprimir el Total General Recaudado por mes en dicha zona.

Tip: predefinir las tarifas en un diccionario base de consulta:
tarifas = {'CH': 2000, 'TE': 2500, 'LO': 3500}
"""

# Mapa satelital de 5x5 parcelas
mapa_satelital = [
['TE', 'TE', 'AV', 'LO', 'LO'],
['LO', 'TE', 'AV', 'TE', 'CH'],
['AV', 'AV', 'AV', 'AV', 'AV'],
['TE', 'LO', 'AV', 'LO', 'TE'],
['TE', 'LO', 'AV', 'TE', 'LO']
]
# Diccionario de tarifas ABL por tipo de edificación
tarifas_abl = {
'CH': 2000,
'TE': 2500,
'LO': 3500
}
# Diccionario para contar los tipos de parcelas
conteo_hogares = {
'CH': 0,
'TE': 0,
'LO': 0,
'AV': 0
}
# TODO 1: Recorrer la matriz mapa_satelital (bucle anidado para filas y celdas)
# e ir incrementando los contadores en conteo_hogares.
for i in mapa_satelital:
    for j in i:
        conteo_hogares[j] += 1
# TODO 2: Crear el diccionario recaudacion_subtotal calculando (conteo * tarifa)
# para las categorías imponibles ('CH', 'TE', 'LO').
recaudacion_subtotal = {}
for i in tarifas_abl:
    recaudacion_subtotal[i] = (conteo_hogares[i] * tarifas_abl[i])
# TODO 3: Mostrar el reporte final:
# - Cantidad de construcciones por tipo
# - Subtotal a cobrar por cada tipo
# - Suma total general recaudada por la zona

print(f"\nResultados: \n-- Techos de chapas: {conteo_hogares['CH']} | Subtotal: ${recaudacion_subtotal['CH']} \n-- Techos de tejas: {conteo_hogares['TE']} | Subtotal: ${recaudacion_subtotal['TE']}\
      \n-- Techos de losas/cemento: {conteo_hogares['LO']} | Subtotal: ${recaudacion_subtotal['LO']}\n-- Vías públicas / Avenidas: {conteo_hogares['AV']}")
print(f"\nTotal recaudado: ${sum(recaudacion_subtotal.values())}\n")