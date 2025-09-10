def pedir_entero(mensaje="Ingresa un número entero: ", minimo=None, maximo=None):
    while True:
        try:
            num = int(input(mensaje))
            if (minimo is None or num >= minimo) and (maximo is None or num <= maximo):
                return num
            print(f"Número debe estar entre {minimo} y {maximo}")
        except ValueError:
            print("Ingresa un número entero válido")

def pedir_flotante(mensaje="Ingresa un número flotante: ", minimo=None, maximo=None):
    while True:
        try:
            num = float(input(mensaje))
            if (minimo is None or num >= minimo) and (maximo is None or num <= maximo):
                return num
            print(f"Número debe estar entre {minimo} y {maximo}")
        except ValueError:
            print("Ingresa un número flotante válido")

def pedir_cadena(mensaje="Ingresa texto: ", min_len=None, max_len=None, no_vacio=False):
    while True:
        texto = input(mensaje).strip()
        if no_vacio and not texto:
            print("El texto no puede estar vacío")
            continue
        if min_len and len(texto) < min_len:
            print(f"Mínimo {min_len} caracteres")
            continue
        if max_len and len(texto) > max_len:
            print(f"Máximo {max_len} caracteres")
            continue
        return texto




# Ejemplos de uso
if __name__ == "__main__":
    # Uso básico
    num = pedir_entero()
    decimal = pedir_flotante()
    texto = pedir_cadena()
    
    # Con validaciones
    edad = pedir_entero("Edad (0-120): ", 0, 120)
    precio = pedir_flotante("Precio ($1-1000): ", 1, 1000)
    nombre = pedir_cadena("Nombre: ", min_len=2, no_vacio=True)
    
    print(f"Edad: {edad}, Precio: {precio}, Nombre: {nombre}")
