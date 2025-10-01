"""
Sistema de Login en Python
Desarrollar un programa en Python que permita gestionar un sistema de usuarios con las siguientes funcionalidades:

Registrarse: El usuario ingresa nombre, email y contraseña. Los datos se guardan en un archivo usuarios.txt.
Login: El usuario ingresa email y contraseña, y el sistema valida sus datos.
Ver Datos: Mostrar la lista de usuarios registrados en formato tabular.
Salir: Termina la ejecución.

Los datos deben guardarse en un diccionario, y luego persistirse en el archivo usuarios.txt.
El menú debe mostrarse con colores para mayor claridad.
"""
import os
import json
import re
from colorama import Fore, Style, init #TODO<- Es para los colores


#inicializar colorama
init(autoreset=True)

archivo = "usuarios.txt"

#Funciones
def cargar_usuarios()->dict:
    "Cargar usuarios desde el archivo"
    if not os.path.exists(archivo):
        print("No encontre nada")
        return {}
    with open(archivo, "r", encoding="utf-8-sig") as f:
        try:
            print("Lei un json")
            return json.load(f)
        except json.JSONDecodeError:
            print("Error al leer el archivo. El archivo puede estar corrupto.")
            return {}
    
def guardar_usuarios(usuarios:dict)->None:
    "Dar de alta un usuario en el archivo"
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4)
    
def registrarse(usuarios:dict)->None:
    "REGISTRARSE"
    # email = input("Ingrese su email: ").strip().lower()
    while True:
        email = input("Ingrese su email: ").strip().lower()
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            print(Fore.RED + "❌ Email inválido.")
            return
        if email in usuarios:
            print(Fore.RED + "El email ya está registrado.")
            return
        # nombre = input("Ingrese su nombre: ").strip().title()
        while True:
            nombre = input("Ingrese su nombre: ").strip().title()
            if not re.match(r"^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]{2,50}$", nombre):
                print(Fore.RED + "❌ El nombre solo puede contener letras y espacios (2-50 caracteres).")
                continue
            break
                
        while True:
            password = input("🔑 Ingrese su contraseña: ").strip()
            if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@#$%^&+=!]{6,}$", password):
                print(Fore.RED + "❌ La contraseña debe tener al menos 6 caracteres, con letras y números.")
                continue
            break
        
        usuarios[email] = {"nombre": nombre, "password": password}
        guardar_usuarios(usuarios)
        print(Fore.GREEN + "✅ Registro exitoso.")
    
def login(usuarios:dict)->None:
    "INICIO DE SESION"
    email = input("Ingrese su email: ").strip().lower()
    password = input("🔑 Ingrese su contraseña: ").strip()
    if email in usuarios and usuarios[email]["password"] == password:
        print(Fore.GREEN + f"✅ Bienvenido, {usuarios[email]['nombre']}!")
    else:
        print(Fore.RED + "❌ Email o contraseña incorrectos.")
    
def ver_datos(usuarios:dict)->None:
    "VER DATOS"
    if not usuarios:
        print(Fore.YELLOW + "No hay usuarios registrados.")
        return
    print(Fore.MAGENTA + "\n=== Lista de Usuarios Registrados ===")
    print("°-°" * 40)
    for email, datos in usuarios.items():
        print(f"Nombre: {datos['nombre']}, Email: {email}")
    print("°-°" * 40)
    
# ===========MENU============
def menu()->None:
    usuarios = cargar_usuarios()
    while True:
        print(Fore.MAGENTA  + "\n=== Sistema de Login ===")
        print(Fore.CYAN + "1. Registrarse")
        print(Fore.LIGHTBLACK_EX + "2. Login")   
        print(Fore.CYAN + "3. Ver Datos")
        print(Fore.CYAN + "4. Salir")
        print(Fore.CYAN + "5. CARGA DATOS DEBUG")
        opcion = input(Fore.YELLOW + "Seleccione una opción: ")
        if opcion == "1":
            registrarse(usuarios)
        elif opcion == "2":
            login(usuarios)
        elif opcion == "3":
            ver_datos(usuarios)
        elif opcion == "4":
            print(Fore.GREEN + "Saliendo del sistema. ¡Hasta luego!")
            break
        elif opcion == "5":
            cargar_usuarios()
        else:
            print(Fore.RED + "Opción inválida. Intente nuevamente.")
            
#=========MAIN==================
if __name__ == "__main__":
    menu()
    
    
    
    
    
