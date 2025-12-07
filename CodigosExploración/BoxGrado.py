"""
# boxplot_grado.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel("CASM83.xlsx")

# Columnas de preguntas
question_cols = [c for c in df.columns if str(c).startswith("Pregunta_")]
if not question_cols:
    raise ValueError("No se encontraron columnas 'Pregunta_'.")

df["promedio_respuestas"] = df[question_cols].mean(axis=1)

# Verificar columna de grado
grado_col = None
for c in df.columns:
    if "grado" in c.lower() or "grade" in c.lower():
        grado_col = c
        break

if grado_col is None:
    raise ValueError("No se encontró columna de Grado (busqué 'grado' o 'grade').")

df["Grado_label"] = df[grado_col].astype(str)

sns.set(style="whitegrid")
plt.figure(figsize=(6, 5))
sns.boxplot(data=df, x="Grado_label", y="promedio_respuestas")
plt.title("Distribución del promedio de respuestas por Grado")
plt.xlabel("Grado")
plt.ylabel("Promedio de respuesta (0–3)")
plt.tight_layout()
plt.show()
"""

# boxplot_grado.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel("CASM83.xlsx")

question_cols = [c for c in df.columns if str(c).startswith("Pregunta_")]
if not question_cols:
    raise ValueError("No se encontraron columnas 'Pregunta_'.")

df["promedio_respuestas"] = df[question_cols].mean(axis=1)

grado_col = None
for c in df.columns:
    if "grado" in c.lower() or "grade" in c.lower():
        grado_col = c
        break

if grado_col is None:
    raise ValueError("No se encontró columna de Grado (busqué 'grado' o 'grade').")

# 🔴 Filtrar filas con grado 0 o NaN
df = df[df[grado_col].notna()]
df = df[df[grado_col] != 0]

df["Grado_label"] = df[grado_col].astype(str)

sns.set(style="whitegrid")
plt.figure(figsize=(6, 5))
sns.boxplot(data=df, x="Grado_label", y="promedio_respuestas")
plt.title("Distribución del promedio de respuestas por Grado")
plt.xlabel("Grado")
plt.ylabel("Promedio de respuesta (0–3)")
plt.tight_layout()
plt.show()
