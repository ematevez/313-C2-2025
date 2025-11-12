import threading

contador = 0
lock = threading.Lock()

def incrementar():
    global contador
    for _ in range(100000):
        with lock:
            contador += 1

hilos = [threading.Thread(target=incrementar) for _ in range(5)]
for h in hilos: h.start()
for h in hilos: h.join()

print("Contador final:", contador)
