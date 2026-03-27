import streamlit as st
from consultar_ia import buscar_versiculo, buscar_en_diccionario

st.set_page_config(page_title="Biblia de Estudio Pro", page_icon="📖", layout="wide")

st.title("📖 Biblia de Estudio con IA")
st.markdown("Encuentra sabiduría en la Biblia y el Diccionario Vine.")

pregunta = st.text_input("¿Qué deseas investigar hoy?", placeholder="Ej: Redención, Gracia, Esperanza...")

if pregunta:
    # Creamos las pestañas para organizar la info
    tab1, tab2 = st.tabs(["📜 Versículos de la IA", "📚 Diccionario Vine"])

    with tab1:
        st.subheader("Resultados de Estudio")
        resultados = buscar_versiculo(pregunta) # Llama a tu motor de IA
        if resultados:
            for sim, libro, cap, ver, texto in resultados:
                with st.expander(f"📍 {libro} {cap}:{ver} - Coincidencia {int(sim*100)}%"):
                    st.write(texto)
        else:
            st.write("No se encontraron versículos relacionados.")

    with tab2:
        st.subheader("Definiciones del Diccionario")
        definiciones = buscar_en_diccionario(pregunta)
        if definiciones is not None and not definiciones.empty:
            for i, row in definiciones.iterrows():
                with st.expander(f"📙 {row['topic']}"):
                    st.write(row['definition'])
        else:
            st.info("No hay una definición exacta en el diccionario para esta palabra.")