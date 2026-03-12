import pandas as pd
import os
from utils.loader import cargar_grupo, cargar_todos


# ============================================================
# EXPORTAR EXCEL POR GRUPO
# ============================================================

def exportar_excel_grupo(n_grupo):

    archivo_salida = f"data/Grupo{n_grupo}_Torneo.xlsx"

    writer = pd.ExcelWriter(
        archivo_salida,
        engine="xlsxwriter"
    )

    workbook = writer.book

    formato_header = workbook.add_format({
        "bold": True,
        "bg_color": "#DDE7F2",
        "border": 1
    })

    df_grupo = cargar_grupo(n_grupo)

    if df_grupo is None:
        return False

    # HOJA 1 → Participantes
    df_grupo.to_excel(writer, sheet_name="Participantes", index=False)

    worksheet = writer.sheets["Participantes"]

    for col_num, value in enumerate(df_grupo.columns.values):
        worksheet.write(0, col_num, value, formato_header)


    # HOJA 2 → Ganadores
    if "Estado" in df_grupo.columns:

        df_gan = df_grupo[
            df_grupo["Estado"]
            .astype(str)
            .str.contains("ganó", case=False, na=False)
        ]

        df_gan.to_excel(
            writer,
            sheet_name="Ganadores",
            index=False
        )


    # HOJA 3 → Eliminados
    if "Estado" in df_grupo.columns:

        df_elim = df_grupo[
            df_grupo["Estado"]
            .astype(str)
            .str.contains("eliminado", case=False, na=False)
        ]

        df_elim.to_excel(
            writer,
            sheet_name="Eliminados",
            index=False
        )


    # HOJA 4 → Ronda 21
    archivo_r21 = f"data/grupo{n_grupo}_ronda2.csv"

    if os.path.exists(archivo_r21):

        pd.read_csv(archivo_r21).to_excel(
            writer,
            sheet_name="Ronda_21",
            index=False
        )


    # HOJA 5 → Ronda 28
    archivo_r28 = f"data/grupo{n_grupo}_ronda3.csv"

    if os.path.exists(archivo_r28):

        pd.read_csv(archivo_r28).to_excel(
            writer,
            sheet_name="Ronda_28",
            index=False
        )


    # HOJA 6 → Historial
    archivo_res = "data/resultados.csv"

    if os.path.exists(archivo_res):

        df_res = pd.read_csv(archivo_res)

        if "grupo" in df_res.columns:

            df_res[
                df_res["grupo"] == n_grupo
            ].to_excel(
                writer,
                sheet_name="Historial",
                index=False
            )

    writer.close()

    return True


# ============================================================
# EXPORTAR TODO EL TORNEO
# ============================================================

def exportar_excel_torneo():

    archivo_salida = "data/TorneoCompleto.xlsx"

    writer = pd.ExcelWriter(
        archivo_salida,
        engine="xlsxwriter"
    )

    grupos = cargar_todos()

    if grupos is None:
        return False


    # HOJA POR GRUPO
    for g, df in grupos.items():

        df.to_excel(
            writer,
            sheet_name=f"Grupo_{g}",
            index=False
        )


    # SEMIFINALES
    archivo_semi = "data/semifinales.csv"

    if os.path.exists(archivo_semi):

        pd.read_csv(archivo_semi).to_excel(
            writer,
            sheet_name="Semifinales",
            index=False
        )


    # FINAL
    archivo_final = "data/final.csv"

    if os.path.exists(archivo_final):

        pd.read_csv(archivo_final).to_excel(
            writer,
            sheet_name="Final",
            index=False
        )


    # DASHBOARD
    dashboard = pd.DataFrame({

        "Item": [
            "Total grupos",
            "Total semifinalistas",
            "Total finalistas"
        ],

        "Valor": [
            len(grupos),
            4 if os.path.exists(archivo_semi) else 0,
            2 if os.path.exists(archivo_final) else 0
        ]
    })

    dashboard.to_excel(
        writer,
        sheet_name="Dashboard",
        index=False
    )

    writer.close()

    return True
