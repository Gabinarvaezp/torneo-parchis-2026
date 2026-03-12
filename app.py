import streamlit as st
import pandas as pd
import os

# ============================================================
# CONFIGURACIÓN GENERAL DE LA APP - ESTILO PASTEL CORPORATIVO
# ============================================================

st.set_page_config(
    page_title="Torneo Parchís 2026",
    layout="wide",
)

PALETTE = {
    "primary": "#8C7AE6",       # Lila corporativo pastel
    "secondary": "#74B9FF",     # Azul corporativo suave
    "accent": "#81ECEC",        # Aqua pastel elegante
    "warning": "#FAB1A0",       # Melón pastel
    "danger": "#FF7675",        # Rojo pastel profesional
    "success": "#55EFC4",       # Verde éxito pastel
    "neutral": "#F5F6FA",       # Blanco/gris limpio
}

# ============================================================
# ESTILOS CSS PASTEL CORPORATIVOS
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
        border: none;
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
# CARPETA DE DATOS
# ============================================================

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)

# ============================================================
# IMPORTAR FUNCIONES (SE CREARÁN EN EL BLOQUE B)
# ============================================================

from utils.loader import cargar_grupo, guardar_grupo
from utils.ganadores import registrar_ganador, corregir_ganador
from utils.rounds import generar_ronda_21, generar_ronda_28
from utils.scheduler import asignar_horarios
from utils.excel_exporter import exportar_excel_grupo, exportar_excel_torneo
from utils.styles import estado_color
from utils.validator import validar_tabla

# ============================================================
# FUNCIÓN PRINCIPAL DE PÁGINAS POR GRUPO
# ============================================================

def pagina_grupo(n_grupo):

    st.header(f"👥 Grupo {n_grupo}")
    st.write("Peguen aquí la tabla EXACTA del Excel del sábado 14.")

    pasted = st.text_area(
        f"📥 Pega la tabla del Grupo {n_grupo} (copiar y pegar desde Excel)",
        height=250
    )

    if pasted:
        try:
            df = pd.read_csv(pd.io.common.StringIO(pasted), sep="\t")
            ok, msg = validar_tabla(df)

            if ok:
                st.success("Tabla detectada correctamente. Previsualización:")
                st.dataframe(df)

                if st.button("💾 Guardar tabla del grupo"):
                    guardar_grupo(n_grupo, df)
                    st.success(f"Grupo {n_grupo} guardado.")
            else:
                st.error(msg)

        except:
            st.error("No pudimos leer la tabla. Asegúrate de pegarla EXACTA desde Excel.")

    st.subheader("📊 Tabla guardada")
    df = cargar_grupo(n_grupo)
    if df is not None:
        st.dataframe(df.style.apply(estado_color, axis=1))

    # ========================================================
    # SECCIÓN: REGISTRAR GANADOR
    # ========================================================

    st.subheader("🏆 Registrar ganador")

    busqueda = st.text_input("Buscar partido por ID, jugador, user:")

    if busqueda and df is not None:
        fil = df[df.apply(lambda row: busqueda.lower() in str(row).lower(), axis=1)]
        st.dataframe(fil)

        if len(fil) == 1:
            fila = fil.iloc[0]
            equipo1 = fila["ID Grupo 1"]
            equipo2 = fila["ID Grupo 2"]

            ganador = st.radio("¿Quién ganó?", [equipo1, equipo2])

            if st.button("Guardar ganador"):
                registrar_ganador(n_grupo, fila, ganador)
                st.success(f"Ganador registrado: {ganador}")

    # ========================================================
    # SECCIÓN: CORREGIR GANADOR
    # ========================================================

    st.subheader("🛠 Corregir ganador")

    partido_txt = st.text_input("Partido exacto (ej: '851 vs 850'):")
    nuevo_ganador = st.text_input("Nuevo ganador (ID exacto):")

    if st.button("Corregir resultado"):
        ok, msg = corregir_ganador(n_grupo, partido_txt, nuevo_ganador)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

    # ========================================================
    # DESCARGAS
    # ========================================================

    st.subheader("📥 Descargar reportes del grupo")

    if st.button("Descargar Excel del Grupo"):
        exportar_excel_grupo(n_grupo)
        st.success("Excel generado. Disponible en /data")


# ============================================================
# RUTEO PRINCIPAL
# ============================================================

st.title("🎲 Torneo Parchís 2026")
menu = st.sidebar.radio(
    "Navegación",
    ["Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4", "Grupo 5",
     "Resumen del Torneo", "Ajustes"]
)

if menu.startswith("Grupo"):
    g = int(menu.split(" ")[1])
    pagina_grupo(g)

elif menu == "Resumen del Torneo":
    st.header("📊 Resumen general del torneo")
    st.write("Aquí irá el dashboard pastel, semifinal y final. (Bloque C)")

    if st.button("Exportar Excel COMPLETO del torneo"):
        exportar_excel_torneo()
        st.success("Excel total exportado.")

elif menu == "Ajustes":
    st.header("⚙ Ajustes del torneo")
    st.write("Aquí se configurarán horarios, límites y reglas. (Bloque C)")

# ============================================================
# RESUMEN DEL TORNEO - BLOQUE C
# ============================================================

def pagina_resumen():

    st.header("📊 Resumen General del Torneo")

    grupos = cargar_todos()

    if not grupos:
        st.warning("No hay datos cargados todavía.")
        return

    # TARJETAS PASTEL POR GRUPO
    cols = st.columns(5)
    idx = 0

    for g, df in grupos.items():
        totales = len(df)
        gan = df[df["Estado"].str.contains("ganó", na=False)]
        elim = df[df["Estado"].str.contains("eliminado", na=False)]
        pend = df[df["Estado"].str.contains("pendiente", na=False)]

        with cols[idx]:
            st.markdown(
                f"""
                <div style="
                    background-color:{PALETTE['secondary']};
                    padding:20px;
                    border-radius:12px;
                    text-align:center;
                    color:white;">
                    <h3>Grupo {g}</h3>
                    <p><b>Total:</b> {totales}</p>
                    <p><b>Ganadores:</b> {len(gan)}</p>
                    <p><b>Eliminados:</b> {len(elim)}</p>
                    <p><b>Pendientes:</b> {len(pend)}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        idx = (idx + 1) % 5

    st.subheader("📈 Avance por grupo")

    resumen = []

    for g, df in grupos.items():
        total = len(df)
        gan = df[df["Estado"].str.contains("ganó", na=False)]
        elim = df[df["Estado"].str.contains("eliminado", na=False)]
        resumen.append([g, total, len(gan), len(elim)])

    res_df = pd.DataFrame(resumen, columns=["Grupo", "Total", "Ganadores", "Eliminados"])
    st.dataframe(res_df)

    # DESCARGAR EXCEL COMPLETO
    st.subheader("📥 Exportar Torneo Completo")

    if st.button("Exportar Excel Total"):
        ok = exportar_excel_torneo()
        if ok:
            st.success("Excel completo generado en la carpeta /data.")
        else:
            st.error("No fue posible generar el Excel.")
