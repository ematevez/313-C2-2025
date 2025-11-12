# import threading
# import requests
# import time

# urls = [
#     "https://picsum.photos/200/300",
#     "https://picsum.photos/300/300",
#     "https://picsum.photos/400/300",
# ]

# def descargar(url, i):
#     print(f"Iniciando descarga {i}")
#     img = requests.get(url).content
#     with open(f"img{i}.jpg", "wb") as f:
#         f.write(img)
#     print(f"Descarga {i} completada")

# def main():
#     inicio = time.time()
#     hilos = []
#     for i, url in enumerate(urls):
#         hilo = threading.Thread(target=descargar, args=(url, i))
#         hilo.start()
#         hilos.append(hilo)
#     for h in hilos: h.join()
#     print("Tiempo total:", time.time() - inicio, "segundos")

# if __name__ == "__main__":
#     main()
import threading
import requests
import time

# Generamos las mismas 10 URLs
urls = [f"https://picsum.photos/200/300?random={i}" for i in range(50)]

def descargar(url, i):
    print(f"[Hilo {i}] Iniciando descarga...")
    img = requests.get(url).content
    with open(f"img{i}.jpg", "wb") as f:
        f.write(img)
    print(f"[Hilo {i}] Descarga completada.")

def main():
    inicio = time.time()
    hilos = []

    for i, url in enumerate(urls):
        hilo = threading.Thread(target=descargar, args=(url, i))
        hilo.start()
        hilos.append(hilo)

    for h in hilos:
        h.join()

    fin = time.time()
    print(f"\n⏱️ Tiempo total (con hilos): {round(fin - inicio, 2)} segundos")

if __name__ == "__main__":
    main()
