"""
Generador de contratos finales.

Lee las anotaciones manuales (días laborales marcados con punto de inicio/fin)
y el detalle de visitas por día, para producir un CSV con las fechas, timestamps
de inicio y fin de jornada, y la duración del recorrido.

Entrada:
    - backend/data/annotations/annotations.jsonl  (anotaciones por día)
    - backend/data/visitas_business_days_by_day.json (detalle de visitas)
Salida:
    - backend/data/final_contract.csv
"""

import json
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Rutas base
# ---------------------------------------------------------------------------
_THIS_DIR = Path(__file__).resolve().parent
_DATA_DIR = _THIS_DIR / ".." / "backend" / "data"

# ---------------------------------------------------------------------------
# 2. Cargar y consolidar anotaciones
#    Cada lote es un archivo JSONL con una anotación por línea.
#    Se concatenan todos los lotes y se eliminan duplicados por fecha,
#    conservando la anotación más reciente.
# ---------------------------------------------------------------------------
df_annotated_til_20240531 = pd.read_json(
    _DATA_DIR / "annotations" / "annotations.jsonl",
    lines=True,
)

batches_list = [df_annotated_til_20240531]
df_full_annotations = pd.concat(batches_list, ignore_index=True)
df_full_annotations.drop_duplicates(subset=["date"], inplace=True, keep="last")

# ---------------------------------------------------------------------------
# 3. Cargar el diccionario de visitas por día
#    Estructura: { "YYYY-MM-DD": { "data": [ { "timestamp": ... }, ... ] } }
# ---------------------------------------------------------------------------
with open(_DATA_DIR / "visitas_business_days_by_day.json", "r") as f:
    dict_visits_by_day = json.load(f)

# ---------------------------------------------------------------------------
# 4. Filtrar solo los días marcados como laborales
# ---------------------------------------------------------------------------
df_final_contract = df_full_annotations[df_full_annotations["working"]].copy()
df_final_contract.reset_index(drop=True, inplace=True)

# ---------------------------------------------------------------------------
# 5. Resolver timestamps de inicio y fin de jornada
#    Cada anotación tiene start_point / end_point que son índices dentro
#    del arreglo de visitas de ese día.
# ---------------------------------------------------------------------------
for idx, day in df_final_contract.iterrows():
    date_str = day["date"].strftime("%Y-%m-%d")
    visits = dict_visits_by_day[date_str]["data"]
    df_final_contract.loc[idx, "inicio"] = visits[int(day["start_point"])]["timestamp"]
    df_final_contract.loc[idx, "fin"] = visits[int(day["end_point"])]["timestamp"]

# ---------------------------------------------------------------------------
# 6. Limpiar columnas auxiliares y calcular duración del recorrido
# ---------------------------------------------------------------------------
df_final_contract.drop(
    columns=["working", "start_point", "end_point", "total_points"], inplace=True
)

df_final_contract["inicio"] = pd.to_datetime(df_final_contract["inicio"])
df_final_contract["fin"] = pd.to_datetime(df_final_contract["fin"])
df_final_contract["recorrido"] = df_final_contract["fin"] - df_final_contract["inicio"]

df_final_contract.rename(columns={"date": "fecha"}, inplace=True)

# ---------------------------------------------------------------------------
# 7. Exportar resultado
# ---------------------------------------------------------------------------
df_final_contract.to_csv(
    _DATA_DIR / "resultados_uriel_mazabuel_etiquetados.csv", index=False
)
