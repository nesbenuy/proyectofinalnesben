from flask import Flask, render_template, request, make_response, send_file, Response
from datetime import date, datetime
import io, hashlib, json

from criteria import (
    TIPOS_AMBIENTE, USOS_SUELO, COBERTURA_RELIEVE,
    INTERVENCION_HUMANA, CONECTIVIDAD_TERRITORIAL,
    VALOR_ECOCULTURAL
)
from storage import read_all, save_row, delete_row_by_key
from analysis import chart_counts_by_ambiente
from geoval import parse_lat, parse_lon

app = Flask(__name__)

def _row_key(row: dict) -> str:
    canonical = {k: row.get(k, "") for k in [
        "fecha","lugar","lat","lon","tipo_ambiente","usos_suelo",
        "cobertura_relieve","intervencion_humana","conectividad",
        "valor_ecocultural","descripcion"
    ]}
    data = json.dumps(canonical, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()

@app.route("/")
def index():
    rows = read_all()
    for r in rows:
        r["_key"] = _row_key(r)
    return render_template(
        "index.html",
        hoy=date.today(),
        rows=rows,
        TIPOS_AMBIENTE=TIPOS_AMBIENTE,
        USOS_SUELO=USOS_SUELO,
        COBERTURA_RELIEVE=COBERTURA_RELIEVE,
        INTERVENCION_HUMANA=INTERVENCION_HUMANA,
        CONECTIVIDAD_TERRITORIAL=CONECTIVIDAD_TERRITORIAL,
        VALOR_ECOCULTURAL=VALOR_ECOCULTURAL,
    )

@app.route("/obs", methods=["POST"])
def crear_obs():
    data = {k: request.form.get(k, "").strip() for k in request.form}

    # Validación de coordenadas
    lat = parse_lat(data.get("lat"))
    lon = parse_lon(data.get("lon"))
    if lat is None or lon is None:
        html = render_template("_row_error.html", msg="Coordenadas inválidas (lat/lon)")
        return make_response(html, 200)
    data["lat"], data["lon"] = lat, lon

    # Catálogos cerrados
    checks = [
        (data.get("tipo_ambiente") in TIPOS_AMBIENTE, "Tipo de ambiente inválido"),
        (data.get("usos_suelo") in USOS_SUELO, "Uso del suelo inválido"),
        (data.get("cobertura_relieve") in COBERTURA_RELIEVE, "Cobertura/relieve inválido"),
        (data.get("intervencion_humana") in INTERVENCION_HUMANA, "Intervención humana inválida"),
        (data.get("conectividad") in CONECTIVIDAD_TERRITORIAL, "Conectividad territorial inválida"),
        (data.get("valor_ecocultural") in VALOR_ECOCULTURAL, "Valor eco-cultural inválido"),
    ]
    for ok, msg in checks:
        if not ok:
            html = render_template("_row_error.html", msg=msg)
            return make_response(html, 200)

    save_row(data)
    data["_key"] = _row_key(data)
    html = render_template("_row.html", r=data, row_index=1)
    resp = make_response(html, 200)
    # Refrescar la gráfica tras guardar
    resp.headers["HX-Trigger"] = json.dumps({"refreshChart": True})
    return resp

@app.route("/obs/<key>", methods=["DELETE"])
def borrar_obs(key):
    deleted = delete_row_by_key(key)
    if deleted:
        # 200 con cuerpo vacío -> HTMX elimina la fila 
        resp = make_response("", 200)
        # Refresco del gráfico
        resp.headers["HX-Trigger"] = json.dumps({"refreshChart": True})
        return resp
    return Response(status=404)

@app.route("/chart.png")
def chart_png():
    rows = read_all()
    png = chart_counts_by_ambiente(rows)
    resp = send_file(io.BytesIO(png), mimetype="image/png")
    # Evitar caché
    resp.headers["Cache-Control"] = "no-store"
    return resp

@app.route("/chart")
def chart_html():
    # HTML que referencia la imagen del gráfico
    return render_template("chart_img.html", ts=datetime.now().timestamp())

if __name__ == "__main__":
    app.run(debug=False)