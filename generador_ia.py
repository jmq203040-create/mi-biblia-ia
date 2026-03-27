import sqlite3
import json
import csv
from sentence_transformers import SentenceTransformer

# 1. Cargar el cerebro de la IA (Modelo optimizado para español)
print("Cargando el motor de Inteligencia Artificial (Esto puede tardar un minuto la primera vez)...")
modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 2. Crear y conectar nuestra base de datos definitiva
conexion = sqlite3.connect('biblia_maestra.db')
cursor = conexion.cursor()

# 3. Diseñar la estructura de la tabla (El Chasis de datos)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS versiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        libro TEXT,
        capitulo INTEGER,
        versiculo INTEGER,
        texto TEXT,
        embedding TEXT
    )
''')
# Limpiamos la tabla por si corremos el script varias veces
cursor.execute('DELETE FROM versiculos') 

# 4. Leer el archivo CSV y procesarlo
print("Leyendo el archivo CSV y generando vectores de IA...")
ruta_csv = 'datos.csv'

with open(ruta_csv, encoding='utf-8') as archivo_csv:
    lector = csv.DictReader(archivo_csv)
    
    for fila in lector:
        libro = fila['Libro']
        cap = fila['Capitulo']
        ver = fila['Versiculo']
        texto = fila['Texto']
        
        # Aquí ocurre la magia: La IA convierte el texto en un vector matemático
        vector = modelo.encode(texto).tolist()
        
        # Guardamos todo en la base de datos
        cursor.execute('''
            INSERT INTO versiculos (libro, capitulo, versiculo, texto, embedding)
            VALUES (?, ?, ?, ?, ?)
        ''', (libro, cap, ver, texto, json.dumps(vector)))
        
        print(f"Procesado: {libro} {cap}:{ver} ✅")

# 5. Guardar cambios y cerrar
conexion.commit()
conexion.close()
print("\n¡Proceso Terminado! Tu base de datos 'biblia_maestra.db' está lista.")