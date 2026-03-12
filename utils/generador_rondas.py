import pandas as pd
import random

def generar_siguiente_ronda():
    resultados_path = "data/resultados.csv"
    df = pd.read_csv(resultados_path, header=None, names=["Ganador"])

    ganadores = df["Ganador"].tolist()
    random.shuffle(ganadores)

    nuevas_parejas = []

    for i in range(0, len(ganadores), 2):
        if i+1 < len(ganadores):
            nuevas_parejas.append({
                "Equipo A": ganadores[i],
                "Equipo B": ganadores[i+1]
            })

    pd.DataFrame(nuevas_parejas).to_csv("data/ronda_siguiente.csv", index=False)
