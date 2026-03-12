import pandas as pd
import os

DATA_PATH = "data"

os.makedirs(DATA_PATH, exist_ok=True)


# ============================================================
# CARGAR TABLA DE GRUPO
# ============================================================

def cargar_grupo(n_grupo):

    archivo = f"{DATA_PATH}/grupo_{n_grupo}.csv"

    if os.path.exists(archivo):

        try:
            return pd.read_csv(archivo)

        except:
            return None

    return None


# ============================================================
# GUARDAR TABLA DE GRUPO
# ============================================================

def guardar_grupo(n_grupo, df):

    archivo = f"{DATA_PATH}/grupo_{n_grupo}.csv"

    df.to_csv(archivo, index=False)


# ============================================================
# CARGAR TODOS LOS GRUPOS
# ============================================================

def cargar_todos():

    grupos = {}

    for g in range(1, 6):

        archivo = f"{DATA_PATH}/grupo_{g}.csv"

        if os.path.exists(archivo):

            try:
                grupos[g] = pd.read_csv(archivo)
            except:
                continue

    return grupos if grupos else None


# ============================================================
# GUARDAR RONDA
# ============================================================

def guardar_ronda(n_grupo, df_ronda, numero_ronda):

    archivo = f"{DATA_PATH}/grupo_{n_grupo}_ronda{numero_ronda}.csv"

    df_ronda.to_csv(archivo, index=False)
