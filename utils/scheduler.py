import pandas as pd


# ============================================================
# HORARIOS OFICIALES DEL TORNEO
# ============================================================

HORARIOS_PRINCIPALES = [
    "8:00 a.m.", "8:30 a.m.", "9:00 a.m.", "9:30 a.m.",
    "12:00 p.m.", "1:00 p.m.", "1:30 p.m."
]

HORARIOS_EXTENDIDOS = [
    "10:30 a.m.", "11:30 a.m.", "2:00 p.m."
]

MAX_PARTIDOS_IDEAL = 20
MAX_PARTIDOS_LIMITE = 25


# ============================================================
# ASIGNAR HORARIOS A UNA RONDA
# ============================================================

def asignar_horarios(df_ronda, historial=None):

    df = df_ronda.copy()

    # reiniciar índice (muy importante)
    df = df.reset_index(drop=True)

    if "Horario" not in df.columns:
        df["Horario"] = ""

    total_partidos = len(df)
    indice_partido = 0

    horarios_base = HORARIOS_PRINCIPALES.copy()

    # activar horarios extendidos si se necesita
    if total_partidos > len(horarios_base) * MAX_PARTIDOS_IDEAL:
        horarios_base += HORARIOS_EXTENDIDOS

    for hora in horarios_base:

        cupo = MAX_PARTIDOS_IDEAL

        # si hay demasiados partidos usar límite
        if total_partidos > cupo * len(horarios_base):
            cupo = MAX_PARTIDOS_LIMITE

        for _ in range(cupo):

            if indice_partido >= total_partidos:
                break

            df.at[indice_partido, "Horario"] = hora
            indice_partido += 1

        if indice_partido >= total_partidos:
            break

    if df["Horario"].eq("").any():

        raise ValueError(
            "No fue posible asignar horarios suficientes. "
            "Aumenta horarios o reduce carga."
        )

    return df
