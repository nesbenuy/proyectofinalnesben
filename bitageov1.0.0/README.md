# Bitácora Geográfica v1.0.0 – Web (Flask + Jinja2 + HTMX)

Interfaz **web** para registrar observaciones geográficas con **criterios**.

## Requisitos
python -m venv .venv
# Win: .venv\Scripts\Activate.ps1
```

## Cómo correr
# desde la carpeta del proyecto
python -m app.app
```

## ¿Qué incluye?
- **Un solo formulario** con criterios: tipo de ambiente, uso del suelo, cobertura/relieve, intervención, conectividad, valor eco-cultural.
- **Listado en tabla** (HTMX agrega la fila sin recargar).
- **Gráfico PNG** por tipo de ambiente (endpoint `/chart.png`).

## Archivos
- `app/app.py` → rutas Flask.
- `app/templates/` → Jinja2 (`index.html`, `_row.html`, `base.html`).
- `app/static/css/pastel.css` → estilos colores pasteles.
- `app/criteria.py` → catálogos de criterios.
- `app/storage.py` → CSV extendido `data/observaciones_ext.csv`.
- `app/analysis.py` → gráfico con matplotlib.
- `data/observaciones_ext.csv` → se crea solo al usar la app.

## Notas
- No usa BD: **CSV** simple y transparente.
- HTMX se carga por CDN (se necesita internet para el script).

