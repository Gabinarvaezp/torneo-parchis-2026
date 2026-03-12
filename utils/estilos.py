import pandas as pd

# Paleta corporativa pastel
PALETTE = {
    "ganador": "#C8F7C5",      # Verde pastel
    "eliminado": "#F7C6C6",    # Rojo pastel
    "pendiente": "#DDE7F2",    # Azul pastel
    "fondo": "#F5F6FA",
}

def estado_color(row):
    """
    Colorea cada fila según el estado del partido.
    """

    estado = str(row.get("Estado", "pendiente")).lower()

    if estado == "ganó":
        color = PALETTE["ganador"]

    elif estado == "eliminado":
        color = PALETTE["eliminado"]

    else:
        color = PALETTE["pendiente"]

    return [f"background-color: {color}"] * len(row)
