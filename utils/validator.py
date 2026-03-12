import pandas as pd

# Columnas mínimas que debe tener el Excel
COLUMNAS_REQUERIDAS = [
    "Horario",
    "Grupo",
    "ID Grupo 1",
    "VS",
    "ID Grupo 2",
    "User 1 G1",
    "User 2 G1",
    "User 1 G2",
    "User 2 G2"
]


def normalizar_vs(valor):

    if pd.isna(valor):
        return "VS"

    v = str(valor).strip().lower()

    if v.startswith("v"):
        return "VS"

    return "VS"


def validar_tabla(df):

    # limpiar nombres de columnas
    df.columns = df.columns.str.strip()

    # verificar columnas mínimas
    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]

    if faltantes:
        return False, f"Faltan columnas: {faltantes}"

    # normalizar VS
    df["VS"] = df["VS"].apply(normalizar_vs)

    return True, "Tabla válida"
