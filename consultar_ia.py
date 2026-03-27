import pandas as pd
import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. Cargamos el mismo motor de IA que usamos ayer
print("Iniciando motor de búsqueda...")
modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def buscar_versiculo(pregunta, top_n=3):
    # 2. Conectamos a tu nueva base de datos
    conexion = sqlite3.connect('biblia_maestra.db')
    cursor = conexion.cursor()
    
    # 3. Convertimos tu pregunta en "matemáticas" (vector)
    vector_pregunta = modelo.encode(pregunta).tolist()
    
    # 4. Traemos todos los versículos para comparar
    cursor.execute("SELECT libro, capitulo, versiculo, texto, embedding FROM versiculos")
    resultados = cursor.fetchall()
    
    busquedas = []
    for r in resultados:
        libro, cap, ver, texto, emb_json = r
        emb_vector = json.loads(emb_json)
        
        # 5. Cálculo de similitud (¿Qué tanto se parece la pregunta al versículo?)
        similitud = np.dot(vector_pregunta, emb_vector) / (np.linalg.norm(vector_pregunta) * np.linalg.norm(emb_vector))
        busquedas.append((similitud, libro, cap, ver, texto))
    
    # Ordenamos de mayor a menor parecido
    busquedas.sort(key=lambda x: x[0], reverse=True)
    
    conexion.close()
    return busquedas[:top_n]

# --- Interfaz de Usuario ---
print("\n--- BIENVENIDO A TU BIBLIA IA ---")
while True:
    usuario = input("\n¿Cómo te sientes o qué buscas? (escribe 'salir' para terminar): ")
    if usuario.lower() == 'salir': break
    
    print(f"\nBuscando sabiduría para: '{usuario}'...")
    respuestas = buscar_versiculo(usuario)
    
    for i, res in enumerate(respuestas):
        sim, lib, cap, ver, texto = res
        print(f"\n[{i+1}] {lib} {cap}:{ver} (Coincidencia: {sim*100:.1f}%)")
        print(f" \"{texto}\"")
        import pandas as pd

def buscar_en_diccionario(palabra):
    try:
        # Cargamos los datos que extrajiste
        df_dic = pd.read_csv("diccionario_limpio.csv")
        # Buscamos la palabra exacta o parecida
        resultado = df_dic[df_dic['topic'].str.contains(palabra, case=False, na=False)]
        return resultado
    except:
        return None