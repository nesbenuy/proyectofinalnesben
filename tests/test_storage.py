from storage import save_row, read_all, delete_row_by_key, _row_key_for_storage

def test_guardado_y_borrado_roundtrip():
    row = {
        "fecha": "2025-10-31",
        "lugar": "Lugar de prueba",
        "lat": "-34.500000",
        "lon": "-56.166667",
        "tipo_ambiente": "urbano",
        "usos_suelo": "residencial",
        "cobertura_relieve": "llanura",
        "intervencion_humana": "alta",
        "conectividad": "local",
        "valor_ecocultural": "medio",
        "descripcion": "fila de prueba"
    }
    save_row(row)
    data = read_all()
    assert any(r.get("lugar") == "Lugar de prueba" for r in data)
    key = _row_key_for_storage(row)
    assert delete_row_by_key(key) is True
