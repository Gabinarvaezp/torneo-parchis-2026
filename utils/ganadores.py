import os
import pandas as pd

DATA_PATH = "data"
RESULTS_FILE = os.path.join(DATA_PATH, "resultados.csv")


# ============================================================
# REGISTRAR GANADOR
# ============================================================

def registrar_ganador(grupo, fila, ganador):

    grupo_file = os.path.join(DATA_PATH, f"grupo_{grupo}.csv")

    if not os.path.exists(grupo_file):
        return False, "No existe el archivo del grupo."

    df = pd.read_csv(grupo_file)

    # asegurar columna Estado
    if "Estado" not in df.columns:
        df["Estado"] = "pendiente"

    id1 = fila["ID Grupo 1"]
    id2 = fila["ID Grupo 2"]

    partido = f"{id1} vs {id2}"

    # actualizar estado
    if ganador == id1:

        df.loc[
            (df["ID Grupo 1"] == id1) &
            (df["ID Grupo 2"] == id2),
            "Estado"
        ] = "ganó"

    else:

        df.loc[
            (df["ID Grupo 1"] == id1) &
            (df["ID Grupo 2"] == id2),
            "Estado"
        ] = "eliminado"

    df.to_csv(grupo_file, index=False)

    # ============================================================
    # HISTORIAL RESULTADOS
    # ============================================================

    if not os.path.exists(RESULTS_FILE):

        resultados = pd.DataFrame(
            columns=["grupo", "partido", "ganador"]
        )

    else:

        try:
            resultados = pd.read_csv(RESULTS_FILE)
        except pd.errors.EmptyDataError:
            resultados = pd.DataFrame(
                columns=["grupo", "partido", "ganador"]
            )

    nuevo = pd.DataFrame([{
        "grupo": grupo,
        "partido": partido,
        "ganador": ganador
    }])

    resultados = pd.concat(
        [resultados, nuevo],
        ignore_index=True
    )

    resultados.to_csv(RESULTS_FILE, index=False)

    return True, "Ganador registrado correctamente."


# ============================================================
# CORREGIR RESULTADO
# ============================================================

def corregir_ganador(grupo, partido, nuevo_ganador):

    if not os.path.exists(RESULTS_FILE):
        return False, "No hay resultados aún."

    try:
        resultados = pd.read_csv(RESULTS_FILE)

    except pd.errors.EmptyDataError:
        return False, "El archivo de resultados está vacío."

    mask = (
        (resultados["grupo"] == grupo) &
        (resultados["partido"] == partido)
    )

    if mask.sum() == 0:
        return False, "Partido no encontrado."

    resultados.loc[mask, "ganador"] = nuevo_ganador

    resultados.to_csv(RESULTS_FILE, index=False)

    return True, "Resultado corregido correctamente."
