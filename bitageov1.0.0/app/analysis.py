from collections import Counter
from io import BytesIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def chart_counts_by_ambiente(rows):
    c = Counter([ (r.get("tipo_ambiente","") or "").strip().lower() for r in rows ])
    if "" in c: del c[""]
    labels = list(c.keys())
    values = list(c.values())
    fig = plt.figure()
    plt.bar(labels, values)
    plt.title("Observaciones por tipo de ambiente")
    plt.xlabel("Tipo de ambiente")
    plt.ylabel("Cantidad")
    bio = BytesIO()
    plt.tight_layout()
    fig.savefig(bio, format="png", bbox_inches="tight")
    plt.close(fig)
    bio.seek(0)
    return bio.read()
