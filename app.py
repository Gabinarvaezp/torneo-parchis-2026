import streamlit as st
import pandas as pd
import os
from utils.lector_datos import cargar_todos_los_grupos
from utils.generador_rondas import generar_siguiente_ronda
from utils.estilos import pastel_css

st.set_page_config(page_title="Torneo de Parchís", layout="wide")

# Estilos pastel
st.markdown(pastel_css, unsafe_allow_html=True)

st.title("🎲 Torneo Profesional de Parchís 2026")
st.subheader("Dashboard General")

# Cargar datos
df = cargar_todos_los_grupos()

menu = st.sidebar.selectbox(
    "Selecciona una vista",
    ["Vista general", "Por grupo", "Registrar ganador", "Generar siguiente ronda"]
)

if menu == "Vista general":
    st.write("### Todos los partidos")
    st.dataframe(df)

elif menu == "Por grupo":
    grupo = st.selectbox("Selecciona el grupo", sorted(df["Grupo"].unique()))
    st.write(f"### Partidos del grupo {grupo}")
    st.dataframe(df[df["Grupo"] == grupo])

elif menu == "Registrar ganador":
    st.write("### Registrar un ganador")

    equipo = st.text_input("Busca el equipo por ID, Nombre o Usuario")
    if equipo:
        filtro = df[df.apply(lambda x: equipo.lower() in str(x).lower(), axis=1)]
        st.dataframe(filtro)

        if len(filtro) == 1:
            fila = filtro.iloc[0]
            equipo1 = fila["ID_Equipo1"]
            equipo2 = fila["ID_Equipo2"]

            ganador = st.radio("¿Quién ganó?", [equipo1, equipo2])
            if st.button("Guardar resultado"):
                with open("data/resultados.csv", "a") as f:
                    f.write(f"{ganador}\n")
                st.success("¡Resultado guardado!")

elif menu == "Generar siguiente ronda":
    if st.button("Generar nueva ronda"):
        generar_siguiente_ronda()
        st.success("Nueva ronda generada correctamente.")
