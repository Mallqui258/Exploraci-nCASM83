import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("CASM83.xlsx")

# 2. Detectar columnas de preguntas (nombres numéricos o tipo Q1, Q2...)
question_cols = []
for c in df.columns:
    name = str(c).strip()
    if name.isdigit():
        question_cols.append(c)
    elif name.upper().startswith("Q") and name[1:].isdigit():
        question_cols.append(c)

# Si no detecta nada, AJUSTA manualmente
if not question_cols:
    # Ejemplo: si las 3 primeras columnas son id, sexo, grado
    question_cols = df.columns[3:]

# 3. Heatmap de missing
plt.figure(figsize=(14, 6))
sns.heatmap(df[question_cols].isna(), cbar=True)
plt.title("Heatmap de valores faltantes por pregunta")
plt.xlabel("Preguntas")
plt.ylabel("Estudiantes")
plt.tight_layout()
plt.show()