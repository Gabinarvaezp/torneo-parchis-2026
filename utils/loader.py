import pandas as pd
import os

DATA_PATH = "data"

# ============================================================
# CARGAR TABLA DE GRUPO
# ============================================================

def cargar_grupo(n_grupo):
    """
    Carga la tabla de un grupo específico.
    Devuelve un DataFrame o None si no existe.
    """
    archivo = f"{DATA_PATH}/grupo{n_grupo}.csv"
    if os.path.exists(archivo):
        try:
            df = pd.read_csv(archivo)
            return df
        except:
            return None
    return None


# ============================================================
# GUARDAR TABLA DE GRUPO
# ============================================================

def guardar_grupo(n_grupo, df):
    """
    Guarda la tabla del grupo (lo que se pegó desde Excel).
    """
    archivo = f"{DATA_PATH}/grupo{n_grupo}.csv"

    # Crear carpeta data si no existe
    os.makedirs(DATA_PATH, exist_ok=True)

    df.to_csv(archivo, index=False)


# ============================================================
# CARGAR TODOS LOS GRUPOS
# ============================================================

def cargar_todos():
    """
    Devuelve un diccionario con todos los grupos cargados:
    {
        1: df1,
        2: df2,
        ...
    }
    """
    grupos = {}
    for g in range(1, 6):
        archivo = f"{DATA_PATH}/grupo{g}.csv"
        if os.path.exists(archivo):
            grupos[g] = pd.read_csv(archivo)
    return grupos if grupos else None


# ============================================================
# GUARDAR UNA RONDA NUEVA DEL GRUPO
# ============================================================

def guardar_ronda(n_grupo, df_ronda, numero_ronda):
    """
    Guarda una ronda generada automáticamente.
    Ej: data/grupo1_ronda2.csv
    """
    archivo = f"{DATA_PATH}/grupo{n_grupo}_ronda{numero_ronda}.csv"
    df_ronda.to_csv(archivo, index=False)
