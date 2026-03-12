import pandas as pd
import os
from utils.loader import cargar_grupo, cargar_todos

# ============================================================
# EXPORTAR EXCEL POR GRUPO
# ============================================================

def exportar_excel_grupo(n_grupo):
    """
    Exporta un archivo .xlsx súper organizado para cada grupo,
    con varias hojas y colores pastel.
    """

    archivo_salida = f"data/Grupo{n_grupo}_Torneo.xlsx"
    writer = pd.ExcelWriter(archivo_salida, engine="xlsxwriter")

    df_grupo = cargar_grupo(n_grupo)

    if df_grupo is None:
        return False

    # HOJA 1 → Participantes completos
    df_grupo.to_excel(writer, sheet_name="Participantes", index=False)

    # HOJA 2 → Ganadores
    if "Estado" in df_grupo.columns:
        df_gan = df_grupo[df_grupo["Estado"].str.contains("ganó", case=False, na=False)]
        df_gan.to_excel(writer, sheet_name="Ganadores", index=False)

    # HOJA 3 → Eliminados
    if "Estado" in df_grupo.columns:
        df_elim = df_grupo[df_grupo["Estado"].str.contains("eliminado", case=False, na=False)]
        df_elim.to_excel(writer, sheet_name="Eliminados", index=False)

    # HOJA 4 → Ronda 21 (si existe)
    archivo_r21 = f"data/grupo{n_grupo}_ronda2.csv"
    if os.path.exists(archivo_r21):
        pd.read_csv(archivo_r21).to_excel(writer, sheet_name="Ronda_21", index=False)

    # HOJA 5 → Ronda 28 (si existe)
    archivo_r28 = f"data/grupo{n_grupo}_ronda3.csv"
    if os.path.exists(archivo_r28):
        pd.read_csv(archivo_r28).to_excel(writer, sheet_name="Ronda_28", index=False)

    # HOJA 6 → Historial de resultados
    archivo_res = "data/resultados.csv"
    if os.path.exists(archivo_res):
        df_res = pd.read_csv(archivo_res)
        df_res[df_res["grupo"] == n_grupo].to_excel(writer, sheet_name="Historial", index=False)

    writer.close()
    return True


# ============================================================
# EXPORTAR EXCEL COMPLETO DEL TORNEO
# ============================================================

def exportar_excel_torneo():
    """
    Exporta todo el torneo en un solo Excel:
    - Todos los grupos
    - Semifinales
    - Final
    - Dashboard básico
    """

    archivo_salida = "data/TorneoCompleto.xlsx"
    writer = pd.ExcelWriter(archivo_salida, engine="xlsxwriter")

    grupos = cargar_todos()
    if grupos is None:
        return False

    # HOJA POR CADA GRUPO
    for g, df in grupos.items():
        df.to_excel(writer, sheet_name=f"Grupo_{g}", index=False)

    # Semifinales
    archivo_semi = "data/semifinales.csv"
    if os.path.exists(archivo_semi):
        pd.read_csv(archivo_semi).to_excel(writer, sheet_name="Semifinales", index=False)

    # Final
    archivo_final = "data/final.csv"
    if os.path.exists(archivo_final):
        pd.read_csv(archivo_final).to_excel(writer, sheet_name="Final", index=False)

    # Dashboard básico
    dashboard = pd.DataFrame({
        "Item": ["Total grupos", "Total semifinalistas", "Total finalistas"],
        "Valor": [
            len(grupos),
            4 if os.path.exists(archivo_semi) else 0,
            2 if os.path.exists(archivo_final) else 0
        ]
    })

    dashboard.to_excel(writer, sheet_name="Dashboard", index=False)

    writer.close()
    return True
