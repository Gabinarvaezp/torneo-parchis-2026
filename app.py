import streamlit as st
import pandas as pd
import os
from io import StringIO

st.set_page_config(
    page_title="Torneo Parchís 2026",
    page_icon="🎲",
    layout="wide"
)

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)

# ============================================================
# PALETA PROFESIONAL
# ============================================================

PALETTE = {
    "primary": "#6C5CE7",
    "secondary": "#00B894",
    "danger": "#D63031",
    "warning": "#E17055",
    "light": "#F5F6FA"
}

# ============================================================
# ESTILOS MODERNOS
# ============================================================

st.markdown(
    f"""
<style>

.main {{
background-color:{PALETTE['light']};
}}

h1,h2,h3 {{
color:{PALETTE['primary']};
}}

.stButton>button {{
border-radius:12px;
background:{PALETTE['primary']};
color:white;
padding:8px 25px;
font-weight:600;
}}

.metric-card {{
background:white;
padding:15px;
border-radius:12px;
box-shadow:0 2px 8px rgba(0,0,0,0.08);
text-align:center;
}}

</style>
""",
unsafe_allow_html=True
)

# ============================================================
# IMPORTS
# ============================================================

from utils.loader import cargar_grupo, guardar_grupo, cargar_todos
from utils.ganadores import registrar_ganador, corregir_ganador
from utils.estilos import estado_color
from utils.validator import validar_tabla
from utils.excel_exporter import exportar_excel_grupo, exportar_excel_torneo

# ============================================================
# LEER TABLA PEGADA
# ============================================================

def leer_excel_pegado(texto):

    try:
        df = pd.read_csv(StringIO(texto), sep="\t")
        df.columns = df.columns.str.strip()
        return df
    except:
        return None


# ============================================================
# TARJETAS RESUMEN
# ============================================================

def tarjetas_grupo(df):

    total = len(df)

    gan = df["Estado"].str.contains("ganó", na=False).sum()
    elim = df["Estado"].str.contains("eliminado", na=False).sum()
    pend = total - gan - elim

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Partidos", total)
    c2.metric("Ganadores", gan)
    c3.metric("Eliminados", elim)
    c4.metric("Pendientes", pend)


# ============================================================
# PÁGINA GRUPO
# ============================================================

def pagina_grupo(n):

    st.header(f"👥 Grupo {n}")

    tab1, tab2 = st.tabs(["📥 Cargar Tabla", "📊 Gestión de Partidos"])

    # --------------------------------------------------------
    # CARGAR TABLA
    # --------------------------------------------------------

    with tab1:

        st.info("Copia la tabla desde Excel y pégala aquí")

        pasted = st.text_area("Pegar tabla", height=250)

        if pasted:

            df = leer_excel_pegado(pasted)

            if df is None:

                st.error("No se pudo leer la tabla")

            else:

                ok, msg, df = validar_tabla(df)

                if ok:

                    st.success("Tabla válida")

                    st.dataframe(df, use_container_width=True)

                    if st.button("💾 Guardar tabla"):

                        guardar_grupo(n, df)

                        st.success("Tabla guardada")

                else:

                    st.warning(msg)

    # --------------------------------------------------------
    # GESTIÓN
    # --------------------------------------------------------

    with tab2:

        df = cargar_grupo(n)

        if df is None:

            st.warning("Aún no hay tabla cargada")

            return

        tarjetas_grupo(df)

        st.subheader("📊 Tabla de Partidos")

        st.dataframe(
            df.style.apply(estado_color, axis=1),
            use_container_width=True,
            height=400
        )

        st.divider()

        # ----------------------------------------------------
        # BUSCAR PARTIDO
        # ----------------------------------------------------

        st.subheader("🔎 Buscar Partido")

        busqueda = st.text_input("Buscar jugador o ID")

        if busqueda:

            filtrado = df[
                df.apply(lambda r: busqueda.lower() in str(r).lower(), axis=1)
            ]

            st.dataframe(filtrado, use_container_width=True)

            if len(filtrado) == 1:

                fila = filtrado.iloc[0]

                g1 = fila["ID Grupo 1"]
                g2 = fila["ID Grupo 2"]

                ganador = st.radio(
                    "Seleccionar ganador",
                    [g1, g2],
                    horizontal=True
                )

                if st.button("🏆 Registrar ganador"):

                    registrar_ganador(n, fila, ganador)

                    st.success("Resultado guardado")

                    st.rerun()

        # ----------------------------------------------------
        # CORREGIR RESULTADO
        # ----------------------------------------------------

        st.divider()

        st.subheader("🛠 Corregir Resultado")

        p = st.text_input("Partido (ej: 851 vs 850)")
        g = st.text_input("Nuevo ganador")

        if st.button("Aplicar corrección"):

            ok, msg = corregir_ganador(n, p, g)

            if ok:

                st.success(msg)
                st.rerun()

            else:

                st.error(msg)

        # ----------------------------------------------------
        # EXPORTAR
        # ----------------------------------------------------

        st.divider()

        if st.button("📥 Exportar Excel Grupo"):

            exportar_excel_grupo(n)

            st.success("Archivo generado en carpeta data")


# ============================================================
# RESUMEN DEL TORNEO
# ============================================================

def pagina_resumen():

    st.header("📊 Dashboard del Torneo")

    grupos = cargar_todos()

    if not grupos:

        st.warning("No hay datos aún")

        return

    cols = st.columns(len(grupos))

    for i, (g, df) in enumerate(grupos.items()):

        total = len(df)
        gan = df["Estado"].str.contains("ganó", na=False).sum()

        cols[i].metric(
            f"Grupo {g}",
            total,
            f"{gan} ganadores"
        )

    st.divider()

    tablas = []

    for g, df in grupos.items():

        tablas.append([
            g,
            len(df),
            df["Estado"].str.contains("ganó", na=False).sum(),
            df["Estado"].str.contains("eliminado", na=False).sum()
        ])

    resumen = pd.DataFrame(
        tablas,
        columns=[
            "Grupo",
            "Partidos",
            "Ganadores",
            "Eliminados"
        ]
    )

    st.dataframe(resumen, use_container_width=True)

    st.divider()

    if st.button("📥 Exportar Excel Torneo"):

        exportar_excel_torneo()

        st.success("Excel generado")


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎲 Torneo Parchís")

menu = st.sidebar.radio(
    "Menú",
    [
        "Grupo 1",
        "Grupo 2",
        "Grupo 3",
        "Grupo 4",
        "Grupo 5",
        "Dashboard"
    ]
)

st.title("🎲 Torneo Parchís 2026")

if menu.startswith("Grupo"):

    n = int(menu.split(" ")[1])

    pagina_grupo(n)

elif menu == "Dashboard":

    pagina_resumen()
