from collections import Counter
from io import BytesIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def chart_counts_by_ambiente(rows):
    ambientes = [(r.get("tipo_ambiente","") or "").strip() for r in rows]
    ambientes = [a for a in ambientes if a]
    if not ambientes:
        fig = plt.figure(figsize=(6, 3.6))
        plt.text(0.5, 0.5, "Sin datos aún", ha="center", va="center", fontsize=12, color="#555")
        plt.axis("off")
    else:
        c = Counter(ambientes)
        tipos = list(c.keys())
        valores = [max(0, c[t]) for t in tipos]
        fig = plt.figure(figsize=(7.2, 4.2))
        plt.bar(tipos, valores, color="#74c69d", edgecolor="#1b4332", linewidth=1.0)
        plt.xlabel("Tipo de ambiente", fontsize=11, color="#1b4332")
        plt.ylabel("Cantidad de registros", fontsize=11, color="#1b4332")
        plt.title("Distribución de observaciones por tipo de ambiente", fontsize=13, color="#081c15", pad=8)
        plt.xticks(rotation=20, ha="right", fontsize=9); plt.yticks(fontsize=9)
        plt.grid(axis="y", linestyle="--", alpha=0.25)
        plt.tight_layout()
    bio = BytesIO(); fig.savefig(bio, format="png", bbox_inches="tight"); plt.close(fig); bio.seek(0)
    return bio.read()