import pandas as pd

# Paleta corporativa pastel
PALETTE = {
    "ganador": "#C8F7C5",      # Verde pastel (ganó)
    "eliminado": "#F7C6C6",    # Rojo pastel elegante (eliminado)
    "pendiente": "#DDE7F2",    # Azul pastel suave (pendiente)
    "fondo": "#F5F6FA",        # Fondo corporativo blanco/gris pastel
}

def estado_color(row):
    """
    Aplica colores pastel dependiendo del estado del partido.
    Se llamará desde app.py usando styling.
    """
    color = PALETTE["pendiente"]

    if "Estado" in row:
        estado = str(row["Estado"]).lower()

        if "ganó" in estado:
            color = PALETTE["ganador"]
        elif "eliminado" in estado:
            color = PALETTE["eliminado"]

    return ["background-color: {}".format(color)] * len(row)
