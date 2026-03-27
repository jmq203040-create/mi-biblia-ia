import streamlit as st
import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Configuración elegante de la página
st.set_page_config(page_title="Biblia IA: Estudio Pro", page_icon="📖", layout="wide")

@st.cache_resource
def cargar_modelo():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

modelo = cargar_modelo()

def buscar(pregunta):
    conexion = sqlite3.connect('biblia_maestra.db')
    cursor = conexion.cursor()
    vector_pregunta = modelo.encode(pregunta).tolist()
    cursor.execute("SELECT libro, capitulo, versiculo, texto, embedding FROM versiculos")
    resultados = cursor.fetchall()
    
    busquedas = []
    for r in resultados:
        libro, cap, ver, texto, emb_json = r
        emb_vector = json.loads(emb_json)
        similitud = np.dot(vector_pregunta, emb_vector) / (np.linalg.norm(vector_pregunta) * np.linalg.norm(emb_vector))
        busquedas.append((similitud, libro, cap, ver, texto))
    
    busquedas.sort(key=lambda x: x[0], reverse=True)
    conexion.close()
    return busquedas[:5]

# --- DISEÑO DE LA INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📖 Biblia de Estudio con IA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Encuentra sabiduría basada en el significado de tus palabras.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔍 Panel de Búsqueda")
    pregunta = st.text_area("¿Qué buscas hoy?", placeholder="Ej: Necesito consuelo para un amigo que perdió a alguien...")
    boton = st.button("Consultar a la IA")

with col2:
    st.subheader("📜 Resultados de Estudio")
    if boton and pregunta:
        with st.spinner('Escudriñando las Escrituras...'):
            res = buscar(pregunta)
            for sim, lib, cap, ver, texto in res:
                porcentaje = int(sim * 100)
                with st.expander(f"📍 {lib} {cap}:{ver} - Coincidencia {porcentaje}%"):
                    st.write(f"*{texto}*")
                    st.progress(sim)
                    st.caption("Usa este versículo para tu estudio personal de hoy.")
    else:
        st.info("Escribe algo a la izquierda para comenzar el análisis.")