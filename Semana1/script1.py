# Práctica: Menú con match y submenú con if-elif
# Sin funciones (estilo estructurado) + colores

# Definimos algunos colores usando secuencias de escape ANSI
ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Menú principal
while True:
    print(f"\n{VERDE}=== MENÚ PRINCIPAL ==={RESET}")
    print(f"{AZUL}1. Opción 1")
    print("2. Opción 2")
    print("3. Opción 3")
    print(f"4. Salir{RESET}")
    
    opcion = input(f"{AMARILLO}Seleccione una opción: {RESET}")
    
    match opcion:
        case "1":
            print(f"\n{CYAN}=== SUBMENÚ OPCIÓN 1 ==={RESET}")
            print("a. Subopción A")
            print("b. Subopción B")
            print("c. Volver al menú principal")
            
            subopcion = input(f"{AMARILLO}Seleccione una subopción: {RESET}")
            
            if subopcion == "a":
                print(f"{VERDE}Ejecutando Subopción A...{RESET}")
            elif subopcion == "b":
                print(f"{VERDE}Ejecutando Subopción B...{RESET}")
            elif subopcion == "c":
                print(f"{AZUL}Volviendo al menú principal...{RESET}")
            else:
                print(f"{ROJO}Subopción no válida{RESET}")
                
        case "2":
            print(f"\n{MAGENTA}Ha seleccionado la Opción 2{RESET}")
            print("Esta opción no tiene submenú")
            
        case "3":
            print(f"\n{CYAN}=== SUBMENÚ OPCIÓN 3 ==={RESET}")
            print("x. Subopción X")
            print("y. Subopción Y")
            print("z. Volver")
            
            subopcion = input(f"{AMARILLO}Seleccione una subopción: {RESET}")
            
            if subopcion == "x":
                print(f"{VERDE}Ejecutando Subopción X...{RESET}")
            elif subopcion == "y":
                print(f"{VERDE}Ejecutando Subopción Y...{RESET}")
            elif subopcion == "z":
                print(f"{AZUL}Volviendo al menú principal...{RESET}")
            else:
                print(f"{ROJO}Subopción no válida{RESET}")
                
        case "4":
            print(f"{ROJO}Saliendo del programa...{RESET}")
            break
            
        case _:
            print(f"{ROJO}Opción no válida. Intente nuevamente.{RESET}")