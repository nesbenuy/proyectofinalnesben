from app.storage import save_row, read_all
from pathlib import Path

def test_save_and_read(tmp_path, monkeypatch):
    from app import storage
    fake = tmp_path / "obs.csv"
    monkeypatch.setattr(storage, "CSV_EXT", fake)
    data = {"fecha":"2025-10-21","lugar":"Patio","lat":"-34.3","lon":"-56.7",
            "tipo_ambiente":"urbano","usos_suelo":"mixto","cobertura_relieve":"pradera/llanura",
            "intervencion_humana":"media","conectividad":"media","valor_ecocultural":"ninguno",
            "descripcion":"prueba"}
    save_row(data)
    rows = read_all()
    assert len(rows)==1
    assert rows[0]["lugar"]=="Patio"
