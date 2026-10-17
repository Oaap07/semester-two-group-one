import pandas as pd
import informe as inf
import json
try:
    with open(inf.RUTA_AUTOS_JSON, 'r', encoding="utf-8") as archivo:
        lista = json.load(archivo)
except OSError as e:
    print(f"/// Ocurrió un error de sistema: {e} ///")
    try: input("[Enter] ")
    except: pass
data = lista 

df = pd.DataFrame(data)
print(df.T)


