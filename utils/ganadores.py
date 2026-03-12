import os
import pandas as pd

RESULTS_FILE = "data/resultados.csv"


def registrar_ganador(grupo, fila, ganador):

    # crear archivo si no existe
    if not os.path.exists(RESULTS_FILE):
        df = pd.DataFrame(columns=["grupo", "partido", "ganador"])
        df.to_csv(RESULTS_FILE, index=False)

    # cargar resultados
    try:
        resultados = pd.read_csv(RESULTS_FILE)
    except:
        resultados = pd.DataFrame(columns=["grupo", "partido", "ganador"])

    partido = f"{fila['ID Grupo 1']} vs {fila['ID Grupo 2']}"

    nuevo = pd.DataFrame([{
        "grupo": grupo,
        "partido": partido,
        "ganador": ganador
    }])

    resultados = pd.concat([resultados, nuevo], ignore_index=True)

    resultados.to_csv(RESULTS_FILE, index=False)


def corregir_ganador(grupo, partido, nuevo_ganador):

    if not os.path.exists(RESULTS_FILE):
        return False, "No hay resultados registrados aún."

    resultados = pd.read_csv(RESULTS_FILE)

    mask = (resultados["grupo"] == grupo) & (resultados["partido"] == partido)

    if mask.sum() == 0:
        return False, "Partido no encontrado."

    resultados.loc[mask, "ganador"] = nuevo_ganador

    resultados.to_csv(RESULTS_FILE, index=False)

    return True, "Resultado corregido correctamente."
