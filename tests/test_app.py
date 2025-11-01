from app import app

def test_chart_png_endpoint():
    client = app.test_client()
    r = client.get("/chart.png")
    assert r.status_code == 200
    assert r.headers.get("Content-Type","").startswith("image/png")
