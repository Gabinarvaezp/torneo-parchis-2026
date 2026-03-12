import streamlit as st
import pandas as pd
import os

# ============================================================
# CONFIGURACIÓN GENERAL DE LA APP
# ============================================================

st.set_page_config(
    page_title="Torneo Parchís 2026",
    layout="wide",
)

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
# ESTILOS PASTEL CORPORATIVOS
# ============================================================

st.markdown(
    f"""
    <style>
    .main {{
        background-color: {PALETTE['neutral']};
    }}
    .stButton>button {{
        background-color: {PALETTE['primary']};
        color: white;
        border-radius: 10px;
        padding: 10px 30px;
        font-size: 18px;
    }}
    .stTextInput>div>input {{
        border-radius: 8px;
        border: 2px solid {PALETTE['primary']};
    }}
    h1, h2, h3, h4 {{
        color: {PALETTE['primary']};
        font-weight: 600;
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

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)


# ============================================================
# PÁGINA DE CADA GRUPO
# ============================================================

def pagina_grupo(n_grupo):

    st.header(f"👥 Grupo {n_grupo}")
    st.write("Pega la tabla EXACTA del Excel del Sábado 14. Nada de mover columnas.")

    pasted = st.text_area(
        f"Pega la tabla del Grupo {n_grupo}",
        height=250,
    )

    # -------------------------
    # Cargar tabla pegada
    # -------------------------
    if pasted:
        try:
            df = pd.read_csv(pd.io.common.StringIO(pasted), sep="\t")

            ok, msg = validar_tabla(df)
            if ok:
                st.success("Tabla detectada correctamente.")
                st.dataframe(df)

                if st.button("💾 Guardar Tabla"):
                    guardar_grupo(n_grupo, df)
                    st.success(f"Grupo {n_grupo} guardado.")
            else:
                st.error(msg)

        except Exception as e:
            st.error("Error al leer la tabla copiada. Asegúrate de pegarla EXACTA.")

    # -------------------------
    # Mostrar tabla guardada
    # -------------------------
    st.subheader("📊 Tabla Guardada del Grupo")
    df = cargar_grupo(n_grupo)

    if df is not None:
        st.dataframe(df.style.apply(estado_color, axis=1))

    # -------------------------
    # Registrar ganador
    # -------------------------
    st.subheader("🏆 Registrar Ganador")

    busqueda = st.text_input("Buscar por ID, nombre o usuario:")

    if busqueda and df is not None:
        fil = df[df.apply(lambda r: busqueda.lower() in str(r).lower(), axis=1)]
        st.dataframe(fil)

        if len(fil) == 1:
            fila = fil.iloc[0]
            e1 = fila["ID Grupo 1"]
            e2 = fila["ID Grupo 2"]

            ganador = st.radio("Selecciona el ganador:", [e1, e2])

            if st.button("Guardar Ganador"):
                registrar_ganador(n_grupo, fila, ganador)
                st.success(f"Ganador guardado: {ganador}")

    # -------------------------
    # Corregir Ganador
    # -------------------------
    st.subheader("🛠 Corregir Ganador")

    partido = st.text_input("Partido exacto: ej. '851 vs 850'")
    nuevo_g = st.text_input("Nuevo ganador (ID exacto)")

    if st.button("Corregir Resultado"):
        ok, msg = corregir_ganador(n_grupo, partido, nuevo_g)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

    # -------------------------
    # Descarga Excel del Grupo
    # -------------------------
    st.subheader("📥 Descargar Excel del Grupo")

    if st.button("Descargar Excel"):
        exportar_excel_grupo(n_grupo)
        st.success("Excel generado en /data")


# ============================================================
# RESUMEN DEL TORNEO
# ============================================================

def pagina_resumen():

    st.header("📊 Resumen General del Torneo")

    grupos = cargar_todos()

    if not grupos:
        st.warning("No hay datos cargados aún.")
        return

    cols = st.columns(5)
    i = 0

    for g, df in grupos.items():
        total = len(df)
        gan = df[df["Estado"].str.contains("ganó", na=False)]
        elim = df[df["Estado"].str.contains("eliminado", na=False)]
        pend = df[df["Estado"].str.contains("pendiente", na=False)]

        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background-color:{PALETTE['secondary']};
                    padding:20px;
                    border-radius:12px;
                    color:white;
                    text-align:center;">
                    <h3>Grupo {g}</h3>
                    <p><b>Total:</b> {total}</p>
                    <p><b>Ganadores:</b> {len(gan)}</p>
                    <p><b>Eliminados:</b> {len(elim)}</p>
                    <p><b>Pendientes:</b> {len(pend)}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        i = (i + 1) % 5

    st.subheader("📈 Avance por Grupo")
    rows = []

    for g, df in grupos.items():
        rows.append([
            g,
            len(df),
            df["Estado"].str.contains("ganó", na=False).sum(),
            df["Estado"].str.contains("eliminado", na=False).sum()
        ])

    st.dataframe(pd.DataFrame(rows, columns=["Grupo", "Total", "Ganadores", "Eliminados"]))

    st.subheader("📥 Descargar Todo el Torneo")

    if st.button("Exportar Excel Total"):
        exportar_excel_torneo()
        st.success("TorneoCompleto.xlsx generado en /data")


# ============================================================
# AJUSTES
# ============================================================

def pagina_ajustes():

    st.header("⚙ Ajustes del Torneo")

    max_partidos = st.slider("Máximo partidos por franja (ideal 20)", 10, 25, 20)
    descanso = st.slider("Descanso mínimo entre partidos (horas)", 1, 3, 2)
    extendidos = st.checkbox("Usar horarios extendidos?", value=True)

    if st.button("Guardar Ajustes"):
        config = {
            "max_partidos": max_partidos,
            "descanso": descanso,
            "extendidos": extendidos
        }
        pd.DataFrame([config]).to_json("data/config.json", orient="records")
        st.success("Ajustes guardados correctamente.")


# ============================================================
# RUTEO PRINCIPAL
# ============================================================

st.title("🎲 Torneo Parchís 2026")

menu = st.sidebar.radio(
    "Menú",
    ["Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4", "Grupo 5",
     "Resumen del Torneo", "Ajustes"]
)

if menu.startswith("Grupo"):
    n = int(menu.split(" ")[1])
    pagina_grupo(n)

elif menu == "Resumen del Torneo":
    pagina_resumen()

elif menu == "Ajustes":
    pagina_ajustes()

else:
    st.write("Selecciona una opción del menú.")
``
