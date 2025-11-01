import criteria

def test_catalogos_basicos():
    assert "urbano" in criteria.TIPOS_AMBIENTE
    assert "residencial" in criteria.USOS_SUELO
    assert isinstance(criteria.COBERTURA_RELIEVE, list)
