import pandas as pd
import random
import os
from utils.loader import cargar_grupo, guardar_ronda
from utils.scheduler import asignar_horarios


# ============================================================
# GENERAR RONDA DEL SÁBADO 21
# ============================================================

def generar_ronda_21(n_grupo):

    df = cargar_grupo(n_grupo)

    if df is None:
        return None, "No hay datos del grupo."

    if "Estado" not in df.columns:
        return None, "Falta columna Estado."

    # tomar solo partidos ganados
    ganados = df[df["Estado"].str.contains("ganó", case=False, na=False)]

    if len(ganados) == 0:
        return None, "No hay ganadores todavía."

    ids_ganadores = []

    for _, row in ganados.iterrows():

        if row["Estado"].lower() == "ganó":
            ids_ganadores.append(str(row["ID Grupo 1"]))

        else:
            ids_ganadores.append(str(row["ID Grupo 2"]))

    random.shuffle(ids_ganadores)

    partidos = []

    for i in range(0, len(ids_ganadores), 2):

        if i + 1 < len(ids_ganadores):

            partidos.append({
                "ID Grupo 1": ids_ganadores[i],
                "VS": "VS",
                "ID Grupo 2": ids_ganadores[i+1],
                "Estado": "pendiente"
            })

    df_ronda = pd.DataFrame(partidos)

    if df_ronda.empty:
        return None, "No se pudieron generar partidos."

    df_ronda = asignar_horarios(df_ronda)

    guardar_ronda(n_grupo, df_ronda, numero_ronda=2)

    return df_ronda, "Ronda del 21 generada correctamente."


# ============================================================
# GENERAR SEMIFINALES (SÁBADO 28)
# ============================================================

def generar_ronda_28():

    ganadores = []

    for g in range(1, 6):

        archivo = f"data/grupo{g}_ronda2.csv"

        if not os.path.exists(archivo):
            continue

        df = pd.read_csv(archivo)

        if "Estado" not in df.columns:
            continue

        partidos_ganados = df[df["Estado"].str.contains("ganó", case=False, na=False)]

        for _, row in partidos_ganados.iterrows():

            if row["Estado"].lower() == "ganó":
                ganadores.append(str(row["ID Grupo 1"]))
            else:
                ganadores.append(str(row["ID Grupo 2"]))

    if len(ganadores) < 4:
        return None, "Aún no hay suficientes ganadores para semifinal."

    random.shuffle(ganadores)

    semifinales = []

    for i in range(0, len(ganadores), 2):

        if i + 1 < len(ganadores):

            semifinales.append({
                "ID Grupo 1": ganadores[i],
                "VS": "VS",
                "ID Grupo 2": ganadores[i+1],
                "Estado": "pendiente"
            })

    df_semi = pd.DataFrame(semifinales)

    df_semi = asignar_horarios(df_semi)

    df_semi.to_csv("data/semifinales.csv", index=False)

    # preparar archivo final
    final = pd.DataFrame(columns=[
        "ID Grupo 1",
        "VS",
        "ID Grupo 2",
        "Estado"
    ])

    final.to_csv("data/final.csv", index=False)

    return df_semi, "Semifinales generadas correctamente."
