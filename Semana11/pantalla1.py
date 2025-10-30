import cv2
import mediapipe as mp
import numpy as np

# Inicialización
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Captura de cámara
cap = cv2.VideoCapture(0)

# Imagen auxiliar para dibujar
imAux = None

# Paleta de colores (x1, y1, x2, y2, color BGR)
palette = [
    (20, 10, 80, 60, (0, 0, 255)),    # Rojo
    (90, 10, 150, 60, (0, 255, 0)),   # Verde
    (160, 10, 220, 60, (255, 0, 0)),  # Azul
    (230, 10, 290, 60, (0, 255, 255)),# Amarillo
    (300, 10, 360, 60, (255, 255, 255)), # Blanco
]

color = (255, 0, 0)
grosor = 6
drawing = False
prev_point = None

def draw_palette(frame):
    for (x1, y1, x2, y2, c) in palette:
        cv2.rectangle(frame, (x1, y1), (x2, y2), c, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 50, 50), 2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    if imAux is None:
        imAux = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    draw_palette(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, _ = frame.shape

            # Coordenadas de los dedos
            coords = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]

            # Dedo índice y medio
            x_index, y_index = coords[8]
            x_middle, y_middle = coords[12]

            # Detección de dedos levantados
            fingers_up = [coords[i][1] < coords[i-2][1] for i in [8, 12, 16, 20]]

            # Modo selección (índice y medio levantados)
            if fingers_up[0] and fingers_up[1]:
                prev_point = None
                drawing = False
                for (x1, y1, x2, y2, c) in palette:
                    if x1 < x_index < x2 and y1 < y_index < y2:
                        color = c
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 3)
            # Modo dibujo (solo índice levantado)
            elif fingers_up[0] and not fingers_up[1]:
                if prev_point is None:
                    prev_point = (x_index, y_index)
                cv2.line(imAux, prev_point, (x_index, y_index), color, grosor)
                prev_point = (x_index, y_index)
            else:
                prev_point = None

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Combinar dibujo con la cámara
    frame = cv2.add(frame, imAux)
    cv2.putText(frame, "Presiona 'c' para limpiar | 'ESC' para salir", (10, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1, cv2.LINE_AA)
    cv2.imshow("Pintar con el dedo", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('c'):
        imAux = np.zeros_like(frame)
    elif k == 27:
        break

cap.release()
cv2.destroyAllWindows()
