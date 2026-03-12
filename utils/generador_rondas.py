
import pandas as pd

def generar_ronda(ganadores):
    parejas = []
    for i in range(0, len(ganadores), 2):
        if i + 1 < len(ganadores):
            parejas.append([ganadores[i], ganadores[i + 1]])
    return pd.DataFrame(parejas, columns=["Equipo A", "Equipo B"])
