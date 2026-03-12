import os
import pandas as pd

RESULTS_FILE = "data/resultados.csv"


def registrar_ganador(grupo, fila, ganador):

    # Si el archivo no existe o está vacío
    if not os.path.exists(RESULTS_FILE) or os.stat(RESULTS_FILE).st_size == 0:

        resultados = pd.DataFrame(columns=[
            "grupo",
            "fila",
            "ganador"
        ])

    else:
        resultados = pd.read_csv(RESULTS_FILE)

    # agregar resultado
    nuevo = pd.DataFrame([{
        "grupo": grupo,
        "fila": fila,
        "ganador": ganador
    }])

    resultados = pd.concat([resultados, nuevo], ignore_index=True)

    resultados.to_csv(RESULTS_FILE, index=False)
