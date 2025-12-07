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

# Contar missing por pregunta
missing_counts = df[question_cols].isna().sum()

# --- Limpiar las etiquetas: quedarnos solo con los dígitos ---
labels = []
for col in missing_counts.index:
    txt = str(col)
    # extrae solo los números del nombre de la columna
    digits = "".join(ch for ch in txt if ch.isdigit())
    labels.append(digits if digits else txt)

plt.figure(figsize=(16, 6))
ax = plt.gca()
ax.bar(range(len(missing_counts)), missing_counts.values)

plt.title("Número de omisiones por pregunta")
plt.xlabel("Pregunta")
plt.ylabel("Cantidad de respuestas faltantes")

plt.xticks(range(len(missing_counts)), labels, rotation=90)
plt.tight_layout()
plt.show()

"""
plt.figure(figsize=(16, 6))
missing_counts.plot(kind="bar")
plt.title("Número de omisiones por pregunta")
plt.xlabel("Pregunta")
plt.ylabel("Cantidad de respuestas faltantes")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
"""