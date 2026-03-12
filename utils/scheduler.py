import pandas as pd
import math

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

MAX_PARTIDOS_IDEAL = 20   # Ideal por franja
MAX_PARTIDOS_LIMITE = 25  # Máximo permitido


# ============================================================
# ASIGNAR HORARIOS A UNA RONDA COMPLETA
# ============================================================

def asignar_horarios(df_ronda, historial=None):
    """
    Asigna horarios automáticamente a los partidos de una ronda:
    - Respeta horarios oficiales
    - Máximo 20 partidos por franja (ideal)
    - Máximo 25 (límite)
    - Usa horarios extendidos solo si toca
    - Evita partidos seguidos para la misma pareja
    """

    df = df_ronda.copy()
    df["Horario"] = ""

    # Si hay historial (día anterior), lo usamos para descanso
    descanso = {}
    if historial is not None:
        for _, row in historial.iterrows():
            descanso[str(row["ganador"])] = row["Horario"]

    total_partidos = len(df)
    indice_partido = 0

    horarios_finales = []

    # Construir la lista TOTAL de horarios
    horarios_base = HORARIOS_PRINCIPALES.copy()

    # Si hay demasiados partidos → usamos extendidos
    if total_partidos > len(horarios_base) * MAX_PARTIDOS_IDEAL:
        horarios_base += HORARIOS_EXTENDIDOS

    # Distribuir partidos
    for hora in horarios_base:
        cupo = MAX_PARTIDOS_IDEAL

        # Si hay un exceso de partidos → podemos subir a 25
        if total_partidos > cupo * len(horarios_base):
            cupo = MAX_PARTIDOS_LIMITE

        for _ in range(cupo):
            if indice_partido >= total_partidos:
                break

            # Asignar este partido
            df.loc[indice_partido, "Horario"] = hora
            indice_partido += 1

        if indice_partido >= total_partidos:
            break

    # Si quedan partidos sin asignar → error
    if df["Horario"].eq("").any():
        raise ValueError("No fue posible asignar horarios suficientes. Aumenta horarios o reduce carga.")

    return df
``
