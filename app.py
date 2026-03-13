import streamlit as st
import pandas as pd
from io import StringIO
import os

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
# ESTILO PRO (claro, moderno)
# ============================================================

st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
  background: linear-gradient(135deg,#f7f9fc,#eef3ff);
}

.block-container{
  padding-top:2rem;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.hub-card{
  background:white;
  padding:24px;
  border-radius:16px;
  box-shadow:0 6px 20px rgba(0,0,0,0.08);
  text-align:center;
  margin-bottom:20px;
}

.partido{
  background:white;
  padding:18px;
  border-radius:14px;
  box-shadow:0 4px 14px rgba(0,0,0,0.08);
  margin-bottom:14px;
}

.equipo{
  font-size:20px;
  font-weight:600;
}

.vs{
  text-align:center;
  font-size:22px;
  font-weight:800;
  padding-top:12px;
}

.estado{
  font-size:14px;
  color:#666;
}

button[kind="primary"]{
  border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# IMPORTS DEL PROYECTO
# ============================================================

from utils.loader import cargar_grupo, guardar_grupo, cargar_todos
from utils.ganadores import registrar_ganador
from utils.validator import validar_tabla
from utils.excel_exporter import exportar_excel_grupo, exportar_excel_torneo

# ============================================================
# HELPERS
# ============================================================

def asegurar_estado(df):
    if "Estado" not in df.columns:
        df["Estado"] = "pendiente"
    return df

def leer_excel_pegado(texto):
    try:
        df = pd.read_csv(StringIO(texto), sep="\t")
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

# ============================================================
# HUB PRINCIPAL (pantalla inicial)
# ============================================================

def pantalla_inicio():

    st.title("🎲 Torneo Parchís 2026")

    st.markdown("### Panel del torneo")

    grupos = ["Grupo 1","Grupo 2","Grupo 3","Grupo 4","Grupo 5"]

    cols = st.columns(3)

    for i,g in enumerate(grupos):

        with cols[i%3]:

            st.markdown(f"""
            <div class="hub-card">
            <h3>{g}</h3>
            <p>Gestionar partidos</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Abrir {g}", key=f"hub{i}"):

                st.session_state["grupo_actual"] = int(g.split(" ")[1])

                st.rerun()

    st.divider()

    if st.button("📊 Ver dashboard torneo"):
        st.session_state["dashboard"] = True
        st.rerun()

# ============================================================
# TARJETAS DE ESTADÍSTICAS
# ============================================================

def estadisticas(df):

    df = asegurar_estado(df)

    total = len(df)
    gan = df["Estado"].str.contains("gan",case=False,na=False).sum()
    pend = total - gan

    c1,c2,c3 = st.columns(3)

    c1.metric("Partidos", total)
    c2.metric("Ganados", gan)
    c3.metric("Pendientes", pend)

# ============================================================
# TARJETAS DE PARTIDOS
# ============================================================

def tarjeta_partido(n,row,idx):

    g1 = row["ID Grupo 1"]
    g2 = row["ID Grupo 2"]

    u1 = row["User 1 G1"]
    u2 = row["User 2 G1"]
    u3 = row["User 1 G2"]
    u4 = row["User 2 G2"]

    estado = row["Estado"]

    st.markdown('<div class="partido">', unsafe_allow_html=True)

    col1,col2,col3 = st.columns([4,1,4])

    with col1:
        st.markdown(f'<div class="equipo">🟣 {g1}</div>', unsafe_allow_html=True)
        st.write(u1)
        st.write(u2)

    with col2:
        st.markdown('<div class="vs">VS</div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="equipo">🔵 {g2}</div>', unsafe_allow_html=True)
        st.write(u3)
        st.write(u4)

    b1,b2,b3 = st.columns(3)

    with b1:
        if st.button(f"🏆 {g1}", key=f"{idx}a"):
            registrar_ganador(n,row,g1)
            st.rerun()

    with b2:
        if st.button(f"🏆 {g2}", key=f"{idx}b"):
            registrar_ganador(n,row,g2)
            st.rerun()

    with b3:
        st.markdown(f'<div class="estado">Estado: {estado}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# INTERFAZ DE GRUPO
# ============================================================

def pagina_grupo(n):

    st.title(f"👥 Grupo {n}")

    colA,colB = st.columns([1,1])

    with colA:
        if st.button("🔄 Actualizar"):
            st.rerun()

    with colB:
        if st.button("⬅ Volver"):
            st.session_state.clear()
            st.rerun()

    tab1,tab2 = st.tabs(["Partidos","Cargar tabla"])

    # --------------------------------------------------------
    # PARTIDOS
    # --------------------------------------------------------

    with tab1:

        df = cargar_grupo(n)

        if df is None:
            st.warning("No hay datos cargados")
            return

        df = asegurar_estado(df)

        estadisticas(df)

        st.divider()

        filtro = st.selectbox(
            "Filtrar estado",
            ["Todos","Pendiente","Ganó"]
        )

        if filtro != "Todos":
            df = df[df["Estado"].str.contains(filtro,case=False,na=False)]

        horarios = df["Horario"].unique()

        for h in horarios:

            st.subheader(f"🕒 {h}")

            juegos = df[df["Horario"]==h]

            for i,row in juegos.iterrows():

                tarjeta_partido(n,row,i)

        if st.button("📥 Exportar Excel Grupo"):
            exportar_excel_grupo(n)
            st.success("Excel generado")

    # --------------------------------------------------------
    # CARGAR TABLA
    # --------------------------------------------------------

    with tab2:

        texto = st.text_area(
            "Pega la tabla desde Excel",
            height=220
        )

        if texto:

            df = leer_excel_pegado(texto)

            if df is None:

                st.error("No se pudo leer la tabla")

            else:

                ok,msg,df = validar_tabla(df)

                if ok:

                    df = asegurar_estado(df)

                    st.success("Tabla válida")

                    st.dataframe(df)

                    if st.button("Guardar grupo"):

                        guardar_grupo(n,df)

                        st.success("Grupo guardado")

                else:

                    st.warning(msg)

# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    st.title("📊 Dashboard Torneo")

    grupos = cargar_todos()

    if not grupos:
        st.warning("No hay datos")
        return

    cols = st.columns(len(grupos))

    for i,(g,df) in enumerate(grupos.items()):

        df = asegurar_estado(df)

        total = len(df)
        gan = df["Estado"].str.contains("gan",case=False,na=False).sum()

        cols[i].metric(
            f"Grupo {g}",
            total,
            f"{gan} ganados"
        )

    if st.button("Exportar torneo"):
        exportar_excel_torneo()
        st.success("Excel generado")

# ============================================================
# ROUTER
# ============================================================

if "grupo_actual" not in st.session_state and "dashboard" not in st.session_state:

    pantalla_inicio()

elif "grupo_actual" in st.session_state:

    pagina_grupo(st.session_state["grupo_actual"])

elif "dashboard" in st.session_state:

    dashboard()
