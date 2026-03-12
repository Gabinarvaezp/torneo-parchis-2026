import streamlit as st
import pandas as pd
import os

# ---------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------
st.set_page_config(
    page_title="Torneo Parchís 2026",
    layout="wide",
)

PALETTE = {
    "primary": "#A38ACB",    # Lila corporativo pastel
    "secondary": "#83A4D4",  # Azul suave corporativo
    "accent": "#9FD8C8",     # Verde aqua pastel
    "warning": "#F7C6A3",    # Melón pastel
    "danger": "#F3A5A5",     # Rojo pastel profesional
    "success": "#A4E1B9",    # Verde éxito
    "neutral": "#F5F5F7",    # Fondo gris blanco elegante
}

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
        font-size: 18px;
        padding: 10px 25px;
        border: none;
    }}
    h1, h2, h3 {{
        color: {PALETTE['primary']};
        font-weight: 600;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)

# ---------------------------
# UTILIDADES
# ---------------------------
def save_group_data(group_num, df):
    df.to_csv(f"{DATA_PATH}/grupo{group_num}.csv", index=False)

def load_group_data(group_num):
    file = f"{DATA_PATH}/grupo{group_num}.csv"
    if os.path.exists(file):
        return pd.read_csv(file)
    return None

# ---------------------------
# INTERFAZ PRINCIPAL
# ---------------------------
st.title("🎲 Torneo Parchís 2026")
st.subheader("Gestión profesional del torneo • Estilo pastel corporativo")

menu = st.sidebar.radio(
    "Navegación",
    ["Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4", "Grupo 5", "Resumen", "Ajustes"]
)

# ---------------------------
# FUNCIONES DE GRUPO
# ---------------------------
def group_page(group_num):

    st.header(f"👥 Grupo {group_num}")
    st.info(f"Copia y pega aquí la tabla EXACTA del Excel de la ronda del Sábado 14.")

    pasted_text = st.text_area(
        f"Pega aquí la tabla del Grupo {group_num}",
        height=250,
        placeholder="Pega la tabla del Excel (con horarios, IDs, jugadores, users...)"
    )

    if pasted_text:
        try:
            df = pd.read_csv(pd.io.common.StringIO(pasted_text), sep="\t")
            st.success("Vista previa de la tabla cargada:")
            st.dataframe(df)

            if st.button("Guardar tabla del grupo"):
                save_group_data(group_num, df)
                st.success(f"Grupo {group_num} guardado correctamente.")

        except Exception as e:
            st.error("No pudimos leer la tabla. Asegúrate que la pegaste tal cual de Excel.")

    st.subheader("📊 Datos guardados")
    saved_df = load_group_data(group_num)
    if saved_df is not None:
        st.dataframe(saved_df)
    else:
        st.warning("No hay datos guardados todavía.")

# ---------------------------
# ROUTING
# ---------------------------
if menu.startswith("Grupo"):
    num = int(menu.split(" ")[1])
    group_page(num)

elif menu == "Resumen":
    st.header("📊 Resumen del Torneo")
    st.info("Aquí aparecerán los dashboards, el estado del torneo y los ganadores.")

elif menu == "Ajustes":
    st.header("⚙ Ajustes")
    st.info("Aquí podrás configurar rondas, horarios y reglas.")
