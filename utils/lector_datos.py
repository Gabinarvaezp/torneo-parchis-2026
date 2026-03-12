import pandas as pd
from io import StringIO


def leer_tabla_pegada(texto):
    """
    Convierte una tabla pegada desde Excel o Sheets en DataFrame.
    Limpia espacios y filas vacías automáticamente.
    """

    if not texto or texto.strip() == "":
        return None

    try:

        df = pd.read_csv(
            StringIO(texto),
            sep="\t"
        )

        # limpiar columnas
        df.columns = df.columns.str.strip()

        # eliminar filas completamente vacías
        df = df.dropna(how="all")

        # resetear índice
        df = df.reset_index(drop=True)

        return df

    except Exception as e:
        raise ValueError(
            "No se pudo leer la tabla pegada. "
            "Asegúrate de copiarla directamente desde Excel."
        )
