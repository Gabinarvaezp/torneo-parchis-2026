import pandas as pd
import os

RESULTS_FILE = "data/resultados.csv"


# ============================================================
# ASEGURAR ARCHIVO DE RESULTADOS
# ============================================================
def _asegurar_archivo():
    """Crea el archivo de resultados si no existe."""
    if not os.path.exists(RESULTS_FILE):
        df = pd.DataFrame(columns=["grupo", "partido", "ganador", "perdedor"])
        df.to_csv(RESULTS_FILE, index=False)


# ============================================================
# REGISTRAR GANADOR (LLAMADO DESDE app.py)
# ============================================================
def registrar_ganador(num_grupo, fila, ganador_id):
    """
    Guarda el resultado de un partido (ganador y perdedor).
    fila = fila del DataFrame original del grupo.
    ganador_id = ID del equipo ganador.
    """
    _asegurar_archivo()

    resultados = pd.read_csv(RESULTS_FILE)

    # Determinar perdedor
    equipo1 = str(fila["ID Grupo 1"])
    equipo2 = str(fila["ID Grupo 2"])
    ganador_id = str(ganador_id)

    perdedor = equipo2 if ganador_id == equipo1 else equipo1

    nuevo = {
        "grupo": num_grupo,
        "partido": f"{equipo1} vs {equipo2}",
        "ganador": ganador_id,
        "perdedor": perdedor
    }

    # Evitar duplicados
    existe = resultados[
        (resultados["partido"] == nuevo["partido"]) &
        (resultados["grupo"] == num_grupo)
    ]

    if not existe.empty:
        # Si ya existía, reemplazarlo (actualizar)
        resultados = resultados[
            ~((resultados["partido"] == nuevo["partido"]) &
              (resultados["grupo"] == num_grupo))
        ]

    # Guardar fila nueva
    resultados = pd.concat(
        [resultados, pd.DataFrame([nuevo])],
        ignore_index=True
    )

    resultados.to_csv(RESULTS_FILE, index=False)
    return ganador_id, perdedor


# ============================================================
# CORREGIR GANADOR (MUY IMPORTANTE)
# ============================================================
def corregir_ganador(num_grupo, partido_txt, nuevo_ganador):
    """
    Corrige un ganador si hubo error.
    partido_txt = "851 vs 850"
    nuevo_ganador = "851" (por ejemplo)
    """
    _asegurar_archivo()
    resultados = pd.read_csv(RESULTS_FILE)

    # Buscar registro
    filtro = (resultados["partido"] == partido_txt) & (resultados["grupo"] == num_grupo)
    fila = resultados[filtro]

    if fila.empty:
        return False, "No encontramos ese partido registrado."

    equipos = partido_txt.split(" vs ")
    equipo1, equipo2 = equipos[0].strip(), equipos[1].strip()

    nuevo_ganador = str(nuevo_ganador)

    if nuevo_ganador not in [equipo1, equipo2]:
        return False, "El ganador no coincide con ninguno de los equipos del partido."

    # Nuevo perdedor
    nuevo_perdedor = equipo1 if nuevo_ganador == equipo2 else equipo2

    # Actualizar registro
    resultados.loc[filtro, "ganador"] = nuevo_ganador
    resultados.loc[filtro, "perdedor"] = nuevo_perdedor

    resultados.to_csv(RESULTS_FILE, index=False)

    return True, f"Ganador corregido correctamente → {nuevo_ganador}"
