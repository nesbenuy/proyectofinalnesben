import csv, os, json, hashlib

CSV_FIELDS = ["fecha","lugar","lat","lon","tipo_ambiente","usos_suelo",
              "cobertura_relieve","intervencion_humana","conectividad",
              "valor_ecocultural","descripcion"]

def _csv_path():
    return os.path.join(os.path.dirname(__file__), "data", "observaciones_ext.csv")

def read_all():
    path = _csv_path()
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=CSV_FIELDS).writeheader()
        return []
    rows = []
    with open(path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            rows.append({k: r.get(k, "") for k in CSV_FIELDS})
    return rows

def save_row(row: dict):
    path = _csv_path()
    exists = os.path.exists(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not exists:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in CSV_FIELDS})

def _row_key_for_storage(row: dict) -> str:
    canonical = {k: row.get(k, "") for k in CSV_FIELDS}
    data = json.dumps(canonical, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def delete_row_by_key(key: str) -> bool:
    rows = read_all()
    kept, removed = [], False
    # calcular hash de cada fila como en app._row_key
    for r in rows:
        data = json.dumps({k: r.get(k, "") for k in CSV_FIELDS}, sort_keys=True, ensure_ascii=False).encode("utf-8")
        h = hashlib.sha256(data).hexdigest()
        if not removed and h == key:
            removed = True
            continue
        kept.append(r)
    # reescribir CSV
    path = _csv_path()
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in kept:
            w.writerow(r)
    return removed