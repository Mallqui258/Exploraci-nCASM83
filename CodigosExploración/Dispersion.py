# dispersion_por_escalas.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations

# ==========================
# 1. Cargar dataset
# ==========================
ARCHIVO = "CASM83.xlsx"
df = pd.read_excel(ARCHIVO)

# ==========================
# 2. Definir ítems por escala
# ==========================
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

# ==========================
# 3. Calcular puntajes promedio por escala
# ==========================
scale_scores = {}
for escala, items in scale_items.items():
    cols = [col_from_num(i) for i in items]
    cols = [c for c in cols if c is not None]
    if not cols:
        print(f"[AVISO] Escala {escala} sin columnas válidas.")
        continue
    scale_scores[escala] = df[cols].mean(axis=1)

scores_df = pd.DataFrame(scale_scores)

# añadir Género para colorear (si existe)
hue_col = None
if "Genero" in df.columns:
    gen = df["Genero"]
    if set(gen.dropna().unique()) <= {0, 1}:
        gen = gen.map({0: "Femenino", 1: "Masculino"})
    scores_df["Genero"] = gen.astype(str)
    hue_col = "Genero"

# ==========================
# 4. Crear carpeta de salida
# ==========================
output_dir = "dispersion_escalas"
os.makedirs(output_dir, exist_ok=True)

# ==========================
# 5. Generar SOLO diagramas de dispersión
# ==========================
sns.set(style="whitegrid")

escalas = list(scale_scores.keys())  # todas las escalas calculadas
pares = list(combinations(escalas, 2))  # todas las combinaciones de 2 en 2

for x_var, y_var in pares:
    plt.figure(figsize=(5, 4))

    if hue_col:
        sns.scatterplot(
            data=scores_df,
            x=x_var,
            y=y_var,
            hue=hue_col,
            alpha=0.8
        )
    else:
        sns.scatterplot(
            data=scores_df,
            x=x_var,
            y=y_var,
            alpha=0.8
        )

    plt.title(f"Dispersión {y_var} vs {x_var}")
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    plt.tight_layout()

    filename = os.path.join(output_dir, f"scatter_{y_var}_vs_{x_var}.png")
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Gráfico guardado: {filename}")

print("✅ Diagramas de dispersión generados en la carpeta 'dispersion_escalas'.")
