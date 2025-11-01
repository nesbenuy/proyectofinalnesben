from analysis import chart_counts_by_ambiente

def test_chart_bytes_vacio():
    png = chart_counts_by_ambiente([])
    assert isinstance(png, (bytes, bytearray))
    assert len(png) > 100

def test_chart_bytes_con_datos():
    rows = [
        {"tipo_ambiente": "urbano"},
        {"tipo_ambiente": "urbano"},
        {"tipo_ambiente": "rural"},
    ]
    png = chart_counts_by_ambiente(rows)
    assert isinstance(png, (bytes, bytearray))
    assert len(png) > 100
