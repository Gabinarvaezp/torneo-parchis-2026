import streamlit as st
import pandas as pd
import os
from io import StringIO

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Torneo Parchís 2026",
    page_icon="🎲",
    layout="wide"
)

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)

PALETTE = {
    "primary": "#8C7AE6",
    "secondary": "#74B9FF",
    "accent": "#81ECEC",
    "warning": "#FAB1A0",
    "danger": "#FF7675",
    "success": "#55EFC4",
    "neutral": "#F5F6FA",
}

# ============================================================
# ESTILOS PASTEL
# ============================================================

st.markdown(
    f"""
<style>
.main {{
    background-color: {PALETTE['neutral']};
}}

.stButton>button {{
    background-color: {PALETTE['primary']};
    color:white;
    border-radius:10px;
    padding:10px 30px;
    font-size:16px;
}}

h1,h2,h3,h4 {{
    color:{PALETTE['primary']};
}}

.block-container {{
    padding-top:2rem;
}}
</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# IMPORTS DE FUNCIONES
# ============================================================

from utils.loader import cargar_grupo, guardar_grupo, cargar_todos
from utils.ganadores import registrar_ganador, corregir_ganador
from utils.generador_rondas import generar_ronda_21, generar_ronda_28
from utils.scheduler import asignar_horarios
from utils.excel_exporter import exportar_excel_grupo, exportar_excel_torneo
from utils.estilos import estado_color
from utils.validator import validar_tabla

# ============================================================
# FUNCIÓN PARA PEGAR EXCEL
# ============================================================

def leer_excel_pegado(texto):

    try:

        df = pd.read_csv(
            StringIO(texto),
            sep="\t"
        )

        df.columns = df.columns.str.strip()

        return df

    except Exception:

        return None

# ============================================================
# PÁGINA DE GRUPO
# ============================================================

def pagina_grupo(n_grupo):

    st.header(f"👥 Grupo {n_grupo}")

    st.info(
        "Pega la tabla copiada directamente desde Excel del Sábado 14."
    )

    pasted = st.text_area(
        "📋 Pegar tabla aquí",
        height=250,
        placeholder="Copia las filas desde Excel y pégalas aquí..."
    )

    if pasted:

        df = leer_excel_pegado(pasted)

        if df is None:

            st.error("No se pudo leer la tabla pegada.")

        else:

            ok, msg = validar_tabla(df)

            if ok:

                st.success("Tabla detectada correctamente")

                st.dataframe(
                    df,
                    use_container_width=True
                )

                if st.button("💾 Guardar Tabla del Grupo"):

                    guardar_grupo(n_grupo, df)

                    st.success(
                        f"Grupo {n_grupo} guardado correctamente"
                    )

            else:

                st.warning(msg)

    # ========================================================
    # TABLA GUARDADA
    # ========================================================

    st.divider()

    st.subheader("📊 Tabla Guardada")

    df = cargar_grupo(n_grupo)

    if df is not None:

        st.dataframe(
            df.style.apply(estado_color, axis=1),
            use_container_width=True
        )

    else:

        st.info("Aún no hay tabla guardada para este grupo.")

    # ========================================================
    # BUSCADOR DE PARTIDOS
    # ========================================================

    st.divider()

    st.subheader("🔎 Buscar Partido")

    busqueda = st.text_input(
        "Buscar por ID, nombre o usuario"
    )

    if busqueda and df is not None:

        fil = df[
            df.apply(
                lambda r: busqueda.lower() in str(r).lower(),
                axis=1
            )
        ]

        if len(fil) == 0:

            st.warning("No se encontraron coincidencias.")

        else:

            st.dataframe(
                fil,
                use_container_width=True
            )

        # ====================================================
        # REGISTRAR GANADOR
        # ====================================================

        if len(fil) == 1:

            fila = fil.iloc[0]

            e1 = fila["ID Grupo 1"]
            e2 = fila["ID Grupo 2"]

            ganador = st.radio(
                "Selecciona el ganador",
                [e1, e2]
            )

            if st.button("🏆 Guardar Ganador"):

                registrar_ganador(
                    n_grupo,
                    fila,
                    ganador
                )

                st.success(
                    f"Ganador registrado: {ganador}"
                )

                st.rerun()

    # ========================================================
    # CORREGIR RESULTADO
    # ========================================================

    st.divider()

    st.subheader("🛠 Corregir Resultado")

    partido = st.text_input(
        "Partido exacto (ej: 851 vs 850)"
    )

    nuevo_g = st.text_input(
        "Nuevo ganador (ID exacto)"
    )

    if st.button("Corregir Resultado"):

        ok, msg = corregir_ganador(
            n_grupo,
            partido,
            nuevo_g
        )

        if ok:

            st.success(msg)

            st.rerun()

        else:

            st.error(msg)

    # ========================================================
    # EXPORTAR EXCEL
    # ========================================================

    st.divider()

    st.subheader("📥 Descargar Excel del Grupo")

    if st.button("Exportar Excel Grupo"):

        exportar_excel_grupo(n_grupo)

        st.success("Excel generado en /data")

# ============================================================
# RESUMEN DEL TORNEO
# ============================================================

def pagina_resumen():

    st.header("📊 Resumen del Torneo")

    grupos = cargar_todos()

    if not grupos:

        st.warning("Aún no hay datos cargados")

        return

    cols = st.columns(5)

    for i, (g, df) in enumerate(grupos.items()):

        total = len(df)

        gan = df["Estado"].str.contains("ganó", na=False).sum()

        elim = df["Estado"].str.contains("eliminado", na=False).sum()

        pend = df["Estado"].str.contains("pendiente", na=False).sum()

        with cols[i]:

            st.metric(
                f"Grupo {g}",
                total,
                f"{gan} ganadores"
            )

    st.divider()

    rows = []

    for g, df in grupos.items():

        rows.append([
            g,
            len(df),
            df["Estado"].str.contains("ganó", na=False).sum(),
            df["Estado"].str.contains("eliminado", na=False).sum()
        ])

    st.dataframe(
        pd.DataFrame(
            rows,
            columns=[
                "Grupo",
                "Total",
                "Ganadores",
                "Eliminados"
            ]
        ),
        use_container_width=True
    )

    st.divider()

    if st.button("📥 Exportar Excel Torneo Completo"):

        exportar_excel_torneo()

        st.success("Excel generado en /data")

# ============================================================
# AJUSTES
# ============================================================

def pagina_ajustes():

    st.header("⚙ Ajustes del Torneo")

    max_partidos = st.slider(
        "Máximo partidos por franja",
        10,
        25,
        20
    )

    descanso = st.slider(
        "Descanso mínimo (horas)",
        1,
        3,
        2
    )

    extendidos = st.checkbox(
        "Activar horarios extendidos",
        value=True
    )

    if st.button("Guardar Ajustes"):

        config = {
            "max_partidos": max_partidos,
            "descanso": descanso,
            "extendidos": extendidos
        }

        pd.DataFrame([config]).to_json(
            "data/config.json",
            orient="records"
        )

        st.success("Ajustes guardados")

# ============================================================
# MENÚ PRINCIPAL
# ============================================================

st.title("🎲 Torneo Parchís 2026")

menu = st.sidebar.radio(
    "Menú",
    [
        "Grupo 1",
        "Grupo 2",
        "Grupo 3",
        "Grupo 4",
        "Grupo 5",
        "Resumen del Torneo",
        "Ajustes"
    ]
)

if menu.startswith("Grupo"):

    n = int(menu.split(" ")[1])

    pagina_grupo(n)

elif menu == "Resumen del Torneo":

    pagina_resumen()

elif menu == "Ajustes":

    pagina_ajustes()
