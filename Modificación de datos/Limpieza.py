"""
FASE DE MODIFICACIÓN - METODOLOGÍA SEMMA
Test CASM83 - Análisis y Limpieza de Datos

Instrucciones:
1. Guarda este archivo como: limpieza_casm83.py
2. Coloca tu archivo Excel en la misma carpeta con nombre: CASM83.xlsx
3. Ejecuta: python limpieza_casm83.py
4. Revisa los archivos generados y el reporte en consola
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ============================================================
# CONFIGURACIÓN INICIAL
# ============================================================

# Nombre del archivo de entrada (Excel)
ARCHIVO_ENTRADA = 'CASM83.xlsx'

# Criterio de eliminación: % de respuestas en 0
UMBRAL_CEROS = 70  # Eliminar si más del 70% son ceros

# Valores válidos
VALORES_VALIDOS_RESPUESTAS = [0, 1, 2, 3]
VALORES_VALIDOS_GENERO = [0, 1]
TOTAL_PREGUNTAS = 143  # Total de preguntas en CASM83 R2014

# Escalas del CASM83 R2014 (Áreas vocacionales) - 11 preguntas por escala
ESCALAS_CASM83 = {
    "CCFM":  [1, 14, 27, 40, 53, 66, 79, 92, 105, 118, 131],   # Ciencias Físico-Matemáticas (11 items)
    "CCSS":  [2, 15, 28, 41, 54, 67, 80, 93, 106, 119, 132],   # Ciencias Sociales (11 items)
    "CCNA":  [3, 16, 29, 42, 55, 68, 81, 94, 107, 120, 133],   # Ciencias Naturales (11 items)
    "CCCO":  [4, 17, 30, 43, 56, 69, 82, 95, 108, 121, 134],   # Ciencias de la Comunicación (11 items)
    "ARTE":  [5, 18, 31, 44, 57, 70, 83, 96, 109, 122, 135],   # Artes (11 items)
    "BURO":  [6, 19, 32, 45, 58, 71, 84, 97, 110, 123, 136],   # Burocracia (11 items)
    "CCEP":  [7, 20, 33, 46, 59, 72, 85, 98, 111, 124, 137],   # Ciencias Económico-Políticas (11 items)
    "HAA":   [8, 21, 34, 47, 60, 73, 86, 99, 112, 125, 138],   # Humanidades, Arte y Arquitectura (11 items)
    "FINA":  [9, 22, 35, 48, 61, 74, 87, 100, 113, 126, 139],  # Finanzas (11 items)
    "LING":  [10, 23, 36, 49, 62, 75, 88, 101, 114, 127, 140], # Lingüística (11 items)
    "JURI":  [11, 24, 37, 50, 63, 76, 89, 102, 115, 128, 141]  # Jurídico (11 items)
}

# Escalas de control de calidad CASM83 R2014
ESCALAS_CONTROL = {
    "VERA":  [12, 25, 38, 51, 64, 77, 90, 103, 116, 129, 142], # Veracidad (11 items)
    "CONS":  [13, 26, 39, 52, 65, 78, 91, 104, 117, 130, 143]  # Consistencia (11 items)
}

# Umbrales de validez según normas CASM83 R2014
UMBRAL_VERACIDAD = 5      # Mínimo de respuestas válidas en escala de veracidad (ajustado para 11 items)
UMBRAL_CONSISTENCIA = 5   # Mínimo de respuestas consistentes (ajustado para 11 items)

# Nombres descriptivos de las escalas
NOMBRES_ESCALAS = {
    "CCFM": "Ciencias Físico-Matemáticas",
    "CCSS": "Ciencias Sociales",
    "CCNA": "Ciencias Naturales",
    "CCCO": "Ciencias de la Comunicación",
    "ARTE": "Artes",
    "BURO": "Burocracia/Administrativo",
    "CCEP": "Ciencias Económico-Políticas",
    "HAA": "Humanidades y Arquitectura",
    "FINA": "Finanzas",
    "LING": "Lingüística",
    "JURI": "Jurídico"
}

# ============================================================
# FUNCIÓN 1: CARGA Y EXPLORACIÓN INICIAL
# ============================================================

def cargar_datos(archivo):
    """Carga el dataset desde Excel y muestra información básica"""
    print("="*70)
    print("FASE 1: CARGA DE DATOS")
    print("="*70)
    
    try:
        # Leer archivo Excel
        df = pd.read_excel(archivo, engine='openpyxl')
        print(f"✓ Archivo Excel cargado exitosamente")
        print(f"✓ Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
        print(f"✓ Columnas: {list(df.columns[:5])}... (mostrando primeras 5)")
        
        # Verificar preguntas disponibles
        preguntas_cols = [col for col in df.columns if col.startswith('Pregunta_')]
        max_pregunta = max([int(col.split('_')[1]) for col in preguntas_cols]) if preguntas_cols else 0
        print(f"✓ Preguntas disponibles: Pregunta_1 hasta Pregunta_{max_pregunta}")
        
        # Advertencia si faltan preguntas
        if max_pregunta < TOTAL_PREGUNTAS:
            print(f"\n⚠️  ADVERTENCIA: El test completo CASM83 R2014 requiere {TOTAL_PREGUNTAS} preguntas")
            print(f"   Tu dataset solo tiene {max_pregunta} preguntas")
            print(f"   Se usarán solo las preguntas disponibles para el cálculo de escalas")
        
        return df
    except FileNotFoundError:
        print(f"✗ ERROR: No se encontró el archivo '{archivo}'")
        print(f"  Asegúrate de tener el archivo Excel en la misma carpeta que este script")
        return None
    except ImportError:
        print(f"✗ ERROR: Falta la biblioteca 'openpyxl' para leer archivos Excel")
        print(f"  Instálala ejecutando: pip install openpyxl")
        return None
    except Exception as e:
        print(f"✗ ERROR al cargar el archivo: {str(e)}")
        return None

# ============================================================
# FUNCIÓN 2B: VALIDACIÓN DE VERACIDAD Y CONSISTENCIA (CASM83 R2014)
# ============================================================

def evaluar_veracidad_consistencia(df):
    """Evalúa las escalas de control según normas CASM83 R2014"""
    print("\n" + "="*70)
    print("FASE 2B: VALIDACIÓN DE VERACIDAD Y CONSISTENCIA (CASM83 R2014)")
    print("="*70)
    
    # Calcular puntajes de Veracidad (solo preguntas disponibles)
    cols_vera = [f'Pregunta_{p}' for p in ESCALAS_CONTROL["VERA"] if f'Pregunta_{p}' in df.columns]
    items_vera_disponibles = len(cols_vera)
    df['puntaje_veracidad'] = df[cols_vera].apply(
        lambda row: sum(val if val in [1, 2, 3] else 0 for val in row), axis=1
    )
    
    # Calcular puntajes de Consistencia (solo preguntas disponibles)
    cols_cons = [f'Pregunta_{p}' for p in ESCALAS_CONTROL["CONS"] if f'Pregunta_{p}' in df.columns]
    items_cons_disponibles = len(cols_cons)
    df['puntaje_consistencia'] = df[cols_cons].apply(
        lambda row: sum(val if val in [1, 2, 3] else 0 for val in row), axis=1
    )
    
    print(f"\n📋 Ítems de control disponibles:")
    print(f"  • Veracidad: {items_vera_disponibles}/{len(ESCALAS_CONTROL['VERA'])} ítems")
    print(f"  • Consistencia: {items_cons_disponibles}/{len(ESCALAS_CONTROL['CONS'])} ítems")
    
    # Ajustar umbrales proporcionalmente si no hay todos los ítems
    umbral_vera_ajustado = int(UMBRAL_VERACIDAD * items_vera_disponibles / len(ESCALAS_CONTROL['VERA']))
    umbral_cons_ajustado = int(UMBRAL_CONSISTENCIA * items_cons_disponibles / len(ESCALAS_CONTROL['CONS']))
    
    if items_vera_disponibles < len(ESCALAS_CONTROL['VERA']) or items_cons_disponibles < len(ESCALAS_CONTROL['CONS']):
        print(f"\n⚠️  Umbrales ajustados proporcionalmente:")
        print(f"  • Veracidad: {umbral_vera_ajustado} (original: {UMBRAL_VERACIDAD} para 11 ítems)")
        print(f"  • Consistencia: {umbral_cons_ajustado} (original: {UMBRAL_CONSISTENCIA} para 11 ítems)")
    
    # Evaluar validez según umbrales ajustados
    df['veracidad_valida'] = df['puntaje_veracidad'] >= umbral_vera_ajustado
    df['consistencia_valida'] = df['puntaje_consistencia'] >= umbral_cons_ajustado
    df['test_valido'] = df['veracidad_valida'] & df['consistencia_valida']
    
    # Estadísticas
    total = len(df)
    invalidos_veracidad = (~df['veracidad_valida']).sum()
    invalidos_consistencia = (~df['consistencia_valida']).sum()
    invalidos_total = (~df['test_valido']).sum()
    
    print(f"\n📋 RESULTADOS DE VALIDACIÓN:")
    print(f"  • Total de registros evaluados: {total}")
    print(f"  • Inválidos por VERACIDAD (< {umbral_vera_ajustado} pts): {invalidos_veracidad} ({invalidos_veracidad/total*100:.2f}%)")
    print(f"  • Inválidos por CONSISTENCIA (< {umbral_cons_ajustado} pts): {invalidos_consistencia} ({invalidos_consistencia/total*100:.2f}%)")
    print(f"  • TOTAL INVÁLIDOS: {invalidos_total} ({invalidos_total/total*100:.2f}%)")
    
    if invalidos_total > 0:
        print(f"\n⚠️  Registros que no cumplen normas CASM83 R2014:")
        invalidos_df = df[~df['test_valido']][['ID', 'puntaje_veracidad', 'puntaje_consistencia', 
                                                 'veracidad_valida', 'consistencia_valida']].head(10)
        for idx, row in invalidos_df.iterrows():
            motivo = []
            if not row['veracidad_valida']:
                motivo.append(f"Veracidad={row['puntaje_veracidad']}/{items_vera_disponibles}")
            if not row['consistencia_valida']:
                motivo.append(f"Consistencia={row['puntaje_consistencia']}/{items_cons_disponibles}")
            print(f"  • ID {row['ID']:3.0f}: {', '.join(motivo)}")
        if invalidos_total > 10:
            print(f"  ... y {invalidos_total - 10} más")
    
    return df

def analizar_calidad(df):
    """Analiza la calidad de los datos y detecta problemas"""
    print("\n" + "="*70)
    print("FASE 2: ANÁLISIS DE CALIDAD")
    print("="*70)
    
    # Seleccionar solo columnas de preguntas disponibles
    preguntas_cols = [col for col in df.columns if col.startswith('Pregunta_')]
    num_preguntas_disponibles = len(preguntas_cols)
    
    print(f"\n📊 Preguntas disponibles para análisis: {num_preguntas_disponibles}/{TOTAL_PREGUNTAS}")
    
    # Calcular porcentaje de ceros por registro (sobre preguntas disponibles)
    df['porcentaje_ceros'] = (df[preguntas_cols] == 0).sum(axis=1) / num_preguntas_disponibles * 100
    df['total_ceros'] = (df[preguntas_cols] == 0).sum(axis=1)
    df['total_respuesta_A'] = (df[preguntas_cols] == 1).sum(axis=1)
    df['total_respuesta_B'] = (df[preguntas_cols] == 2).sum(axis=1)
    df['total_respuesta_ambos'] = (df[preguntas_cols] == 3).sum(axis=1)
    
    # Estadísticas generales
    print("\n📊 ESTADÍSTICAS GENERALES:")
    print(f"  • Promedio de ceros por registro: {df['porcentaje_ceros'].mean():.2f}%")
    print(f"  • Mediana de ceros: {df['porcentaje_ceros'].median():.2f}%")
    print(f"  • Máximo de ceros: {df['porcentaje_ceros'].max():.2f}%")
    
    # Detectar valores fuera de rango
    valores_invalidos = []
    for col in preguntas_cols:
        invalidos = df[~df[col].isin(VALORES_VALIDOS_RESPUESTAS)]
        if not invalidos.empty:
            valores_invalidos.append((col, invalidos))
    
    if valores_invalidos:
        print("\n⚠️  VALORES INVÁLIDOS DETECTADOS:")
        for col, inv in valores_invalidos:
            print(f"  • {col}: {inv[col].unique()}")
    else:
        print("\n✓ Todos los valores están en el rango válido [0, 1, 2, 3]")
    
    return df

# ============================================================
# FUNCIÓN 3: IDENTIFICAR REGISTROS A ELIMINAR
# ============================================================

def identificar_registros_invalidos(df, umbral):
    """Identifica registros inválidos por múltiples criterios"""
    print("\n" + "="*70)
    print("FASE 3: IDENTIFICACIÓN DE REGISTROS INVÁLIDOS")
    print("="*70)
    
    print(f"\n🔍 CRITERIOS DE ELIMINACIÓN:")
    print(f"  1. Más del {umbral}% de respuestas en 0 (sin interés)")
    print(f"  2. Veracidad < {UMBRAL_VERACIDAD} puntos (respuestas no veraces)")
    print(f"  3. Consistencia < {UMBRAL_CONSISTENCIA} puntos (respuestas inconsistentes)")
    
    # Criterio 1: Exceso de ceros
    invalidos_ceros = df[df['porcentaje_ceros'] > umbral]
    
    # Criterio 2 y 3: Escalas de control
    invalidos_control = df[~df['test_valido']]
    
    # Combinar ambos criterios (unión)
    ids_invalidos = set(invalidos_ceros['ID'].tolist()) | set(invalidos_control['ID'].tolist())
    registros_invalidos = df[df['ID'].isin(ids_invalidos)].copy()
    
    # Clasificar motivo de eliminación
    def clasificar_motivo(row):
        motivos = []
        if row['porcentaje_ceros'] > umbral:
            motivos.append(f"Exceso ceros ({row['porcentaje_ceros']:.1f}%)")
        if not row['veracidad_valida']:
            motivos.append(f"Veracidad baja ({row['puntaje_veracidad']}/{len(ESCALAS_CONTROL['VERA'])})")
        if not row['consistencia_valida']:
            motivos.append(f"Consistencia baja ({row['puntaje_consistencia']}/{len(ESCALAS_CONTROL['CONS'])})")
        return " | ".join(motivos)
    
    registros_invalidos['motivo_eliminacion'] = registros_invalidos.apply(clasificar_motivo, axis=1)
    
    print(f"\n📋 REGISTROS A ELIMINAR: {len(registros_invalidos)}")
    print(f"  • Por exceso de ceros: {len(invalidos_ceros)}")
    print(f"  • Por control de calidad: {len(invalidos_control)}")
    print(f"  • Total únicos: {len(registros_invalidos)}")
    
    if not registros_invalidos.empty:
        print("\n⚠️  Detalle de registros problemáticos:")
        print("-" * 70)
        for idx, row in registros_invalidos.iterrows():
            print(f"  ID {row['ID']:3.0f} | {row['motivo_eliminacion']}")
    
    return registros_invalidos

# ============================================================
# FUNCIÓN 4: LIMPIEZA Y FILTRADO
# ============================================================

def limpiar_datos(df, registros_invalidos):
    """Elimina registros problemáticos"""
    print("\n" + "="*70)
    print("FASE 4: LIMPIEZA DE DATOS")
    print("="*70)
    
    # Guardar tamaño original
    filas_originales = len(df)
    
    # Eliminar registros inválidos
    ids_eliminar = registros_invalidos['ID'].tolist()
    df_limpio = df[~df['ID'].isin(ids_eliminar)].copy()
    
    # Eliminar columnas auxiliares temporales
    columnas_eliminar = ['porcentaje_ceros', 'total_ceros', 'total_respuesta_A', 
                         'total_respuesta_B', 'total_respuesta_ambos',
                         'puntaje_veracidad', 'puntaje_consistencia',
                         'veracidad_valida', 'consistencia_valida', 'test_valido']
    df_limpio = df_limpio.drop(columns=columnas_eliminar, errors='ignore')
    
    filas_finales = len(df_limpio)
    
    print(f"\n✓ Registros eliminados: {filas_originales - filas_finales}")
    print(f"✓ Registros conservados: {filas_finales}")
    print(f"✓ Tasa de retención: {(filas_finales/filas_originales)*100:.2f}%")
    
    return df_limpio

# ============================================================
# FUNCIÓN 5: CREAR VARIABLES DERIVADAS
# ============================================================

def crear_variables_derivadas(df):
    """Crea nuevas variables útiles para análisis"""
    print("\n" + "="*70)
    print("FASE 5: CREACIÓN DE VARIABLES DERIVADAS")
    print("="*70)
    
    preguntas_cols = [col for col in df.columns if col.startswith('Pregunta_')]
    num_preguntas_disponibles = len(preguntas_cols)
    
    # ========== VARIABLES DE CONTEO GENERAL ==========
    df['total_ninguno'] = (df[preguntas_cols] == 0).sum(axis=1)
    df['total_opcion_A'] = (df[preguntas_cols] == 1).sum(axis=1)
    df['total_opcion_B'] = (df[preguntas_cols] == 2).sum(axis=1)
    df['total_ambos'] = (df[preguntas_cols] == 3).sum(axis=1)
    
    # Porcentajes generales (sobre preguntas disponibles)
    df['porc_ninguno'] = (df['total_ninguno'] / num_preguntas_disponibles * 100).round(2)
    df['porc_opcion_A'] = (df['total_opcion_A'] / num_preguntas_disponibles * 100).round(2)
    df['porc_opcion_B'] = (df['total_opcion_B'] / num_preguntas_disponibles * 100).round(2)
    df['porc_ambos'] = (df['total_ambos'] / num_preguntas_disponibles * 100).round(2)
    
    # Respuestas válidas (diferente de 0)
    df['respuestas_validas'] = num_preguntas_disponibles - df['total_ninguno']
    df['tasa_completitud'] = (df['respuestas_validas'] / num_preguntas_disponibles * 100).round(2)
    
    # Etiquetas de género
    df['genero_etiqueta'] = df['Genero'].map({0: 'Femenino', 1: 'Masculino'})
    
    print("✓ Variables generales creadas:")
    print("  • Contadores: total_ninguno, total_opcion_A, total_opcion_B, total_ambos")
    print("  • Porcentajes: porc_ninguno, porc_opcion_A, porc_opcion_B, porc_ambos")
    print("  • Calidad: respuestas_validas, tasa_completitud")
    print("  • Etiquetas: genero_etiqueta")
    
    # ========== PUNTAJES POR ESCALA VOCACIONAL ==========
    print("\n✓ Calculando puntajes por área vocacional (11 ítems por escala)...")
    
    escalas_incompletas = []
    
    for escala, preguntas in ESCALAS_CASM83.items():
        # Columnas correspondientes a esta escala
        cols_escala = [f'Pregunta_{p}' for p in preguntas]
        
        # Filtrar solo las columnas que existen en el dataframe
        cols_existentes = [col for col in cols_escala if col in df.columns]
        items_disponibles = len(cols_existentes)
        
        if items_disponibles < len(preguntas):
            escalas_incompletas.append((escala, items_disponibles, len(preguntas)))
        
        # Calcular puntaje: suma de respuestas donde eligió A (1), B (2) o Ambos (3)
        df[f'puntaje_{escala}'] = df[cols_existentes].apply(
            lambda row: sum(val if val in [1, 2, 3] else 0 for val in row), axis=1
        )
        
        # Porcentaje de interés en esta área (sobre el máximo posible)
        max_puntaje = items_disponibles * 3  # Máximo si todas son "ambos" (3)
        df[f'porc_{escala}'] = ((df[f'puntaje_{escala}'] / max_puntaje) * 100).round(2) if max_puntaje > 0 else 0
    
    if escalas_incompletas:
        print(f"\n⚠️  Escalas con ítems faltantes (se usarán los disponibles):")
        for escala, disponibles, total in escalas_incompletas:
            print(f"  • {escala}: {disponibles}/{total} ítems ({disponibles/total*100:.0f}%)")
    
    # Identificar área dominante (mayor puntaje)
    escalas_puntaje = [f'puntaje_{e}' for e in ESCALAS_CASM83.keys()]
    df['area_dominante'] = df[escalas_puntaje].idxmax(axis=1).str.replace('puntaje_', '')
    df['puntaje_dominante'] = df[escalas_puntaje].max(axis=1)
    
    # Mapear código de escala a nombre completo
    df['area_dominante_nombre'] = df['area_dominante'].map(NOMBRES_ESCALAS)
    
    print(f"  • Puntajes por escala: {', '.join([f'puntaje_{e}' for e in ESCALAS_CASM83.keys()])}")
    print(f"  • Porcentajes por escala: {', '.join([f'porc_{e}' for e in ESCALAS_CASM83.keys()])}")
    print(f"  • Área dominante identificada para cada estudiante")
    
    return df

# ============================================================
# FUNCIÓN 6: GENERAR REPORTES
# ============================================================

def generar_reportes(df_original, df_limpio, registros_invalidos):
    """Genera reportes estadísticos y visualizaciones"""
    print("\n" + "="*70)
    print("FASE 6: GENERACIÓN DE REPORTES")
    print("="*70)
    
    # Reporte de texto
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_reporte = f'reporte_limpieza_{timestamp}.txt'
    
    with open(nombre_reporte, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("REPORTE DE LIMPIEZA - DATASET CASM83\n")
        f.write("Fase: MODIFICACIÓN (SEMMA)\n")
        f.write("="*70 + "\n\n")
        
        f.write("1. RESUMEN DE DATOS ORIGINALES\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total de registros: {len(df_original)}\n")
        f.write(f"Total de preguntas: {TOTAL_PREGUNTAS}\n\n")
        
        f.write("2. CRITERIO DE LIMPIEZA\n")
        f.write("-" * 70 + "\n")
        f.write(f"Criterio 1: > {UMBRAL_CEROS}% de respuestas en 0 (sin interés)\n")
        f.write(f"Criterio 2: Veracidad < {UMBRAL_VERACIDAD} puntos (según CASM83 R2014)\n")
        f.write(f"Criterio 3: Consistencia < {UMBRAL_CONSISTENCIA} puntos (según CASM83 R2014)\n\n")
        
        f.write("3. REGISTROS ELIMINADOS\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total eliminados: {len(registros_invalidos)}\n")
        if not registros_invalidos.empty:
            f.write("\nIDs eliminados (con motivo):\n")
            for idx, row in registros_invalidos.iterrows():
                f.write(f"  - ID {row['ID']}: {row['motivo_eliminacion']}\n")
        f.write("\n")
        
        f.write("4. RESUMEN DE DATOS LIMPIOS\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total de registros: {len(df_limpio)}\n")
        f.write(f"Tasa de retención: {(len(df_limpio)/len(df_original)*100):.2f}%\n\n")
        
        f.write("5. ESTADÍSTICAS DESCRIPTIVAS (DATOS LIMPIOS)\n")
        f.write("-" * 70 + "\n")
        f.write(f"Promedio tasa de completitud: {df_limpio['tasa_completitud'].mean():.2f}%\n")
        f.write(f"Promedio respuestas 'Ninguno': {df_limpio['porc_ninguno'].mean():.2f}%\n")
        f.write(f"Promedio respuestas 'Opción A': {df_limpio['porc_opcion_A'].mean():.2f}%\n")
        f.write(f"Promedio respuestas 'Opción B': {df_limpio['porc_opcion_B'].mean():.2f}%\n")
        f.write(f"Promedio respuestas 'Ambos': {df_limpio['porc_ambos'].mean():.2f}%\n\n")
        
        f.write("6. DISTRIBUCIÓN POR GÉNERO\n")
        f.write("-" * 70 + "\n")
        dist_genero = df_limpio['genero_etiqueta'].value_counts()
        for genero, count in dist_genero.items():
            f.write(f"{genero}: {count} ({count/len(df_limpio)*100:.2f}%)\n")
        f.write("\n")
        
        f.write("7. DISTRIBUCIÓN POR GRADO\n")
        f.write("-" * 70 + "\n")
        dist_grado = df_limpio['Grado'].value_counts().sort_index()
        for grado, count in dist_grado.items():
            f.write(f"Grado {grado}: {count} ({count/len(df_limpio)*100:.2f}%)\n")
        f.write("\n")
        
        f.write("8. ÁREAS VOCACIONALES MÁS POPULARES\n")
        f.write("-" * 70 + "\n")
        dist_areas = df_limpio['area_dominante_nombre'].value_counts()
        for area, count in dist_areas.items():
            f.write(f"{area}: {count} estudiantes ({count/len(df_limpio)*100:.2f}%)\n")
        f.write("\n")
        
        f.write("9. PUNTAJES PROMEDIO POR ÁREA VOCACIONAL\n")
        f.write("-" * 70 + "\n")
        for escala, nombre in NOMBRES_ESCALAS.items():
            puntaje_promedio = df_limpio[f'puntaje_{escala}'].mean()
            porc_promedio = df_limpio[f'porc_{escala}'].mean()
            f.write(f"{nombre:35s}: {puntaje_promedio:5.2f} pts ({porc_promedio:5.2f}%)\n")
    
    print(f"✓ Reporte guardado: {nombre_reporte}")
    
    # Generar visualizaciones
    generar_visualizaciones(df_limpio)
    
    return nombre_reporte

# ============================================================
# FUNCIÓN 7: VISUALIZACIONES
# ============================================================

def generar_visualizaciones(df):
    """Crea gráficos de análisis"""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Análisis del Dataset CASM83 - Datos Limpios', fontsize=16, fontweight='bold')
    
    # Gráfico 1: Distribución de respuestas por tipo
    ax1 = axes[0, 0]
    tipos = ['Ninguno', 'Opción A', 'Opción B', 'Ambos']
    promedios = [
        df['porc_ninguno'].mean(),
        df['porc_opcion_A'].mean(),
        df['porc_opcion_B'].mean(),
        df['porc_ambos'].mean()
    ]
    ax1.bar(tipos, promedios, color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'])
    ax1.set_ylabel('Porcentaje Promedio (%)')
    ax1.set_title('Distribución Promedio de Tipos de Respuesta')
    ax1.set_ylim(0, max(promedios) * 1.2)
    for i, v in enumerate(promedios):
        ax1.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
    
    # Gráfico 2: Distribución por género
    ax2 = axes[0, 1]
    dist_genero = df['genero_etiqueta'].value_counts()
    colors = ['#ff6b6b', '#4ecdc4']
    ax2.pie(dist_genero.values, labels=dist_genero.index, autopct='%1.1f%%', 
            colors=colors, startangle=90)
    ax2.set_title('Distribución por Género')
    
    # Gráfico 3: Distribución de tasa de completitud
    ax3 = axes[0, 2]
    ax3.hist(df['tasa_completitud'], bins=20, color='#45b7d1', edgecolor='black', alpha=0.7)
    ax3.axvline(df['tasa_completitud'].mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Media: {df["tasa_completitud"].mean():.1f}%')
    ax3.set_xlabel('Tasa de Completitud (%)')
    ax3.set_ylabel('Frecuencia')
    ax3.set_title('Distribución de Tasa de Completitud')
    ax3.legend()
    
    # Gráfico 4: Top 5 Áreas Vocacionales
    ax4 = axes[1, 0]
    dist_areas = df['area_dominante'].value_counts().head(5)
    colores_areas = plt.cm.Set3(range(len(dist_areas)))
    ax4.barh(range(len(dist_areas)), dist_areas.values, color=colores_areas)
    ax4.set_yticks(range(len(dist_areas)))
    ax4.set_yticklabels([NOMBRES_ESCALAS[area] for area in dist_areas.index])
    ax4.set_xlabel('Número de Estudiantes')
    ax4.set_title('Top 5 Áreas Vocacionales Dominantes')
    for i, v in enumerate(dist_areas.values):
        ax4.text(v + 0.3, i, str(v), va='center', fontweight='bold')
    
    # Gráfico 5: Puntajes promedio por área
    ax5 = axes[1, 1]
    escalas = list(ESCALAS_CASM83.keys())
    puntajes_prom = [df[f'puntaje_{e}'].mean() for e in escalas]
    ax5.bar(range(len(escalas)), puntajes_prom, color='#96ceb4', edgecolor='black')
    ax5.set_xticks(range(len(escalas)))
    ax5.set_xticklabels(escalas, rotation=45, ha='right')
    ax5.set_ylabel('Puntaje Promedio')
    ax5.set_title('Puntaje Promedio por Área Vocacional')
    ax5.grid(axis='y', alpha=0.3)
    
    # Gráfico 6: Distribución por grado
    ax6 = axes[1, 2]
    dist_grado = df['Grado'].value_counts().sort_index()
    ax6.bar(dist_grado.index.astype(str), dist_grado.values, color='#feca57', edgecolor='black')
    ax6.set_xlabel('Grado')
    ax6.set_ylabel('Número de Estudiantes')
    ax6.set_title('Distribución por Grado Académico')
    for i, v in enumerate(dist_grado.values):
        ax6.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
    
    plt.tight_layout()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_grafico = f'visualizacion_datos_{timestamp}.png'
    plt.savefig(nombre_grafico, dpi=300, bbox_inches='tight')
    print(f"✓ Visualización guardada: {nombre_grafico}")
    
    # Crear gráfico adicional: Heatmap de áreas por género
    crear_heatmap_areas_genero(df)
    
    return nombre_grafico

def crear_heatmap_areas_genero(df):
    """Crea un heatmap de distribución de áreas por género"""
    
    # Crear tabla cruzada
    tabla = pd.crosstab(df['area_dominante_nombre'], df['genero_etiqueta'])
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(tabla, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': 'Cantidad'})
    plt.title('Distribución de Áreas Vocacionales por Género', fontsize=14, fontweight='bold')
    plt.xlabel('Género')
    plt.ylabel('Área Vocacional')
    plt.tight_layout()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_heatmap = f'heatmap_areas_genero_{timestamp}.png'
    plt.savefig(nombre_heatmap, dpi=300, bbox_inches='tight')
    print(f"✓ Heatmap guardado: {nombre_heatmap}")
    plt.close()

# ============================================================
# FUNCIÓN 8: EXPORTAR DATOS LIMPIOS
# ============================================================

def exportar_datos(df, registros_invalidos):
    """Exporta los datos procesados en Excel y CSV"""
    print("\n" + "="*70)
    print("FASE 7: EXPORTACIÓN DE DATOS")
    print("="*70)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Exportar dataset limpio en Excel
    archivo_limpio_excel = f'CASM83_limpio_{timestamp}.xlsx'
    df.to_excel(archivo_limpio_excel, index=False, engine='openpyxl')
    print(f"✓ Dataset limpio guardado (Excel): {archivo_limpio_excel}")
    
    # También exportar en CSV para compatibilidad
    archivo_limpio_csv = f'CASM83_limpio_{timestamp}.csv'
    df.to_csv(archivo_limpio_csv, index=False, encoding='utf-8')
    print(f"✓ Dataset limpio guardado (CSV): {archivo_limpio_csv}")
    
    # Exportar registros eliminados
    if not registros_invalidos.empty:
        archivo_eliminados = f'registros_eliminados_{timestamp}.xlsx'
        registros_invalidos.to_excel(archivo_eliminados, index=False, engine='openpyxl')
        print(f"✓ Registros eliminados guardados: {archivo_eliminados}")
    
    return archivo_limpio_excel

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """Función principal que ejecuta todo el proceso"""
    
    print("\n" + "🎯 " * 25)
    print("ANÁLISIS Y LIMPIEZA DE DATOS - TEST CASM83")
    print("Metodología SEMMA - Fase: MODIFICACIÓN")
    print("Aplicando normas: CASM83 R2014 (Veracidad y Consistencia)")
    print("🎯 " * 25)
    
    # 1. Cargar datos
    df = cargar_datos(ARCHIVO_ENTRADA)
    if df is None:
        return
    
    # 2. Análisis de calidad
    df = analizar_calidad(df)
    
    # 2B. Validación de veracidad y consistencia (CASM83 R2014)
    df = evaluar_veracidad_consistencia(df)
    
    # 3. Identificar registros inválidos
    registros_invalidos = identificar_registros_invalidos(df, UMBRAL_CEROS)
    
    # 4. Limpiar datos
    df_limpio = limpiar_datos(df, registros_invalidos)
    
    # 5. Crear variables derivadas
    df_limpio = crear_variables_derivadas(df_limpio)
    
    # 6. Generar reportes
    reporte = generar_reportes(df, df_limpio, registros_invalidos)
    
    # 7. Exportar datos
    archivo_final = exportar_datos(df_limpio, registros_invalidos)
    
    # Resumen final
    print("\n" + "="*70)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("="*70)
    print(f"\n📁 Archivos generados:")
    print(f"  1. {archivo_final} (dataset limpio)")
    print(f"  2. {reporte} (reporte detallado)")
    print(f"  3. visualizacion_datos_*.png (gráficos)")
    if not registros_invalidos.empty:
        print(f"  4. registros_eliminados_*.csv (IDs eliminados)")
    
    print(f"\n📊 Estadísticas finales:")
    print(f"  • Total registros válidos: {len(df_limpio)}")
    print(f"  • Promedio de completitud: {df_limpio['tasa_completitud'].mean():.2f}%")
    print(f"  • Validados según normas CASM83 R2014")
    print(f"  • Dataset listo para FASE DE MODELADO")
    
    print("\n" + "🎯 " * 25 + "\n")

# ============================================================
# EJECUTAR PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()