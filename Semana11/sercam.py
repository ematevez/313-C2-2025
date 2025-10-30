# pip install opencv-python mediapipe


import cv2
import mediapipe as mp

# --- Configuración de la cámara IP Webcam ---
url = "http://192.168.10.157:8080/video"
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("❌ No se pudo conectar con la cámara.")
    exit()

# --- Inicializar MediaPipe Face Detection ---
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Configurar detector de rostros
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

print("✅ Cámara conectada. Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ No se pudo leer el frame. Verifica la conexión.")
        break

    # Convertir el frame a RGB (MediaPipe usa RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar detección facial
    results = face_detection.process(rgb_frame)

    # Dibujar las detecciones
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(frame, detection)

    # Mostrar el video con detección
    cv2.imshow("Detección Facial - IP Webcam", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
