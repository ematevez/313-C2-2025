"""
AI Training Arena - versión completa
- Control por nariz (MediaPipe face mesh)
- Disparo por doble parpadeo
- Minijuego (jugador, balas, enemigos, vidas, puntos, escudo, dificultad)
- Chat con Ollama (en hilo, respuestas truncadas y limpiadas)
- Panel derecho con historial, input y botones predefinidos
"""

import pygame
import random
import sys
import cv2
import mediapipe as mp
import numpy as np
import time
import threading
import requests
import string
import json  # ✅ necesario para leer las líneas NDJSON

# --------------------------
# CONFIG: Ollama / modelos
# --------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:3b"   # ✅ modelo que ya tenés instalado
MAX_RESPONSE_CHARS = 300       # límite de texto

# Reducir timeout de requests para evitar bloqueos
OLLAMA_TIMEOUT = 8

# --------------------------
# MEDIA PIPE (face mesh)
# --------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

# --------------------------
# PYGAME init
# --------------------------
pygame.init()
ANCHO, ALTO = 1100, 600
GAME_WIDTH = 700
CHAT_WIDTH = ANCHO - GAME_WIDTH
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("AI Training Arena - Control + Qwen")

# colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (40, 40, 40)
VERDE = (0, 200, 0)
ROJO = (200, 0, 0)
AZUL = (0, 120, 255)
AMARILLO = (240, 200, 0)

fuente = pygame.font.SysFont(None, 20)
fuente_titulo = pygame.font.SysFont(None, 24, bold=True)

# --------------------------
# JUEGO: variables y funciones
# --------------------------
jugador = pygame.Rect(50, ALTO//2 - 25, 50, 50)
balas = []
enemigos = []
vel_bala = 10
vel_enemigo = 3
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1400)

vidas = 3
puntos = 0

tiene_escudo = False
escudo_fin = 0.0
dificultad_mul = 1.0

def disparar(x, y):
    bala = pygame.Rect(x + jugador.width, y + jugador.height//2 - 4, 12, 6)
    balas.append(bala)

def crear_enemigo():
    y = random.randint(0, ALTO - 40)
    enemigo = pygame.Rect(GAME_WIDTH - 40, y, 40, 40)
    enemigos.append(enemigo)

def aplicar_comando_desde_texto(texto):
    global tiene_escudo, escudo_fin, vidas, dificultad_mul, vel_enemigo, puntos

    txt = texto.lower()
    if "escudo" in txt or "shield" in txt:
        tiene_escudo = True
        escudo_fin = time.time() + 8.0
        return "Escudo activado 8s"
    if "curar" in txt or "vida" in txt or "heal" in txt or "regenerar" in txt:
        vidas += 1
        return "Vida +1"
    if "aumenta" in txt or "dificultad" in txt or "difícil" in txt or "hard" in txt:
        dificultad_mul *= 1.3
        return "Dificultad aumentada"
    if "bajar dificultad" in txt or "fácil" in txt or "easy" in txt:
        dificultad_mul = max(0.6, dificultad_mul / 1.3)
        return "Dificultad reducida"
    if "reset" in txt or "reiniciar" in txt:
        dificultad_mul = 1.0
        vidas = 3
        puntos = 0
        return "Juego reiniciado (valores por defecto)"
    if "puntos" in txt or "score" in txt:
        puntos += 50
        return "+50 puntos (bonus IA)"
    return None

# --------------------------
# CHAT: estructura
# --------------------------
chat_history = []
chat_lock = threading.Lock()
pending_model_calls = 0

def append_chat(author, text):
    with chat_lock:
        chat_history.append((author, text))
        if len(chat_history) > 200:
            chat_history.pop(0)

def clean_model_text(s, max_chars=MAX_RESPONSE_CHARS):
    if not isinstance(s, str):
        s = str(s)
    printable = set(string.printable)
    s = ''.join(ch for ch in s if ch in printable)
    s = s.replace('\r', '\n')
    while '\n\n' in s:
        s = s.replace('\n\n', '\n')
    s = s.strip()
    if len(s) > max_chars:
        s = s[:max_chars].rsplit(' ', 1)[0] + "..."
    return s

# ✅ NUEVA VERSIÓN DE ESTA FUNCIÓN
def consultar_ollama_async(prompt, model=DEFAULT_MODEL):
    """
    Ejecutar en hilo. Envía prompt a Ollama y agrega la respuesta al chat.
    Lee el stream NDJSON correctamente.
    """
    global pending_model_calls
    pending_model_calls += 1
    append_chat("Tú", prompt)

    try:
        payload = {"model": model, "prompt": prompt, "stream": True, "max_tokens": 256}
        r = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT, stream=True)

        if r.status_code == 200:
            text_parts = []
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if "response" in data and data["response"]:
                        text_parts.append(data["response"])
                    if data.get("done"):
                        break
                except Exception:
                    continue
            text = "".join(text_parts)
            text = clean_model_text(text, MAX_RESPONSE_CHARS)
            append_chat("Ollie", text)

            cmd_res = aplicar_comando_desde_texto(text)
            if cmd_res:
                append_chat("Sistema", f"Comando aplicado: {cmd_res}")

        else:
            append_chat("Ollie", f"[ERROR: status {r.status_code}] {clean_model_text(r.text,200)}")
    except Exception as e:
        append_chat("Ollie", f"[ERROR conexión] {repr(e)}")
    finally:
        pending_model_calls -= 1

