from geoval import parse_lat, parse_lon

def test_parse_lat_lon_decimal():
    assert parse_lat("34.5") == 34.5
    assert parse_lon("-56.2") == -56.2

def test_parse_lat_lon_dms():
    assert parse_lat("34°30'S") == -34.5
    assert parse_lon("56°10'W") == -56.166667
