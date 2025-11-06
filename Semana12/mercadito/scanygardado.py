# instalar vcredist_x64.exe
# pip install pyzbar

import cv2
from pyzbar import pyzbar

def leer_codigo_barra_con_camara():
    cap = cv2.VideoCapture(0)
    print("📸 Apuntá el código de barras del producto (ESC para salir)...")
    codigo_detectado = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Detectar códigos de barras
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            # Obtener solo el número del código
            codigo_detectado = barcode.data.decode('utf-8')
            
            # Dibujar un rectángulo alrededor del código
            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Mostrar el código sobre la imagen
            cv2.putText(frame, codigo_detectado, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            print(f"\n✅ Código detectado: {codigo_detectado}")
            break  # Solo toma el primer código detectado

        # Mostrar la cámara en tiempo real
        cv2.imshow("Escaneando código de barras", frame)

        # Presionar ESC para salir
        if cv2.waitKey(1) & 0xFF == 27 or codigo_detectado:
            break

    cap.release()
    cv2.destroyAllWindows()
    return codigo_detectado

if __name__ == "__main__":
    codigo = leer_codigo_barra_con_camara()
    if codigo:
        print(f"\n📦 Código final leído: {codigo}")
    else:
        print("\n🚫 No se detectó ningún código.")
