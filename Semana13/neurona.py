# pip install numpy tqdm pyttsx3 fitz pymupdf pdfminer.six torch torchvision  # torch opcional si no querés/tenés GPU
# o si preferís con pip: pip install numpy tqdm pyttsx3 pymupdf pdfminer.six

# neural_reader.py
# ===========================================
# NEURAL READER - Asistente entrenable con libros PDF
# ===========================================
# Autor: Emanuel Tevez
# Descripción: Entrena una neurona con tus libros PDF
# y conversa usando lo aprendido.

import os
import pickle
import numpy as np
import pyttsx3
import tensorflow as tf
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===========================================
# CONFIGURACIÓN Y PERSISTENCIA
# ===========================================
DATA_DIR = "neural_data"
os.makedirs(DATA_DIR, exist_ok=True)
MODEL_PATH = os.path.join(DATA_DIR, "neural_model.keras")
VECTORIZER_PATH = os.path.join(DATA_DIR, "vectorizer.pkl")
TEXTS_PATH = os.path.join(DATA_DIR, "texts.pkl")

engine = pyttsx3.init()

def hablar(texto):
    print(f"\n🧠 Neurona: {texto}")
    engine.say(texto)
    engine.runAndWait()

# ===========================================
# CARGAR O CREAR MODELO
# ===========================================
def crear_modelo(input_dim):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_dim=input_dim),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model

def cargar_modelo(vectorizer_dim):
    if os.path.exists(MODEL_PATH):
        hablar("Modelo cargado desde disco.")
        return tf.keras.models.load_model(MODEL_PATH)
    else:
        hablar("Creando un nuevo modelo neuronal.")
        return crear_modelo(vectorizer_dim)

# ===========================================
# PROCESAMIENTO DE PDF
# ===========================================
def extraer_texto_pdf(pdf_path):
    hablar(f"Leyendo archivo {pdf_path}")
    reader = PdfReader(pdf_path)
    texto = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return texto

def preprocesar_texto(texto):
    texto = texto.lower()
    texto = "".join(c for c in texto if c.isalpha() or c.isspace())
    return texto

# ===========================================
# ENTRENAMIENTO
# ===========================================
def entrenar_con_pdf(pdf_path):
    texto = preprocesar_texto(extraer_texto_pdf(pdf_path))
    hablar("Procesando texto del libro...")
    
    if os.path.exists(VECTORIZER_PATH):
        with open(VECTORIZER_PATH, "rb") as f:
            vectorizer = pickle.load(f)
        with open(TEXTS_PATH, "rb") as f:
            textos = pickle.load(f)
    else:
        vectorizer = TfidfVectorizer(max_features=5000)
        textos = []
    
    textos.append(texto)
    X = vectorizer.fit_transform(textos).toarray()
    y = np.ones((len(textos), 1))
    
    model = cargar_modelo(X.shape[1])
    hablar("Entrenando neurona con el nuevo libro...")
    model.fit(X, y, epochs=5, verbose=1)
    
    model.save(MODEL_PATH)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    with open(TEXTS_PATH, "wb") as f:
        pickle.dump(textos, f)
    
    hablar("Entrenamiento finalizado y guardado.")

# ===========================================
# CONSULTAS Y RESPUESTAS
# ===========================================
def responder(pregunta):
    if not os.path.exists(VECTORIZER_PATH):
        hablar("Aún no tengo conocimiento. Cargá un PDF primero.")
        return
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    with open(TEXTS_PATH, "rb") as f:
        textos = pickle.load(f)
    
    X = vectorizer.transform(textos).toarray()
    q_vec = vectorizer.transform([pregunta]).toarray()
    similitudes = cosine_similarity(q_vec, X).flatten()
    
    idx = np.argmax(similitudes)
    respuesta = textos[idx][:300] + "..."  # recorte del texto más relevante
    hablar(respuesta)

# ===========================================
# INTERFAZ PRINCIPAL
# ===========================================
def menu():
    while True:
        print("\n🧠 NeuralReader - Menú Principal")
        print("1. Cargar nuevo libro PDF y entrenar")
        print("2. Hacer una pregunta al modelo")
        print("3. Salir")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            pdf_path = input("Ruta del PDF: ").strip()
            if os.path.exists(pdf_path):
                entrenar_con_pdf(pdf_path)
            else:
                print("❌ Archivo no encontrado.")
        elif opcion == "2":
            pregunta = input("Tu pregunta: ")
            responder(pregunta)
        elif opcion == "3":
            hablar("Cerrando el sistema neuronal. Hasta luego.")
            break
        else:
            print("Opción no válida.")

# ===========================================
# EJECUCIÓN PRINCIPAL
# ===========================================
if __name__ == "__main__":
    hablar("Inicializando sistema NeuralReader persistente...")
    menu()
