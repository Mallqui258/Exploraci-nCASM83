# heatmap_atipicos_normales.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1) Cargar dataset
df = pd.read_excel("CASM83.xlsx")

# 2) Detectar columnas de preguntas (tipo 'Pregunta_1', 'Pregunta_2', ...)
question_cols = [c for c in df.columns if str(c).startswith("Pregunta_")]

if not question_cols:
    raise ValueError("No se encontraron columnas que empiecen con 'Pregunta_'.")

# Matriz solo de respuestas
df_q = df[question_cols].copy()

# 3) Función para marcar estudiantes atípicos:
#    solo usan respuestas 0 y/o 3 en TODAS las preguntas contestadas
def es_atipico(fila):
    vals = fila.dropna().unique()          # respuestas usadas por ese estudiante
    if len(vals) == 0:
        return False                       # si no respondió nada, no lo marcamos
    return set(vals).issubset({0, 3})      # solo 0 y/o 3 → atípico

mask_atip = df_q.apply(es_atipico, axis=1)

# 4) Separar atípicos y normales
df_atip = df_q[mask_atip]
df_norm = df_q[~mask_atip]

print(f"Estudiantes atípicos: {df_atip.shape[0]}")
print(f"Estudiantes normales: {df_norm.shape[0]}")

# 5) Unir en un solo DataFrame (atípicos arriba, normales abajo)
df_heat = pd.concat([df_atip, df_norm], axis=0)

# Opcional: renombrar columnas para que se vea solo el número de la pregunta
new_cols = []
for c in df_heat.columns:
    # intenta extraer el número después de 'Pregunta_'
    try:
        num = int(str(c).split("_")[1])
        new_cols.append(num)
    except Exception:
        new_cols.append(c)

df_heat.columns = new_cols

# 6) Dibujar mapa de calor
plt.figure(figsize=(14, 8))
sns.set(style="white")

ax = sns.heatmap(
    df_heat,
    cmap="viridis",           # puedes cambiar la paleta si quieres
    cbar_kws={"label": "Respuesta (0–3)"},
    linewidths=0.0
)

ax.set_xlabel("Número de pregunta")
ax.set_ylabel("Estudiantes\n(Atípicos arriba, Normales abajo)")
ax.set_title("Mapa de calor de respuestas: atípicos (0 y 3) vs normales")

# Línea roja para separar atípicos y normales
n_atip = df_atip.shape[0]
if n_atip > 0 and n_atip < df_heat.shape[0]:
    ax.hlines(n_atip, *ax.get_xlim(), colors="red", linewidth=2)

plt.tight_layout()
plt.show()
