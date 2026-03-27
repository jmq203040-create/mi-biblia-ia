import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Biblia de Estudio Pro", page_icon="📖", layout="wide")

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_diccionario():
    try:
        return pd.read_csv("diccionario_limpio.csv")
    except:
        return None

df_diccionario = cargar_diccionario()

# --- INTERFAZ ---
st.title("📖 Biblia de Estudio con IA")
st.markdown("Busca versículos y consulta el **Diccionario Vine** al instante.")

busqueda = st.text_input("¿Qué deseas estudiar hoy?", placeholder="Ej: Amor, Fe, Justificación...")

if busqueda:
    # Creamos las pestañas
    tab1, tab2 = st.tabs(["📜 Versículos encontrados", "📚 Diccionario Vine"])

    with tab1:
        st.subheader("Resultados de la Biblia")
        # Aquí llamaríamos a tu función de búsqueda por IA que ya tienes
        # (Asegúrate de mantener tu lógica de 'consultar_ia' aquí abajo)
        st.info("Mostrando versículos relacionados con: " + busqueda)
        # [PEGA AQUÍ TU LÓGICA ACTUAL DE RESULTADOS DE BIBLIA]

    with tab2:
        st.subheader("Definiciones del Diccionario Vine")
        if df_diccionario is not None:
            # Buscamos palabras que coincidan con lo que el usuario escribió
            resultado_dic = df_diccionario[df_diccionario['topic'].str.contains(busqueda, case=False, na=False)]
            
            if not resultado_dic.empty:
                for index, row in resultado_dic.iterrows():
                    with st.expander(f"📙 Definición de: {row['topic']}"):
                        st.markdown(row['definition'])
            else:
                st.warning("No se encontró esa palabra exacta en el diccionario, pero puedes ver los versículos relacionados.")
        else:
            st.error("Archivo 'diccionario_limpio.csv' no encontrado.")
