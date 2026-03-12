import pandas as pd
import os

RESULTS_FILE = "data/resultados.csv"

# ------------------------
# Guardar resultado
# ------------------------
def register_winner(row, ganador_id):
    """
    row = una fila del DataFrame del grupo
    ganador_id = ID del ganador (equipo 1 o equipo 2)
    """

    # Crear archivo resultados si no existe
    if not os.path.exists(RESULTS_FILE):
        pd.DataFrame(columns=["grupo", "partido", "ganador", "perdedor"]).to_csv(RESULTS_FILE, index=False)

    resultados = pd.read_csv(RESULTS_FILE)

    # Determinar perdedor
    if ganador_id == row["ID Grupo 1"]:
        perdedor = row["ID Grupo 2"]
    else:
        perdedor = row["ID Grupo 1"]

    nuevo = {
        "grupo": row["Grupo"],
        "partido": f"{row['ID Grupo 1']} vs {row['ID Grupo 2']}",
        "ganador": ganador_id,
        "perdedor": perdedor
    }

    # Guardar
    resultados = pd.concat([resultados, pd.DataFrame([nuevo])], ignore_index=True)
    resultados.to_csv(RESULTS_FILE, index=False)

    return ganador_id, perdedor


# ------------------------
# CORREGIR GANADOR
# ------------------------
def correct_winner(grupo_num, partido, nuevo_ganador):
    """
    partido → string tipo '123 vs 456'
    nuevo_ganador → nuevo ID ganador
    """

    if not os.path.exists(RESULTS_FILE):
        return False, "No hay resultados guardados aún."

    resultados = pd.read_csv(RESULTS_FILE)

    # Buscar el partido
    fila = resultados[resultados["partido"] == partido]

    if fila.empty:
        return False, "No encontramos ese partido."

    viejo_ganador = fila["ganador"].values[0]

    # Determinar nuevo perdedor
    ids = partido.split(" vs ")
    equipo1, equipo2 = ids[0], ids[1]
    nuevo_perdedor = equipo1 if nuevo_ganador == equipo2 else equipo2

    # Actualizar fila
    resultados.loc[resultados["partido"] == partido, "ganador"] = nuevo_ganador
    resultados.loc[resultados["partido"] == partido, "perdedor"] = nuevo_perdedor

    resultados.to_csv(RESULTS_FILE, index=False)

    return True, f"Ganador corregido: antes {viejo_ganador}, ahora {nuevo_ganador}"
