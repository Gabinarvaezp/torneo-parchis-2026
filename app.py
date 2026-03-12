import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(
    page_title="Torneo Parchís",
    page_icon="🎲",
    layout="wide"
)

# ====================================================
# TEMA VISUAL MODERNO
# ====================================================

st.markdown("""
<style>

body {
    background: linear-gradient(135deg,#f5f6fa,#f1f2ff);
}

.big-title {
    font-size:40px;
    font-weight:700;
    color:#6c5ce7;
}

.card {
    padding:20px;
    border-radius:15px;
    background:linear-gradient(135deg,#a29bfe,#81ecec);
    color:white;
    text-align:center;
    box-shadow:0px 5px 20px rgba(0,0,0,0.15);
}

.card h3{
    margin:0;
}

.card p{
    font-size:30px;
    font-weight:bold;
}

.sidebar-title{
    font-size:20px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# ====================================================
# HEADER
# ====================================================

col1, col2 = st.columns([1,6])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=70)

with col2:
    st.markdown('<p class="big-title">Torneo Parchís 2026</p>', unsafe_allow_html=True)

st.divider()

# ====================================================
# DASHBOARD
# ====================================================

st.subheader("Dashboard del Torneo")

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.markdown('<div class="card"><h3>Grupos</h3><p>5</p></div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card"><h3>Parejas</h3><p>1400</p></div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card"><h3>Partidos</h3><p>700</p></div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card"><h3>Eliminados</h3><p>0</p></div>', unsafe_allow_html=True)

with c5:
    st.markdown('<div class="card"><h3>Clasificados</h3><p>0</p></div>', unsafe_allow_html=True)

st.divider()

# ====================================================
# TABLA PROFESIONAL
# ====================================================

st.subheader("Grupo 1")

data = {
    "Horario":["8:00","8:00","8:30"],
    "Equipo A":["851","852","853"],
    "Equipo B":["850","849","848"],
    "Estado":["Pendiente","Pendiente","Pendiente"]
}

df = pd.DataFrame(data)

gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_pagination()
gb.configure_default_column(filter=True, sortable=True)
gb.configure_selection('single')

gridOptions = gb.build()

AgGrid(
    df,
    gridOptions=gridOptions,
    height=400,
    theme="streamlit",
)
