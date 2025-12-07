import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

# ================================
# 1. CARGA DE DATOS
# ================================
df = pd.read_excel("CASM83.xlsx")

# ================================
# 2. ESCALAS E ÍTEMS
# ================================
scale_items = {
    "CCFM": [1, 14, 27, 40, 53, 66, 79, 92, 105, 118, 131],
    "CCSS": [2, 15, 28, 41, 54, 67, 80, 93, 106, 119, 132],
    "CCNA": [3, 16, 29, 42, 55, 68, 81, 94, 107, 120, 133],
    "CCCO": [4, 17, 30, 43, 56, 69, 82, 95, 108, 121, 134],
    "ARTE": [5, 18, 31, 44, 57, 70, 83, 96, 109, 122, 135],
    "BURO": [6, 19, 32, 45, 58, 71, 84, 97, 110, 123, 136],
    "CCEP": [7, 20, 33, 46, 59, 72, 85, 98, 111, 124, 137],
    "HAA":  [8, 21, 34, 47, 60, 73, 86, 99, 112, 125, 138],
    "FINA": [9, 22, 35, 48, 61, 74, 87, 100, 113, 126, 139],
    "LING": [10, 23, 36, 49, 62, 75, 88, 101, 114, 127, 140],
    "JURI": [11, 24, 37, 50, 63, 76, 89, 102, 115, 128, 141],
    "VERA": [12, 25, 38, 51, 64, 77, 90, 103, 116, 129, 142],
    "CONS": [13, 26, 39, 52, 65, 78, 91, 104, 117, 130, 143],
}

def col_from_num(n: int):
    col = f"Pregunta_{n}"
    return col if col in df.columns else None

# ================================
# 3. CÁLCULO DE PUNTAJES POR ESCALA
# ================================
scale_scores = {}
for escala, items in scale_items.items():
    cols = [col_from_num(i) for i in items]
    cols = [c for c in cols if c is not None]
    if cols:
        scale_scores[escala] = df[cols].mean(axis=1)

scores_df = pd.DataFrame(scale_scores)

# Añadir género si existe (para densidades separadas)
if "Genero" in df.columns:
    gen = df["Genero"]
    if set(gen.dropna().unique()) <= {0, 1}:
        gen = gen.map({0: "Femenino", 1: "Masculino"})
    scores_df["Genero"] = gen.astype(str)
    hue_col = "Genero"
else:
    hue_col = None

# ================================
# 4. DIAGRAMAS DE DENSIDAD POR ESCALA
# ================================
sns.set(style="whitegrid")

escalas = list(scale_items.keys())
n_escalas = len(escalas)

# Definimos una rejilla 4x4 (16 > 13 escalas) para que haya espacio
n_rows, n_cols = 4, 4
fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 12), sharex=True, sharey=True)
axes = axes.flatten()

for i, escala in enumerate(escalas):
    ax = axes[i]
    if hue_col:
        sns.kdeplot(
            data=scores_df,
            x=escala,
            hue=hue_col,
            common_norm=False,
            ax=ax,
            fill=True,
            alpha=0.4
        )
    else:
        sns.kdeplot(
            data=scores_df,
            x=escala,
            ax=ax,
            fill=True,
            alpha=0.5
        )

    ax.set_title(escala)
    ax.set_xlabel("")
    ax.set_ylabel("Densidad")

# Quitar subplots vacíos si sobran
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

fig.suptitle("Distribución de puntajes promedio por escala CASM-83", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.savefig("densidad_escalas_casm83.png", dpi=300, bbox_inches="tight")
plt.show()
