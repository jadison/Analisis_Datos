
"""
Proyecto final – Análisis de datos
Internet Fijo – Accesos por tecnología y segmento 
Enlace: https://www.datos.gov.co/Ciencia-Tecnolog-a-e-Innovaci-n/Internet-Fijo-Accesos-por-tecnolog-a-y-segmento/n48w-gutb/about_data

Pasos realizados en el análisis:

1. Carga del archivo CSV.
2. Exploración inicial de los datos.
3. Limpieza y preparación de datos.
4. Análisis descriptivo:
   - Estadísticas de accesos.
   - Accesos por departamento, municipio, tecnología y segmento.
   - Evolución de accesos por año.
   - Tecnologías principales y su evolución en el tiempo.
   - Velocidad promedio por tecnología.
   - Porcentaje de accesos por tipo de segmento.
5. Generación de gráficas y guardado de imágenes en una carpeta.

Estudiante: Jadison Yulian Ramirez Durango
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


def main():
    # -------------------------------------------------------------------------
    # 0. CONFIGURACIÓN INICIAL
    # -------------------------------------------------------------------------

    # Nombre del archivo CSV 
    CSV_FILE = "Internet_Fijo_Accesos_por_tecnología_y_segmento_20251210.csv"

    # Caperta para guardar gráficos
    
    OUTPUT_DIR = "graficos"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

   
    plt.rcParams["figure.figsize"] = (10, 5)

    print("============================================")
    print("  ANÁLISIS DE INTERNET FIJO EN COLOMBIA  ")   
    print("============================================\n")
    print("Cargando datos desde:", CSV_FILE)

    # -------------------------------------------------------------------------
    # 1. CARGA DEL CSV
    # -------------------------------------------------------------------------
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"\n[ERROR] No se encontró el archivo '{CSV_FILE}'.")
     
        return

    print("\n=== EXPLORACIÓN INICIAL ===\n")
    print("Dimensiones de los datos (filas, columnas):", df.shape)

    print("\nColumnas originales:")
    print(df.columns)

    print("\nPrimeras 5 filas:")
    print(df.head())

    print("\nInformación general de los datos:")
    print(df.info())

    # -------------------------------------------------------------------------
    # 2. RENOMBRAR COLUMNAS PARA TRABAJAR MÁS CÓMODO
    # -------------------------------------------------------------------------
     
    df = df.rename(columns={
        "AÑO": "anio",
        "TRIMESTRE": "trimestre",
        "PROVEEDOR": "proveedor",
        "COD_DEPARTAMENTO": "cod_departamento",
        "DEPARTAMENTO": "departamento",
        "COD_MUNICIPIO": "cod_municipio",
        "MUNICIPIO": "municipio",
        "SEGMENTO": "segmento",
        "TECNOLOGIA": "tecnologia",
        "VELOCIDAD_BAJADA": "velocidad_bajada",
        "VELOCIDAD_SUBIDA": "velocidad_subida",
        "No DE ACCESOS": "accesos"
    })

    print("\nColumnas despues de renombrar:")
    print(df.columns)

    # -------------------------------------------------------------------------
    # 3. LIMPIEZA DE DATOS
    # -------------------------------------------------------------------------
    print("\n=== LIMPIEZA DE DATOS ===\n")

    
    print("Valores nulos por columna (antes de limpiar):")
    print(df.isna().sum())

    # 3.1 Asegurar que la columna 'accesos' sea numerica
    
    df["accesos"] = pd.to_numeric(df["accesos"], errors="coerce")

    # 3.2 Manejo de velocidades con coma decimal
    
    for col in ["velocidad_bajada", "velocidad_subida"]:
        df[col] = df[col].astype(str).str.replace(",", ".", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3.3 Eliminar filas sin dato de accesos
    
    filas_antes = df.shape[0]
    df = df.dropna(subset=["accesos"])
    filas_despues = df.shape[0]
    
    print(f"\nFilas eliminadas por accesos nulos: {filas_antes - filas_despues}")

    # 3.4 Crear columna de periodo (ej: "2020-T1")
    
    df["periodo"] = df["anio"].astype(str) + "-T" + df["trimestre"].astype(str)

    # 3.5 Crear columna de tipo_segmento simplificada
    
    def clasificar_segmento(seg):
        if isinstance(seg, str):
            texto = seg.upper()
            if "RESIDENCIAL" in texto:
                return "RESIDENCIAL"
            if "CORPORATIVO" in texto:
                return "CORPORATIVO"
        return "OTRO"

    df["tipo_segmento"] = df["segmento"].apply(clasificar_segmento)

    print("\nDistribución de 'tipo_segmento':")
    print(df["tipo_segmento"].value_counts())

    print("\nValores nulos por columna (después de limpiar):")
    print(df.isna().sum())

    # -------------------------------------------------------------------------
    # 4. ANÁLISIS DESCRIPTIVO BÁSICO
    # -------------------------------------------------------------------------
    
    print("\n=== ANÁLISIS DESCRIPTIVO GENERAL ===\n")

    print("Estadísticas básicas de 'accesos':")
    print(df["accesos"].describe())

    # 4.1 Accesos totales por departamento (ordenados de mayor a menor)
    
    accesos_dep = df.groupby("departamento")["accesos"].sum().sort_values(ascending=False)
    print("\nTop 10 departamentos por número total de accesos:")
    print(accesos_dep.head(10))

    # 4.2 Accesos por tecnología
    
    accesos_tec = df.groupby("tecnologia")["accesos"].sum().sort_values(ascending=False)
    print("\nAccesos totales por tecnología:")
    print(accesos_tec)

    # 4.3 Accesos por tipo de segmento
    
    accesos_seg = df.groupby("tipo_segmento")["accesos"].sum().sort_values(ascending=False)
    print("\nAccesos totales por tipo de segmento:")
    print(accesos_seg)

    # 4.4 Evolución de accesos por año
    
    accesos_anio = df.groupby("anio")["accesos"].sum().sort_index()
    print("\nAccesos totales por año:")
    print(accesos_anio)

    # -------------------------------------------------------------------------
    # 5. ANÁLISIS ADICIONAL (MÁS DETALLADO)
    # -------------------------------------------------------------------------
    
    print("\n=== ANÁLISIS ADICIONAL ===\n")

    # 5.1 Análisis por municipio (Top 10)
    
    top_municipios = (
        df.groupby("municipio")["accesos"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    print("\nTop 10 municipios por accesos totales:")
    print(top_municipios)

    # 5.2 Análisis del año más reciente
    anio_reciente = df["anio"].max()
    print(f"\nAño más reciente en el dataset: {anio_reciente}")

    df_reciente = df[df["anio"] == anio_reciente]

    accesos_dep_reciente = (
        df_reciente.groupby("departamento")["accesos"]
        .sum()
        .sort_values(ascending=False)
    )

    print(f"\nTop 10 departamentos por accesos en el año {anio_reciente}:")
    print(accesos_dep_reciente.head(10))

    # 5.3 Tecnologías principales y su evolución en el tiempo
    
    top3_tecnologias = accesos_tec.head(3).index.tolist()
    print("\nTop 3 tecnologías por accesos totales:")
    print(top3_tecnologias)

    df_top3 = df[df["tecnologia"].isin(top3_tecnologias)]

    # Tabla con accesos por año y tecnología (solo top 3)
    
    evol_top3 = (
        df_top3.groupby(["anio", "tecnologia"])["accesos"]
        .sum()
        .unstack("tecnologia")
        .sort_index()
    )

    print("\nEvolución anual de accesos para las 3 tecnologías principales:")
    print(evol_top3)

    # 5.4 Velocidad promedio de bajada por tecnología
    velocidad_media_tec = (
        df.groupby("tecnologia")["velocidad_bajada"]
        .mean()
        .sort_values(ascending=False)
    )

    print("\nVelocidad promedio de bajada por tecnología (Mbps):")
    print(velocidad_media_tec)

    # 5.5 Porcentaje de accesos por tipo de segmento
    total_accesos = accesos_seg.sum()
    porcentajes_segmento = (accesos_seg / total_accesos) * 100

    print("\nPorcentaje de accesos por tipo de segmento:")
    print(porcentajes_segmento.round(2))

    # -------------------------------------------------------------------------
    # 6. VISUALIZACIONES (GRÁFICOS)
    # -------------------------------------------------------------------------
    print("\n=== GENERANDO GRÁFICAS (se guardan en la carpeta 'graficos') ===\n")

    # 6.1 Top 10 departamentos (total histórico)
    top10_dep = accesos_dep.head(10)
    plt.figure()
    top10_dep.plot(kind="bar")
    plt.title("Top 10 departamentos por accesos de internet fijo (histórico)")
    plt.xlabel("Departamento")
    plt.ylabel("Número de accesos")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top10_departamentos_historico.png"))
    plt.close()

    # 6.2 Accesos por tecnología
    plt.figure()
    accesos_tec.plot(kind="bar")
    plt.title("Accesos de internet fijo por tecnología (histórico)")
    plt.xlabel("Tecnología")
    plt.ylabel("Número de accesos")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "accesos_por_tecnologia.png"))
    plt.close()

    # 6.3 Accesos por tipo de segmento
    plt.figure()
    accesos_seg.plot(kind="bar")
    plt.title("Accesos de internet fijo por tipo de segmento")
    plt.xlabel("Tipo de segmento")
    plt.ylabel("Número de accesos")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "accesos_por_tipo_segmento.png"))
    plt.close()

    # 6.4 Evolución de accesos por año
    plt.figure()
    accesos_anio.plot(kind="line", marker="o")
    plt.title("Evolución de accesos de internet fijo por año")
    plt.xlabel("Año")
    plt.ylabel("Número de accesos")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "evolucion_accesos_por_anio.png"))
    plt.close()

    # 6.5 Top 10 municipios
    plt.figure()
    top_municipios.plot(kind="bar")
    plt.title("Top 10 municipios por accesos de internet fijo")
    plt.xlabel("Municipio")
    plt.ylabel("Número de accesos")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top10_municipios.png"))
    plt.close()

    # 6.6 Top 10 departamentos en el año más reciente
    plt.figure()
    accesos_dep_reciente.head(10).plot(kind="bar")
    plt.title(f"Top 10 departamentos por accesos en {anio_reciente}")
    plt.xlabel("Departamento")
    plt.ylabel("Número de accesos")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"top10_departamentos_{anio_reciente}.png"))
    plt.close()

    # 6.7 Evolución anual de las 3 tecnologías principales
    plt.figure()
    evol_top3.plot(marker="o")
    plt.title("Evolución de accesos por año (top 3 tecnologías)")
    plt.xlabel("Año")
    plt.ylabel("Número de accesos")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "evolucion_top3_tecnologias.png"))
    plt.close()

    # 6.8 Velocidad promedio de bajada (top 8 tecnologías más rápidas)
    plt.figure()
    vel_top = velocidad_media_tec.head(8)
    vel_top.plot(kind="bar")
    plt.title("Velocidad promedio de bajada por tecnología (top 8)")
    plt.xlabel("Tecnología")
    plt.ylabel("Velocidad promedio (Mbps)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "velocidad_promedio_tecnologia_top8.png"))
    plt.close()

    # 6.9 Porcentaje de accesos por tipo de segmento
    plt.figure()
    porcentajes_segmento.plot(kind="bar")
    plt.title("Porcentaje de accesos por tipo de segmento")
    plt.xlabel("Tipo de segmento")
    plt.ylabel("Porcentaje de accesos (%)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "porcentaje_accesos_segmento.png"))
    plt.close()

    print("Gráficas guardadas en la carpeta:", OUTPUT_DIR)
    print("\n=== FIN DEL ANÁLISIS ===")
    print("Usa estas tablas y gráficas para tu informe (análisis descriptivo e interpretación).")


if __name__ == "__main__":
    main()
