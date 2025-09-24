import random

# Lista de posibles claves
claves = ["python", "lis", "orden", "frutass"]

clave_secreta = random.choice(claves)   # elige una al azar

print("Juego: Adivina la clave secreta.")
print(f"Pista: tiene {len(clave_secreta)} letras.")

while True:
    intento = input("Escribí tu intento: ").strip().lower()
    if intento == clave_secreta:
        print("¡Correcto! La clave era:", clave_secreta)
        break
    else:
        print("No es esa. Probá de nuevo.")
