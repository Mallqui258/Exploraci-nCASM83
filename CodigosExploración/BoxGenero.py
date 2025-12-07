# boxplot_genero.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Cargar dataset
df = pd.read_excel("CASM83.xlsx")

# 2. Detectar columnas de preguntas
question_cols = [c for c in df.columns if str(c).startswith("Pregunta_")]
if not question_cols:
    raise ValueError("No se encontraron columnas 'Pregunta_'.")

# 3. Calcular promedio de respuesta por estudiante
df["promedio_respuestas"] = df[question_cols].mean(axis=1)

# 4. Verificar columna de género
if "Genero" not in df.columns:
    raise ValueError("No se encontró la columna 'Genero' en el archivo.")

# Si está codificado 0/1, convertir a texto
if set(df["Genero"].dropna().unique()) <= {0, 1}:
    df["Genero_label"] = df["Genero"].map({0: "Femenino", 1: "Masculino"})
else:
    df["Genero_label"] = df["Genero"].astype(str)

# 5. Boxplot
sns.set(style="whitegrid")
plt.figure(figsize=(6, 5))
sns.boxplot(data=df, x="Genero_label", y="promedio_respuestas")
plt.title("Distribución del promedio de respuestas por Género")
plt.xlabel("Género")
plt.ylabel("Promedio de respuesta (0–3)")
plt.tight_layout()
plt.show()
