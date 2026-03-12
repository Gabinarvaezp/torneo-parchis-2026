import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Torneo Parchís 2026", layout="wide")

DATA_PATH = "data"
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

st.title("🎲 Torneo de Parchís 2026")
st.markdown("Copia y pega los datos directamente desde Excel. No necesitas subir archivos.")

menu = st.sidebar.selectbox(
    "Menú",
    ["Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4", "Grupo 5", "Registrar Ganadores", "Siguiente Ronda"]
)

def guardar_grupo(num, df):
    df.to_csv(f"{DATA_PATH}/grupo{num}.csv", index=False)

def cargar_grupo(num):
    archivo = f"{DATA_PATH}/grupo{num}.csv"
    if os.path.exists(archivo):
        return pd.read_csv(archivo)
    return None

# --- COPIAR Y PEGAR --
if "Grupo" in menu:
    grupo_num = int(menu.split(" ")[1])
    st.subheader(f"📋 Participantes del Grupo {grupo_num}")
    st.write("Pega aquí la tabla directamente desde Excel (CTRL+C → CTRL+V):")

    texto = st.text_area("Pega aquí los datos del grupo")

    if texto:
        try:
            df = pd.read_csv(pd.io.common.StringIO(texto), sep="\t")
            st.dataframe(df)

            if st.button("Guardar grupo"):
                guardar_grupo(grupo_num, df)
                st.success(f"Grupo {grupo_num} guardado correctamente.")
        except:
            st.error("La tabla no es válida. Asegúrate de copiar TODAS las columnas de Excel.")

    existente = cargar_grupo(grupo_num)
    if existente is not None:
        st.write("### Datos guardados en la nube:")
        st.dataframe(existente)

# --- REGISTRAR GANADORES ---
elif menu == "Registrar Ganadores":
    st.subheader("🏆 Registrar Ganador del Partido")
    grupos = []

    # Cargar todos los grupos
    for i in range(1, 6):
        df = cargar_grupo(i)
        if df is not None:
            df["Grupo"] = i
            grupos.append(df)

    if grupos:
        todos = pd.concat(grupos, ignore_index=True)

        busqueda = st.text_input("Busca por nombre, usuario o ID")
        if busqueda:
            filtro = todos[todos.apply(lambda x: busqueda.lower() in str(x).lower(), axis=1)]
            st.dataframe(filtro)

            if len(filtro) == 1:
                fila = filtro.iloc[0]
                e1 = fila["ID Grupo 1"]
                e2 = fila["ID Grupo 2"]

                ganador = st.radio("¿Quién ganó?", [e1, e2])

                if st.button("Guardar ganador"):
                    with open(f"{DATA_PATH}/resultados.csv", "a") as f:
                        f.write(f"{ganador}\n")
                    st.success("Ganador registrado correctamente.")

# --- SIGUIENTE RONDA ---
elif menu == "Siguiente Ronda":
    st.subheader("🔄 Generar nueva ronda automáticamente")

    if st.button("Generar"):
        resultados = f"{DATA_PATH}/resultados.csv"
        if not os.path.exists(resultados):
            st.error("Aún no hay resultados registrados.")
        else:
            df = pd.read_csv(resultados, header=None, names=["Ganador"])
            ganadores = df["Ganador"].tolist()

            # Emparejar ganadores
            parejas = []
            for i in range(0, len(ganadores), 2):
                if i+1 < len(ganadores):
                    parejas.append([ganadores[i], ganadores[i+1]])

            salida = pd.DataFrame(parejas, columns=["Equipo A", "Equipo B"])
            salida.to_csv(f"{DATA_PATH}/ronda_siguiente.csv", index=False)

            st.success("Nueva ronda generada correctamente.")
            st.dataframe(salida)
