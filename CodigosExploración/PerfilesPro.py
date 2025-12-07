import pandas as pd
import matplotlib.pyplot as plt

# ================================
# 1. Cargar datos
# ================================
ARCHIVO = "CASM83.xlsx"   # Cambia el nombre si tu archivo se llama distinto
df = pd.read_excel(ARCHIVO)

# ================================
# 2. Definir ítems por escala vocacional
#    (solo las 11 áreas, sin VERA ni CONS)
# ================================
ESCALAS_VOC = {
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
}

NOMBRES_ESCALAS = {
    "CCFM": "CCFM",
    "CCSS": "CCSS",
    "CCNA": "CCNA",
    "CCCO": "CCCO",
    "ARTE": "ARTE",
    "BURO": "Buro",
    "CCEP": "CCEP",
    "HAA":  "HAA",
    "FINA": "Finanzas",
    "LING": "Lingüística",
    "JURI": "Jurídico",
}

def col_from_num(n: int):
    col = f"Pregunta_{n}"
    return col if col in df.columns else None

# ================================
# 3. Calcular puntajes por área y área dominante
# ================================
puntajes = {}

for escala, items in ESCALAS_VOC.items():
    cols = [col_from_num(i) for i in items]
    cols = [c for c in cols if c is not None]

    if not cols:
        print(f"[AVISO] La escala {escala} no tiene columnas válidas en el archivo.")
        continue

    # Suma de respuestas A(1), B(2) o Ambos(3); 0 cuenta como 0
    puntajes[escala] = df[cols].apply(
        lambda fila: sum(v if v in (1, 2, 3) else 0 for v in fila),
        axis=1
    )

puntajes_df = pd.DataFrame(puntajes)

# Área con mayor puntaje por estudiante
df["area_dominante"] = puntajes_df.idxmax(axis=1)
df["area_dominante_nombre"] = df["area_dominante"].map(NOMBRES_ESCALAS)

# ================================
# 4. Conteo de áreas dominantes
# ================================
conteo = df["area_dominante_nombre"].value_counts().sort_index()
porcentaje = (conteo / conteo.sum() * 100).round(1)

print("Distribución de áreas vocacionales dominantes:")
print(pd.DataFrame({"frecuencia": conteo, "porcentaje": porcentaje}))

# ================================
# 5. Gráfico de barras
# ================================
plt.figure(figsize=(10, 6))

plt.bar(conteo.index.astype(str), conteo.values)

plt.xlabel("Áreas vocacionales dominantes")
plt.ylabel("Número de estudiantes")
plt.title("Distribución de las áreas vocacionales")
plt.xticks(rotation=45, ha="right")

# Porcentaje encima de cada barra
for x, y, p in zip(range(len(conteo)), conteo.values, porcentaje.values):
    plt.text(x, y + 0.5, f"{p}%", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.savefig("distribucion_areas.png", dpi=300)
plt.show()