# --------------------------
# Entrada de texto (UI)
# --------------------------
input_text = ""
input_active = True

# --------------------------
# Botones rápidos
# --------------------------
botones_accion = [
    ("Escudo", "Activar escudo por 8 segundos"),
    ("Curar", "Recuperar una vida"),
    ("Dificultad ↑", "Aumentar dificultad"),
    ("Dificultad ↓", "Bajar dificultad"),
    ("Reset", "Reiniciar el juego"),
]
botones_rect = []
boton_altura = 34
boton_sep = 8
for i, (nombre, _) in enumerate(botones_accion):
    y = 60 + i * (boton_altura + boton_sep)
    botones_rect.append(pygame.Rect(GAME_WIDTH + 12, y, CHAT_WIDTH - 24, boton_altura))

# --------------------------
# MEDIAPIPE: utilidades de parpadeo
# --------------------------
last_blink_time = 0
double_blink_delay = 0.5

def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def eye_aspect_ratio(eye_landmarks):
    v1 = euclidean_distance(eye_landmarks[1], eye_landmarks[5])
    v2 = euclidean_distance(eye_landmarks[2], eye_landmarks[4])
    h = euclidean_distance(eye_landmarks[0], eye_landmarks[3])
    if h == 0:
        return 1.0
    return (v1 + v2) / (2.0 * h)

# --------------------------
# BUCLE PRINCIPAL
# --------------------------
reloj = pygame.time.Clock()
running = True
preview_surf = None

