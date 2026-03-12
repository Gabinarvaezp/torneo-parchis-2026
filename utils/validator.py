import pandas as pd

# ============================================================
# COLUMNAS REQUERIDAS EXACTAS DE LA TABLA
# ============================================================

COLUMNAS_REQUERIDAS = [
    "Horario",
    "Grupo",
    "ID Grupo 1",
    "VS",
    "ID Grupo 2",
    "Nombre Jugador 1 (Creador Tablero)",
    "User 1 G1",
    "User 2 G1",
    "Nombre Jugador Grupo 2",
    "User 1 G2",
    "User 2 G2"
]

# ============================================================
# VALIDACIÓN DE TABLA PEGADA DESDE EXCEL
# ============================================================

def validar_tabla(df):
    """
    Valida la tabla pegada por Excel.
    Revisa:
    - que tenga todas las columnas
    - que no falten columnas
    - que la estructura sea correcta
    - que haya al menos 1 partido
    """

    # Convertir columnas a string limpio
    df.columns = [str(c).strip() for c in df.columns]

    # 1. Validar columnas necesarias
    for col in COLUMNAS_REQUERIDAS:
        if col not in df.columns:
            return False, f"❌ Falta la columna obligatoria: {col}"

    # 2. Validar que haya filas
    if df.empty:
        return False, "❌ La tabla está vacía."

    # 3. Validar que los IDs sean numéricos o texto válido
    try:
        df["ID Grupo 1"] = df["ID Grupo 1"].astype(str).str.strip()
        df["ID Grupo 2"] = df["ID Grupo 2"].astype(str).str.strip()
    except:
        return False, "❌ Los IDs no parecen válidos."

    # 4. Validar columna VS
    if not df["VS"].isin(["VS", "vs", "Vs", "v.s.", "V S"]).all():
        return False, "❌ La columna VS tiene valores inválidos."

    # 5. Validación de datos repetidos
    duplicados = df.duplicated(subset=["ID Grupo 1", "ID Grupo 2"])
    if duplicados.any():
        return False, "❌ Hay partidos duplicados."

    # 6. Validar que haya parejas completas
    for _, row in df.iterrows():
        if pd.isna(row["ID Grupo 1"]) or pd.isna(row["ID Grupo 2"]):
            return False, "❌ Hay filas sin ambas parejas completas."

    # 7. Validar usuarios vacíos
    user_cols = ["User 1 G1", "User 2 G1", "User 1 G2", "User 2 G2"]
    for col in user_cols:
        if df[col].isna().any():
            return False, f"❌ Falta información en la columna: {col}"

    return True, "Tabla válida."
