import csv
from pathlib import Path
from typing import Dict, List

CSV_EXT = Path(__file__).resolve().parent.parent / "data" / "observaciones_ext.csv"
FIELDS = [
    "fecha","lugar","lat","lon","tipo_ambiente",
    "usos_suelo","cobertura_relieve","intervencion_humana",
    "conectividad","valor_ecocultural","descripcion"
]

def ensure_csv():
    CSV_EXT.parent.mkdir(parents=True, exist_ok=True)
    if not CSV_EXT.exists():
        with open(CSV_EXT, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)

def save_row(row: Dict[str,str]):
    ensure_csv()
    with open(CSV_EXT, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([row.get(k, "") for k in FIELDS])

def read_all() -> List[Dict[str,str]]:
    ensure_csv()
    with open(CSV_EXT, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