while running:
    ret, frame = cap.read()
    if not ret:
        frame = None
    else:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        h_cam, w_cam, _ = frame.shape

        disparo = False
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                lm = face_landmarks.landmark
                nose = (int(lm[1].x * w_cam), int(lm[1].y * h_cam))
                jugador.x = int((nose[0] / w_cam) * (GAME_WIDTH - jugador.width))
                jugador.y = int((nose[1] / h_cam) * (ALTO - jugador.height))

                right_eye_idx = [33, 160, 158, 133, 153, 144]
                left_eye_idx = [362, 385, 387, 263, 373, 380]
                right_eye = [(int(lm[i].x * w_cam), int(lm[i].y * h_cam)) for i in right_eye_idx]
                left_eye = [(int(lm[i].x * w_cam), int(lm[i].y * h_cam)) for i in left_eye_idx]
                ear = (eye_aspect_ratio(right_eye) + eye_aspect_ratio(left_eye)) / 2.0
                if ear < 0.20:
                    if time.time() - last_blink_time < double_blink_delay:
                        disparo = True
                    last_blink_time = time.time()

        try:
            small = cv2.resize(frame, (int(GAME_WIDTH*0.35), int(ALTO*0.35)))
            small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
            preview_surf = pygame.surfarray.make_surface(np.rot90(small))
        except Exception:
            preview_surf = None

    # eventos pygame
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == SPAWN_EVENT:
            crear_enemigo()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif evento.key == pygame.K_RETURN:
                if input_text.strip():
                    threading.Thread(target=consultar_ollama_async, args=(input_text.strip(), DEFAULT_MODEL), daemon=True).start()
                    input_text = ""
            else:
                if evento.unicode:
                    input_text += evento.unicode
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = evento.pos
            for i, rect in enumerate(botones_rect):
                if rect.collidepoint(mx, my):
                    nombre, texto_cmd = botones_accion[i]
                    append_chat("Tú", nombre)
                    resultado = aplicar_comando_desde_texto(texto_cmd)
                    if resultado:
                        append_chat("Sistema", resultado)

    if 'disparo' in locals() and disparo:
        disparar(jugador.x, jugador.y)

    for bala in balas[:]:
        bala.x += vel_bala
        if bala.x > GAME_WIDTH:
            balas.remove(bala)
    vel_en = vel_enemigo * dificultad_mul
    for enemigo in enemigos[:]:
        enemigo.x -= vel_en
        if enemigo.x < -50:
            enemigos.remove(enemigo)

    for bala in balas[:]:
        for enemigo in enemigos[:]:
            if bala.colliderect(enemigo):
                balas.remove(bala)
                enemigos.remove(enemigo)
                puntos += 10
                break

    for enemigo in enemigos[:]:
        if jugador.colliderect(enemigo):
            if tiene_escudo:
                enemigos.remove(enemigo)
                append_chat("Sistema", "Escudo protegió al jugador")
            else:
                enemigos.remove(enemigo)
                vidas -= 1
                append_chat("Sistema", f"Has sido golpeado. Vidas: {vidas}")
                if vidas <= 0:
                    append_chat("Sistema", "GAME OVER")
                    running = False

    if tiene_escudo and time.time() > escudo_fin:
        tiene_escudo = False
        append_chat("Sistema", "Escudo finalizado")

    ventana.fill(GRIS)
    juego_area = pygame.Rect(0, 0, GAME_WIDTH, ALTO)
    pygame.draw.rect(ventana, (20,20,20), juego_area)

    color_j = VERDE if not tiene_escudo else AMARILLO
    pygame.draw.rect(ventana, color_j, jugador)
    for b in balas:
        pygame.draw.rect(ventana, BLANCO, b)
    for e in enemigos:
        pygame.draw.rect(ventana, ROJO, e)

    hud = fuente.render(f"Vidas: {vidas}   Puntos: {puntos}   Dificultad: x{dificultad_mul:.2f}", True, BLANCO)
    ventana.blit(hud, (10, 10))

    if preview_surf is not None:
        ventana.blit(preview_surf, (GAME_WIDTH - preview_surf.get_width() - 8, ALTO - preview_surf.get_height() - 8))

    chat_rect = pygame.Rect(GAME_WIDTH, 0, CHAT_WIDTH, ALTO)
    pygame.draw.rect(ventana, (30,30,30), chat_rect)
    ventana.blit(fuente_titulo.render("CHAT (Ollama Qwen)", True, BLANCO), (GAME_WIDTH + 10, 8))

    mx, my = pygame.mouse.get_pos()
    for i, (nombre, texto_cmd) in enumerate(botones_accion):
        rect = botones_rect[i]
        hover = rect.collidepoint(mx, my)
        color = (70, 70, 70) if not hover else (100, 100, 100)
        pygame.draw.rect(ventana, color, rect, border_radius=6)
        ventana.blit(fuente.render(nombre, True, BLANCO), (rect.x + 8, rect.y + 8))

    with chat_lock:
        y = 60 + len(botones_accion)*(boton_altura+boton_sep) + 8
        max_lines = 12
        recent = chat_history[-max_lines:]
        for author, text in recent:
            color = AZUL if author == "Tú" else (200,200,200) if author == "Ollie" else (150, 255, 150)
            lines = [text[i:i+40] for i in range(0, len(text), 40)]
            for ln in lines:
                ventana.blit(fuente.render(f"{author}: {ln}", True, color), (GAME_WIDTH + 10, y))
                y += 16
            y += 4

    input_box = pygame.Rect(GAME_WIDTH + 10, ALTO - 60, CHAT_WIDTH - 20, 40)
    pygame.draw.rect(ventana, (50,50,50), input_box, border_radius=6)
    txt_show = input_text if input_text else "Escribí tu mensaje y presioná Enter..."
    color_hint = (180,180,180) if not input_text else BLANCO
    ventana.blit(fuente.render(txt_show, True, color_hint), (input_box.x + 8, input_box.y + 10))

    status = "Enviando..." if pending_model_calls > 0 else "Listo"
    ventana.blit(fuente.render(f"Estado: {status}", True, BLANCO), (GAME_WIDTH + 10, ALTO - 90))

    pygame.display.flip()
    reloj.tick(30)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
