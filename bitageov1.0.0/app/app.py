from flask import Flask, render_template, request, redirect, url_for, Response
from datetime import date
from .criteria import (TIPOS_AMBIENTE, USOS_SUELO, COBERTURA_RELIEVE, 
                       INTERVENCION_HUMANA, CONECTIVIDAD_TERRITORIAL, VALOR_ECOCULTURAL, escoger)
from .storage import save_row, read_all, ensure_csv
from .analysis import chart_counts_by_ambiente

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    ensure_csv()
    rows = read_all()
    return render_template("index.html",
                           rows=rows,
                           hoy=str(date.today()),
                           TIPOS_AMBIENTE=TIPOS_AMBIENTE,
                           USOS_SUELO=USOS_SUELO,
                           COBERTURA_RELIEVE=COBERTURA_RELIEVE,
                           INTERVENCION_HUMANA=INTERVENCION_HUMANA,
                           CONECTIVIDAD_TERRITORIAL=CONECTIVIDAD_TERRITORIAL,
                           VALOR_ECOCULTURAL=VALOR_ECOCULTURAL)

@app.route("/obs", methods=["POST"])
def crear_obs():
    # Entrada con criterios
    data = {
        "fecha": request.form.get("fecha","").strip() or str(date.today()),
        "lugar": request.form.get("lugar","").strip(),
        "lat": request.form.get("lat","0").strip(),
        "lon": request.form.get("lon","0").strip(),
        "tipo_ambiente": escoger(TIPOS_AMBIENTE, request.form.get("tipo_ambiente","urbano"), "urbano"),
        "usos_suelo": escoger(USOS_SUELO, request.form.get("usos_suelo","mixto"), "mixto"),
        "cobertura_relieve": escoger(COBERTURA_RELIEVE, request.form.get("cobertura_relieve","mosaico_mixto"), "mosaico_mixto"),
        "intervencion_humana": escoger(INTERVENCION_HUMANA, request.form.get("intervencion_humana","media"), "media"),
        "conectividad": escoger(CONECTIVIDAD_TERRITORIAL, request.form.get("conectividad","media"), "media"),
        "valor_ecocultural": escoger(VALOR_ECOCULTURAL, request.form.get("valor_ecocultural","ninguno"), "ninguno"),
        "descripcion": request.form.get("descripcion","").strip(),
    }
    # Guardar
    save_row(data)
    # Respuesta HTMX: devolver la fila renderizada
    return render_template("_row.html", r=data, i=0)

@app.route("/chart.png", methods=["GET"])
def chart_png():
    rows = read_all()
    png = chart_counts_by_ambiente(rows)
    return Response(png, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
