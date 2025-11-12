# import threading
# import time

# def tarea(nombre):
#     for i in range(3):
#         print(f"{nombre} ejecutando iteración {i}")
#         time.sleep(1)

# # Crear los hilos
# h1 = threading.Thread(target=tarea, args=("Hilo 1",))
# h2 = threading.Thread(target=tarea, args=("Hilo 2",))

# # Iniciar los hilos
# h1.start()
# h2.start()

# # Esperar que terminen
# h1.join()
# h2.join()

# print("Tareas finalizadas.")

import threading
import time
from random import randint

def tarea(nombre, duracion):
    print(f"[{time.strftime('%H:%M:%S')}] 🔹 {nombre} iniciado (duración estimada: {duracion}s)")
    for i in range(1, 4):
        print(f"[{time.strftime('%H:%M:%S')}] {nombre} ejecutando iteración {i}")
        time.sleep(duracion / 3)
    print(f"[{time.strftime('%H:%M:%S')}] ✅ {nombre} finalizado\n")

# Crear múltiples tareas con diferentes duraciones
tareas = [
    ("Descarga de archivo", randint(3,6)),
    ("Lectura de base de datos", randint(2,5)),
    ("Procesamiento de imagen", randint(4,7)),
    ("Análisis de datos", randint(3,5)),
    ("Generación de reporte", randint(2,4))
]

# Crear los hilos
hilos = [threading.Thread(target=tarea, args=(nombre, dur)) for nombre, dur in tareas]

inicio = time.time()
print(f"🕓 Inicio del programa: {time.strftime('%H:%M:%S')}\n")

# Iniciar todos los hilos
for h in hilos:
    h.start()

# Esperar que todos terminen
for h in hilos:
    h.join()

fin = time.time()
print(f"🏁 Todas las tareas finalizadas en {fin - inicio:.2f} segundos totales.")

