import streamlit as st
import pandas as pd
import os
from io import StringIO

# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Torneo Parchís 2026",
    page_icon="🎲",
    layout="wide"
)

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)

# ============================================================
# ESTILO (UI MÁS LIMPIA)
# ============================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
background:#f4f6fb;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.block-container{
padding-top:2rem;
}

.partido-card{
background:white;
padding:20px;
border-radius:14px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
margin-bottom:18px;
}

.vs{
text-align:center;
font-size:22px;
font-weight:700;
padding-top:20px;
}

.ganador-btn button{
width:100%;
font-size:18px;
height:48px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# IMPORTS DE TU PROYECTO
# ============================================================

from utils.loader import cargar_grupo, guardar_grupo, cargar_todos
from utils.ganadores import registrar_ganador, corregir_ganador
from utils.validator import validar_tabla
from utils.excel_exporter import exportar_excel_grupo, exportar_excel_torneo

# ============================================================
# LEER TABLA PEGADA DESDE EXCEL
# ============================================================

def leer_excel_pegado(texto):

    try:

        df = pd.read_csv(
            StringIO(texto),
            sep="\t"
        )

        df.columns = df.columns.str.strip()

        return df

    except:

        return None


# ============================================================
# ASEGURAR COLUMNA ESTADO
# ============================================================

def asegurar_estado(df):

    if "Estado" not in df.columns:

        df["Estado"] = "pendiente"

    return df


# ============================================================
# TARJETAS DE ESTADÍSTICAS
# ============================================================

def dashboard_grupo(df):

    df = asegurar_estado(df)

    total = len(df)

    gan = df["Estado"].str.contains("gan", case=False, na=False).sum()
    elim = df["Estado"].str.contains("elim", case=False, na=False).sum()
    pend = total - gan - elim

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🎮 Partidos", total)
    c2.metric("🏆 Ganadores", gan)
    c3.metric("❌ Eliminados", elim)
    c4.metric("⏳ Pendientes", pend)


# ============================================================
# RENDER PARTIDO (CARD)
# ============================================================

def render_partido(n, row, idx):

    g1 = row["ID Grupo 1"]
    g2 = row["ID Grupo 2"]

    u1 = row["User 1 G1"]
    u2 = row["User 2 G1"]

    u3 = row["User 1 G2"]
    u4 = row["User 2 G2"]

    estado = row["Estado"]

    st.markdown('<div class="partido-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([4,1,4])

    with col1:

        st.markdown(f"### 🟣 {g1}")
        st.write(u1)
        st.write(u2)

    with col2:

        st.markdown('<div class="vs">VS</div>', unsafe_allow_html=True)

    with col3:

        st.markdown(f"### 🔵 {g2}")
        st.write(u3)
        st.write(u4)

    b1, b2, b3 = st.columns(3)

    with b1:

        if st.button(f"🏆 Ganó {g1}", key=f"{idx}g1"):

            registrar_ganador(n, row, g1)

            st.rerun()

    with b2:

        if st.button(f"🏆 Ganó {g2}", key=f"{idx}g2"):

            registrar_ganador(n, row, g2)

            st.rerun()

    with b3:

        st.write(f"Estado: **{estado}**")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# MOSTRAR PARTIDOS POR HORARIO
# ============================================================

def mostrar_partidos(n, df):

    df = asegurar_estado(df)

    horarios = df["Horario"].unique()

    for h in horarios:

        st.subheader(f"🕗 {h}")

        partidos = df[df["Horario"] == h]

        for i, row in partidos.iterrows():

            render_partido(n, row, i)


# ============================================================
# PAGINA GRUPO
# ============================================================

def pagina_grupo(n):

    st.header(f"👥 Grupo {n}")

    tab1, tab2 = st.tabs(["📥 Cargar tabla", "🎮 Partidos"])

    # --------------------------------------------------------
    # CARGAR TABLA
    # --------------------------------------------------------

    with tab1:

        st.info("Copia la tabla desde Excel y pégala aquí")

        pasted = st.text_area(
            "Tabla copiada desde Excel",
            height=250
        )

        if pasted:

            df = leer_excel_pegado(pasted)

            if df is None:

                st.error("No se pudo leer la tabla")

            else:

                ok, msg, df = validar_tabla(df)

                if ok:

                    df = asegurar_estado(df)

                    st.success("Tabla válida")

                    st.dataframe(df, use_container_width=True)

                    if st.button("💾 Guardar tabla grupo"):

                        guardar_grupo(n, df)

                        st.success("Grupo guardado")

                else:

                    st.warning(msg)

    # --------------------------------------------------------
    # PARTIDOS
    # --------------------------------------------------------

    with tab2:

        df = cargar_grupo(n)

        if df is None:

            st.warning("Aún no hay datos del grupo")

            return

        df = asegurar_estado(df)

        dashboard_grupo(df)

        st.divider()

        mostrar_partidos(n, df)

        st.divider()

        if st.button("📥 Exportar Excel Grupo"):

            exportar_excel_grupo(n)

            st.success("Excel generado en carpeta data")


# ============================================================
# DASHBOARD GENERAL
# ============================================================

def pagina_resumen():

    st.header("📊 Dashboard Torneo")

    grupos = cargar_todos()

    if not grupos:

        st.warning("Aún no hay datos")

        return

    cols = st.columns(len(grupos))

    for i, (g, df) in enumerate(grupos.items()):

        df = asegurar_estado(df)

        total = len(df)

        gan = df["Estado"].str.contains("gan", case=False, na=False).sum()

        cols[i].metric(
            f"Grupo {g}",
            total,
            f"{gan} ganadores"
        )

    st.divider()

    if st.button("📥 Exportar Excel Torneo"):

        exportar_excel_torneo()

        st.success("Excel generado")


# ============================================================
# MENU
# ============================================================

st.sidebar.title("🎲 Torneo Parchís")

menu = st.sidebar.selectbox(
    "Navegación",
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
