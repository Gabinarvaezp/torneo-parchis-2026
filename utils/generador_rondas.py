import pandas as pd
import random
from utils.loader import cargar_grupo, guardar_ronda
from utils.scheduler import asignar_horarios

# ============================================================
# GENERAR RONDA DEL SÁBADO 21 (solo ganadores del grupo)
# ============================================================

def generar_ronda_21(n_grupo):
    """
    Toma los ganadores del primer sábado y genera los partidos
    aleatoriamente dentro del mismo grupo.
    """

    df = cargar_grupo(n_grupo)
    if df is None:
        return None, "No hay datos del grupo."

    # Filtrar ganadores
    if "Estado" not in df.columns:
        return None, "Falta columna Estado."

    ganadores = df[df["Estado"].str.contains("ganó", case=False, na=False)]

    if len(ganadores) < 2:
        return None, "No hay suficientes ganadores para ronda 21."

    # IDs de ganadores
    ids = []
    for _, row in ganadores.iterrows():
        ids.append(str(row["ID Grupo 1"]))
        ids.append(str(row["ID Grupo 2"]))

    # Algunos partidos tendrán solo uno (depende quien ganó)
    ids = list(set(ids))

    random.shuffle(ids)

    # Crear nuevos partidos
    partidos = []
    for i in range(0, len(ids), 2):
        if i + 1 < len(ids):
            partidos.append({
                "ID Grupo 1": ids[i],
                "VS": "VS",
                "ID Grupo 2": ids[i+1],
                "Estado": "Pendiente"
            })

    df_ronda = pd.DataFrame(partidos)

    # Asignar horarios inteligentes
    df_horarios = asignar_horarios(df_ronda)

    # Guardar ronda en data/grupoX_ronda2.csv
    guardar_ronda(n_grupo, df_horarios, numero_ronda=2)

    return df_horarios, "Ronda 21 generada correctamente."


# ============================================================
# GENERAR SEMIFINAL Y FINAL (SÁBADO 28)
# ============================================================

def generar_ronda_28():
    """
    Toma el ganador de cada grupo y arma semifinal + final.
    """

    ganadores_por_grupo = []

    # Cargar ronda 21
    for g in range(1, 6):
        archivo = f"data/grupo{g}_ronda2.csv"
        try:
            df = pd.read_csv(archivo)
            ganador = df[df["Estado"].str.contains("ganó", na=False)]
            if not ganador.empty:
                # Tomar el ID del ganador
                fila = ganador.iloc[0]
                if str(fila["Estado"]).lower().startswith("ganó"):
                    ganadores_por_grupo.append(str(fila["ID Grupo 1"]))
        except:
            continue

    if len(ganadores_por_grupo) < 2:
        return None, "No hay suficientes ganadores para semifinal."

    random.shuffle(ganadores_por_grupo)

    # Crear semifinales
    semifinales = []
    for i in range(0, len(ganadores_por_grupo), 2):
        if i + 1 < len(ganadores_por_grupo):
            semifinales.append({
                "ID Grupo 1": ganadores_por_grupo[i],
                "VS": "VS",
                "ID Grupo 2": ganadores_por_grupo[i+1],
                "Estado": "Pendiente"
            })

    df_semi = pd.DataFrame(semifinales)
    df_semi = asignar_horarios(df_semi)

    df_semi.to_csv("data/semifinales.csv", index=False)

    # Crear final (se generará cuando ganen las semifinales)
    final = pd.DataFrame(columns=["ID Grupo 1", "VS", "ID Grupo 2", "Estado"])
    final.to_csv("data/final.csv", index=False)

    return df_semi, "Semifinales generadas correctamente."
