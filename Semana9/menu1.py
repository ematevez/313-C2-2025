import os, sys, time

# Compatibilidad Windows / Linux para capturar teclas
if os.name == "nt":
    import msvcrt
else:
    import termios, tty

# ------------------ COLORES ------------------
AZUL = "\033[94m"
VERDE = "\033[92m"
ROJO = "\033[91m"
AMARILLO = "\033[93m"
RESET = "\033[0m"

# ------------------ FUNCIONES UTILES ------------------
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def animar_texto(texto, delay=0.03):
    for letra in texto:
        print(letra, end="", flush=True)
        time.sleep(delay)
    print()

def obtener_tecla():
    if os.name == "nt":
        tecla = msvcrt.getch()
        if tecla == b'\xe0':  # tecla especial (flechas)
            tecla = msvcrt.getch()
        return tecla
    else:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        tecla = sys.stdin.read(1)
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return tecla

def barra_progreso(tiempo=2):
    limpiar()
    print("Procesando...\n")
    for i in range(21):
        porcentaje = i * 5
        barra = "█" * i + "-" * (20 - i)
        sys.stdout.write(f"\r[{barra}] {porcentaje}%")
        sys.stdout.flush()
        time.sleep(tiempo / 20)
    print(f"\n{VERDE}✅ Completado.{RESET}\n")
    time.sleep(1)

# ------------------ MENÚ CON FLECHAS ------------------
def menu_flechas(opciones, titulo="=== MENÚ INTERACTIVO ==="):
    seleccion = 0
    while True:
        limpiar()
        animar_texto(f"{AZUL}{titulo}{RESET}\n", delay=0.01)
        for i, opcion in enumerate(opciones):
            prefijo = "👉 " if i == seleccion else "   "
            color = VERDE if i == seleccion else RESET
            print(f"{prefijo}{color}{opcion}{RESET}")
        print("\nUsa ↑ ↓ y ENTER para elegir.")

        tecla = obtener_tecla()
        # Windows flechas: b'H' arriba, b'P' abajo ; Linux: '\x1b[A' arriba, '\x1b[B' abajo
        if tecla in [b'H', '\x1b[A']:
            seleccion = (seleccion - 1) % len(opciones)
        elif tecla in [b'P', '\x1b[B']:
            seleccion = (seleccion + 1) % len(opciones)
        elif tecla in [b'\r', '\n']:
            return seleccion

# ------------------ PROGRAMA PRINCIPAL ------------------
def programa_principal():
    opciones = ["Registrar usuario", "Ver usuarios", "Iniciar sesión", "Simular carga", "Salir"]
    usuarios = {}

    while True:
        eleccion = menu_flechas(opciones)
        limpiar()
        if eleccion == 0:
            nombre = input("Ingrese nombre de usuario: ").strip()
            if nombre in usuarios:
                print(f"{ROJO}El usuario ya existe.{RESET}")
            else:
                usuarios[nombre] = "clave123"  # clave por defecto
                print(f"{VERDE}Usuario registrado correctamente.{RESET}")

        elif eleccion == 1:
            if not usuarios:
                print(f"{AMARILLO}No hay usuarios registrados.{RESET}")
            else:
                print(f"{AZUL}Usuarios registrados:{RESET}")
                for u in usuarios:
                    print(f" - {u}")

        elif eleccion == 2:
            usuario = input("Ingrese nombre de usuario para iniciar sesión: ").strip()
            if usuario in usuarios:
                print(f"{VERDE}Bienvenid@, sesión iniciada correctamente.{RESET}")
            else:
                print(f"{ROJO}Usuario no encontrado.{RESET}")

        elif eleccion == 3:
            barra_progreso(3)  # simulación de carga / proceso

        elif eleccion == 4:
            print(f"{ROJO}Saliendo del programa...{RESET}")
            break

        input("\nPresione Enter para volver al menú...")

# ------------------ EJECUCIÓN ------------------
if __name__ == "__main__":
    programa_principal()
