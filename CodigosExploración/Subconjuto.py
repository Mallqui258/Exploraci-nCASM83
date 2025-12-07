# ============================================================
# 3a) Histogramas / barras de distribución para un subconjunto de preguntas
# (para todas las 143 sería muy pesado visualizar)
# ============================================================
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("CASM83.xlsx")

# Detectar columnas de preguntas
question_cols = []
for c in df.columns:
    name = str(c).strip()
    if name.isdigit():
        question_cols.append(c)
    elif name.upper().startswith("Q") and name[1:].isdigit():
        question_cols.append(c)
if not question_cols:
    question_cols = df.columns[3:]

# Seleccionar algunas preguntas de ejemplo (ajusta según tu interés)
# Si las columnas son numéricas (1..143) puedes hacer algo así:
ejemplo_preguntas = question_cols[:6]  # primeras 6 preguntas

num_plots = len(ejemplo_preguntas)
cols = 3
rows = (num_plots + cols - 1) // cols

plt.figure(figsize=(15, 8))

for i, col in enumerate(ejemplo_preguntas, start=1):
    plt.subplot(rows, cols, i)
    # Distribución de valores 0,1,2,3
    value_counts = df[col].value_counts().sort_index()
    value_counts.plot(kind="bar")
    plt.title(f"Distribución de respuestas - Pregunta {col}")
    plt.xlabel("Respuesta (0=Ninguna,1=A,2=B,3=Ambas)")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=0)

plt.tight_layout()
plt.show()