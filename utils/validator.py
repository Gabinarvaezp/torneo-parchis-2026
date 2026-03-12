import pandas as pd


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

    v = str(valor).strip().upper()

    if v in ["VS", "V", "VS.", "VERSUS"]:
        return "VS"

    return "VS"


def validar_tabla(df):

    df = df.copy()

    # limpiar nombres de columnas
    df.columns = df.columns.str.strip()

    # verificar columnas mínimas
    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]

    if faltantes:
        return False, f"Faltan columnas: {faltantes}", None

    # limpiar VS
    df["VS"] = df["VS"].apply(normalizar_vs)

    # limpiar espacios en usuarios
    columnas_users = [
        "User 1 G1",
        "User 2 G1",
        "User 1 G2",
        "User 2 G2"
    ]

    for col in columnas_users:
        df[col] = df[col].astype(str).str.strip()

    return True, "Tabla válida", df
