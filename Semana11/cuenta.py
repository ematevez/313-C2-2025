import cv2
import mediapipe as mp

# --- URL de tu cámara IP ---
# url = "http://192.168.10.157:8080/video"

url =  "rtsp://admin:amdin@192.168.10.131:554/Streaming/Channels/104"
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("❌ No se pudo conectar con la cámara IP.")
    exit()

# --- Inicializar MediaPipe Hands ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

print("✅ Cámara conectada. Mostrá la mano frente a la cámara. Presioná 'q' para salir.")

# --- Bucle principal ---
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ No se pudo leer el frame.")
        break

    frame = cv2.flip(frame, 1)  # espejo para comodidad
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detección de manos
    results = hands.process(rgb_frame)

    count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibuja la mano detectada
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Lista de landmarks
            lm = hand_landmarks.landmark

            # Coordenadas Y de los puntos importantes
            finger_tips = [4, 8, 12, 16, 20]  # pulgar, índice, medio, anular, meñique
            finger_pips = [3, 6, 10, 14, 18]

            fingers = []

            # --- Pulgar (comparación en X por orientación diferente) ---
            if lm[finger_tips[0]].x < lm[finger_pips[0]].x:
                fingers.append(1)
            else:
                fingers.append(0)

            # --- Resto de dedos (comparación en Y) ---
            for tip, pip in zip(finger_tips[1:], finger_pips[1:]):
                if lm[tip].y < lm[pip].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            count = sum(fingers)

            # Mostrar número en pantalla
            cv2.putText(frame, f"Dedos: {count}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow("Contador de dedos - IP Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
