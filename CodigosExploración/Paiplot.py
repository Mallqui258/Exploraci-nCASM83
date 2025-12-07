# Paiplot.py  (o como lo hayas llamado)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1) Cargar dataset
df = pd.read_excel("CASM83.xlsx")

# 2) Detectar columnas de preguntas (todas las que empiezan con 'Pregunta_')
question_cols = [c for c in df.columns if str(c).startswith("Pregunta_")]

print(f"Total de preguntas detectadas: {len(question_cols)}")
# Debería ser 143

# 3) DEFINIR ESCALAS Y SUS ÍTEMS
scale_items = {
    "CCFM":  [1, 14, 27, 40, 53, 66, 79, 92, 105, 118, 131],
    "CCSS":  [2, 15, 28, 41, 54, 67, 80, 93, 106, 119, 132],
    "CCNA":  [3, 16, 29, 42, 55, 68, 81, 94, 107, 120, 133],
    #"CCCO":  [4, 17, 30, 43, 56, 69, 82, 95, 108, 121, 134],
    #"ARTE":  [5, 18, 31, 44, 57, 70, 83, 96, 109, 122, 135],
    #"BURO":  [6, 19, 32, 45, 58, 71, 84, 97, 110, 123, 136],
    #"CCEP":  [7, 20, 33, 46, 59, 72, 85, 98, 111, 124, 137],
    #"HAA":  [8, 21, 34, 47, 60, 73, 86, 99, 112, 125, 138],
    #"FINA":  [9, 22, 35, 48, 61, 74, 87, 100, 113, 126, 139],
    #"LING":  [10, 23, 36, 49, 62, 75, 88, 101, 114, 127, 140],
    #"JURI":  [11, 24, 37, 50, 63, 76, 89, 102, 115, 128, 141],
    #"VERA":  [12, 25, 38, 51, 64, 77, 90, 103, 116, 129, 142],
    #"CONS":  [13, 26, 39, 52, 65, 78, 91, 104, 117, 130, 143]
}

def col_from_num(n: int):
    """
    Devuelve 'Pregunta_n' si existe en el DataFrame.
    """
    col = f"Pregunta_{n}"
    if col not in df.columns:
        print(f"[WARN] {col} no existe en el DataFrame.")
        return None
    return col


# 4) Calcular puntajes promedio por escala para cada estudiante
scale_scores = {}
for escala, items in scale_items.items():
    cols = [col_from_num(i) for i in items]
    cols = [c for c in cols if c is not None]  # quitar Nones si hay errores

    if not cols:
        print(f"[AVISO] La escala '{escala}' no tiene columnas válidas, revisa scale_items.")
        continue

    # promedio de las preguntas de esa escala por estudiante
    scale_scores[escala] = df[cols].mean(axis=1)

scores_df = pd.DataFrame(scale_scores)

if scores_df.empty:
    raise ValueError("No se calculó ninguna escala. Revisa el diccionario scale_items.")

print("Escalas calculadas:", list(scores_df.columns))


# 5) Elegir variable para colorear (hue): usaremos 'Genero'
if "Genero" in df.columns:
    hue_series = df["Genero"]
    # mapear 0/1 a etiquetas legibles si corresponde
    if set(hue_series.dropna().unique()) <= {0, 1}:
        hue_series = hue_series.map({0: "Femenino", 1: "Masculino"})
    scores_df["Genero"] = hue_series.astype(str)
    hue_col = "Genero"
else:
    hue_col = None


# 6) Generar pairplot
sns.set(style="whitegrid")

if hue_col:
    g = sns.pairplot(
        scores_df,
        hue=hue_col,
        diag_kind="kde",
        corner=True
    )
else:
    g = sns.pairplot(
        scores_df,
        diag_kind="kde",
        corner=True
    )

g.fig.suptitle("Matriz de dispersión entre puntajes por escala CASM-83", y=1.02)
plt.tight_layout()
plt.show()
