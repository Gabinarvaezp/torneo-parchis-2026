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
# ESTILOS PRO
# ============================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
background:#f4f6fb;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

h1{
font-weight:700;
}

.card{
background:white;
padding:25px;
border-radius:16px;
box-shadow:0 5px 20px rgba(0,0,0,0.08);
text-align:center;
}

.stButton>button{
background:#6C5CE7;
color:white;
border:none;
border-radius:10px;
padding:10px 20px;
font-weight:600;
}

.stButton>button:hover{
background:#5649c9;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# IMPORTS
# ============================================================

from utils.loader import cargar_grupo, guardar_grupo, cargar_todos
from utils.ganadores import registrar_ganador, corregir_ganador
from utils.validator import validar_tabla
from utils.estilos import estado_color
from utils.excel_exporter import exportar_excel_grupo, exportar_excel_torneo

# ============================================================
# LEER EXCEL PEGADO
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
# TARJETAS
# ============================================================

def card(titulo, valor):

    st.markdown(
        f"""
        <div class="card">
        <h3>{titulo}</h3>
        <h1>{valor}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


def tarjetas_grupo(df):

    if "Estado" not in df.columns:
        df["Estado"] = "pendiente"

    total = len(df)

    gan = df["Estado"].str.contains("gan", case=False, na=False).sum()
    elim = df["Estado"].str.contains("elim", case=False, na=False).sum()
    pend = total - gan - elim

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        card("🎮 Partidos", total)

    with c2:
        card("🏆 Ganadores", gan)

    with c3:
        card("❌ Eliminados", elim)

    with c4:
        card("⏳ Pendientes", pend)


# ============================================================
# PAGINA GRUPO
# ============================================================

def pagina_grupo(n):

    st.header(f"👥 Grupo {n}")

    tab1, tab2 = st.tabs(["📥 Cargar tabla", "🎮 Gestionar"])

    # --------------------------------------------------------
    # CARGAR TABLA
    # --------------------------------------------------------

    with tab1:

        pasted = st.text_area(
            "Pega aquí la tabla copiada desde Excel",
            height=250
        )

        if pasted:

            df = leer_excel_pegado(pasted)

            if df is None:

                st.error("No se pudo leer la tabla")

            else:

                ok,msg,df = validar_tabla(df)

                if ok:

                    st.success("Tabla válida")

                    if "Estado" not in df.columns:
                        df["Estado"] = "pendiente"

                    st.dataframe(df, use_container_width=True)

                    if st.button("💾 Guardar tabla"):

                        guardar_grupo(n, df)

                        st.success("Tabla guardada")

                else:

                    st.warning(msg)

    # --------------------------------------------------------
    # GESTION
    # --------------------------------------------------------

    with tab2:

        df = cargar_grupo(n)

        if df is None:

            st.warning("Aún no hay datos")

            return

        if "Estado" not in df.columns:
            df["Estado"] = "pendiente"

        tarjetas_grupo(df)

        st.subheader("📊 Partidos")

        st.dataframe(
            df.style.apply(estado_color, axis=1),
            use_container_width=True,
            height=500
        )

        # ----------------------------------------------------
        # BUSCAR PARTIDO
        # ----------------------------------------------------

        st.divider()

        busqueda = st.text_input(
            "🔎 Buscar jugador o ID",
            placeholder="Ej: 851"
        )

        if busqueda:

            fil = df[
                df.apply(
                    lambda r: busqueda.lower() in str(r).lower(),
                    axis=1
                )
            ]

            st.dataframe(fil, use_container_width=True)

            if len(fil) == 1:

                fila = fil.iloc[0]

                e1 = fila["ID Grupo 1"]
                e2 = fila["ID Grupo 2"]

                ganador = st.radio(
                    "Seleccionar ganador",
                    [e1,e2],
                    horizontal=True
                )

                if st.button("🏆 Registrar ganador"):

                    registrar_ganador(
                        n,
                        fila,
                        ganador
                    )

                    st.success("Resultado guardado")

                    st.rerun()

        # ----------------------------------------------------
        # CORREGIR RESULTADO
        # ----------------------------------------------------

        st.divider()

        st.subheader("🛠 Corregir resultado")

        partido = st.text_input(
            "Partido exacto (ej: 851 vs 850)"
        )

        nuevo = st.text_input(
            "Nuevo ganador"
        )

        if st.button("Aplicar corrección"):

            ok,msg = corregir_ganador(
                n,
                partido,
                nuevo
            )

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

            st.success("Excel generado")


# ============================================================
# RESUMEN TORNEO
# ============================================================

def pagina_resumen():

    st.header("📊 Dashboard del Torneo")

    grupos = cargar_todos()

    if not grupos:

        st.warning("No hay datos")

        return

    cols = st.columns(len(grupos))

    for i,(g,df) in enumerate(grupos.items()):

        if "Estado" not in df.columns:
            df["Estado"] = "pendiente"

        total = len(df)
        gan = df["Estado"].str.contains("gan",case=False,na=False).sum()

        cols[i].metric(
            f"Grupo {g}",
            total,
            f"{gan} ganadores"
        )

    st.divider()

    if st.button("📥 Exportar Excel torneo"):

        exportar_excel_torneo()

        st.success("Excel generado")


# ============================================================
# MENU
# ============================================================

st.sidebar.title("🎲 Torneo")

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
