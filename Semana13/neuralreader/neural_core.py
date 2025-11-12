# neural_core.py
import os
import pickle
import numpy as np
import tensorflow as tf
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pyttsx3

DATA_DIR = "neural_data"
os.makedirs(DATA_DIR, exist_ok=True)
MODEL_PATH = os.path.join(DATA_DIR, "neural_model.keras")
VECTORIZER_PATH = os.path.join(DATA_DIR, "vectorizer.pkl")
TEXTS_PATH = os.path.join(DATA_DIR, "texts.pkl")

engine = pyttsx3.init()

def hablar(texto):
    print(f"🧠 Neurona: {texto}")
    engine.say(texto)
    engine.runAndWait()

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
        return tf.keras.models.load_model(MODEL_PATH)
    else:
        return crear_modelo(vectorizer_dim)

def extraer_texto_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    texto = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return texto

def preprocesar_texto(texto):
    texto = texto.lower()
    texto = "".join(c for c in texto if c.isalpha() or c.isspace())
    return texto

def entrenar_con_pdf(pdf_path):
    texto = preprocesar_texto(extraer_texto_pdf(pdf_path))

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
    model.fit(X, y, epochs=5, verbose=0)

    model.save(MODEL_PATH)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    with open(TEXTS_PATH, "wb") as f:
        pickle.dump(textos, f)

    hablar("Entrenamiento finalizado.")
    return "Entrenamiento completado con éxito."

def responder(pregunta):
    if not os.path.exists(VECTORIZER_PATH):
        return "Aún no tengo conocimiento. Cargá un PDF primero."

    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    with open(TEXTS_PATH, "rb") as f:
        textos = pickle.load(f)

    X = vectorizer.transform(textos).toarray()
    q_vec = vectorizer.transform([pregunta]).toarray()
    similitudes = cosine_similarity(q_vec, X).flatten()

    idx = np.argmax(similitudes)
    respuesta = textos[idx][:300] + "..."
    hablar(respuesta)
    return respuesta
