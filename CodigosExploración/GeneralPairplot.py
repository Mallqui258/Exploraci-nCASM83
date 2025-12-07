# pairplot_general.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1) Cargar dataset
df = pd.read_excel("CASM83.xlsx")

# 2) Seleccionar solo columnas numéricas
num_df = df.select_dtypes(include="number").copy()

# 3) (Opcional) eliminar columnas tipo ID que no aportan al análisis
cols_to_drop = []
for c in num_df.columns:
    name = str(c).lower()
    if "id" in name or "codigo" in name:
        cols_to_drop.append(c)

num_df = num_df.drop(columns=cols_to_drop, errors="ignore")

print("Columnas numéricas detectadas (sin IDs):")
print(list(num_df.columns))

# 4) Limitar la cantidad de variables para que el gráfico sea legible
MAX_VARS = 8  # cambia esto si quieres más/menos
if num_df.shape[1] > MAX_VARS:
    # Tomamos las primeras N columnas (puedes usar sample si quieres aleatorio)
    used_cols = num_df.columns[:MAX_VARS]
    print(f"\nSe usarán solo {MAX_VARS} variables para el pairplot:")
    print(list(used_cols))
    num_df = num_df[used_cols]
else:
    used_cols = num_df.columns

# 5) Elegir columna para colorear (hue) si existe
hue_col = None
if "Genero" in df.columns:
    hue_series = df["Genero"]
    # Mapear 0/1 a texto si está codificado
    if set(hue_series.dropna().unique()) <= {0, 1}:
        hue_series = hue_series.map({0: "Femenino", 1: "Masculino"})
    num_df["Genero"] = hue_series.astype(str)
    hue_col = "Genero"
else:
    # otros posibles nombres de target/perfil
    for cand in ["perfil", "Perfil", "perfil_profesional", "target", "clase"]:
        if cand in df.columns:
            num_df[cand] = df[cand].astype(str)
            hue_col = cand
            break

# 6) Generar pairplot general
sns.set(style="whitegrid")

if hue_col:
    g = sns.pairplot(
        num_df,
        hue=hue_col,
        diag_kind="kde",
        corner=True
    )
else:
    g = sns.pairplot(
        num_df,
        diag_kind="kde",
        corner=True
    )

g.fig.suptitle("Matriz de dispersión general de variables numéricas", y=1.02)
plt.tight_layout()
plt.show()
