import os
import sys

# --- compatibilidad Windows / Linux ---
if os.name == "nt":  # Windows
    import msvcrt
    def esperar_tecla():
        print("\nPresione cualquier tecla para continuar...")
        msvcrt.getch()
else:  # Linux o Mac
    import termios
    import tty
    def esperar_tecla():
        print("\nPresione cualquier tecla para continuar...")
        tty.setcbreak(sys.stdin)
        sys.stdin.read(1)

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

# --- MENÚ PRINCIPAL ---
def menu():
    while True:
        limpiar()
        print("=== MENÚ PRINCIPAL ===")
        print("1. Registrar usuario")
        print("2. Ver usuarios")
        print("3. Iniciar sesión")
        print("4. Guardar")
        print("5. Salir")
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            print("Registrando usuario...")
        elif opcion == "2":
            print("Mostrando usuarios...")
        elif opcion == "3":
            print("Iniciando sesión...")
        elif opcion == "4":
            print("Guardando...")
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

        esperar_tecla()  # espera una tecla antes de volver al menú

# Ejecutar menú
menu()
