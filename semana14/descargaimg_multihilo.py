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
#     for i, url in enumerate(urls):
#         descargar(url, i)
#     print("Tiempo total:", time.time() - inicio, "segundos")

# if __name__ == "__main__":
#     main()

import requests
import time

# Generamos 10 URLs diferentes
urls = [f"https://picsum.photos/200/300?random={i}" for i in range(50)]

def descargar(url, i):
    print(f"Descargando imagen {i}...")
    img = requests.get(url).content
    with open(f"img{i}.jpg", "wb") as f:
        f.write(img)
    print(f"Imagen {i} completada.")

def main():
    inicio = time.time()
    for i, url in enumerate(urls):
        descargar(url, i)
    fin = time.time()
    print(f"\n⏱️ Tiempo total (secuencial): {round(fin - inicio, 2)} segundos")

if __name__ == "__main__":
    main()
