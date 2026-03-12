import pandas as pd
import os

def cargar_todos_los_grupos():
    data_path = "data"
    archivos = [f for f in os.listdir(data_path) if f.endswith(".csv") and f.startswith("grupo")]
    df_list = []

    for archivo in archivos:
        df = pd.read_csv(os.path.join(data_path, archivo))
        df["Grupo"] = archivo.replace(".csv", "").replace("grupo", "")
        df_list.append(df)

    return pd.concat(df_list, ignore_index=True)
