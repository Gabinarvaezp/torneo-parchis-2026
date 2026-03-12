import pandas as pd

def leer_tabla_pegada(texto):
    return pd.read_csv(pd.io.common.StringIO(texto), sep="\t")
