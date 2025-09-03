# Ejemplos de estructuras
frutas = ["manzana", "banana", "pera"]       # list
coordenadas = (10, 20, 30)                   # tuple
numeros = {1, 2, 3, 2, 3}                    # set
colores = frozenset(["rojo", "verde", "azul", "rojo"])  # frozenset
persona = {"nombre": "Ana", "edad": 25}      # dict
palabra = "Python"                           # str

while True:
    print("\n=== MENÚ DE ITERADORES ===")
    print("1. Mostrar lista (frutas)")
    print("2. Mostrar tupla (coordenadas)")
    print("3. Mostrar set (números)")
    print("4. Mostrar frozenset (colores)")
    print("5. Mostrar diccionario (persona)")
    print("6. Mostrar string (palabra)")
    print("0. Salir")

    opcion = input("Elige una opción: ")

    match opcion:
        case "1":
            it = iter(frutas) # no esta en la catedra pero lo puedo leer sin ofender
            print("Frutas:")
        case "2":
           
            print("Coordenadas:")
           
        case "3":
        
            print("Números:")
            

        case "4":
    
            print("Colores:")
            
        case "5":
            print("Diccionario persona (clave: valor):")
            
        case "6":
          
            print("Letras en la palabra:")
           

        case "0":
            print("👋 Saliendo del programa...")
            break

        case _:
            print("❌ Opción inválida, intenta de nuevo.")
