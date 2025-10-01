def get_int(mensaje:str, mensaje_error:str, minimo:int, maximo:int, reintentos:int) -> int|None:
    for intento in range(reintentos):
        numero_recibido = input(mensaje)
        if validate_number(numero_recibido, minimo, maximo):
            return int(numero_recibido)
        reintentos_restantes = reintentos - intento - 1
        if reintentos_restantes > 0:
            print(f"El numero ingresado no es valido. Le quedan {reintentos_restantes} reintentos")
    print(mensaje_error)
    return None
    
      
def get_string(mensaje:str, mensaje_error:str, minimo:int, maximo:int, reintentos:int) -> str|None:
    for intento in range(reintentos):
        cadena_recibida = input(mensaje)
        if validate_lenght(cadena_recibida, minimo, maximo):
            return str(cadena_recibida)
        reintentos_restantes = reintentos - intento - 1
        if reintentos_restantes > 0:
            print(f"La cadena no es valida. Le quedan {reintentos_restantes} reintos")
    print(mensaje_error)
    return None
    
def get_float(mensaje:str, mensaje_error:str, minimo:int, maximo:int, reintentos:int) -> float|None:
    for intento in range(reintentos):
        numero_recibido = input(mensaje)
        if validate_number(numero_recibido, minimo, maximo):
            return float(numero_recibido)
        reintentos_restantes = reintentos - intento - 1
        if reintentos_restantes > 0:
            print(f"El numero ingresado no es valido. Le quedan {reintentos_restantes} reintentos")
    print(mensaje_error)
    return None
    


def validate_number(valor:str, minimo:int, maximo:int) -> bool:
    try:
        numero = float(valor)
        return minimo <= numero <= maximo
    except ValueError :
        return False

def validate_lenght(valor:str, minimo:int, maximo:int) -> bool:
    if minimo <= len(valor) <= maximo:
        return True

if __name__ == "__main__": # si se ejecuta este archivo se llama a init(). Si se importa el archivo, no se llama a nada
    get_int("Ingrese entero entre 1 y 10: ", "Numero no valido", 1, 10, 3)
    get_float("Ingrese entero entre 1 y 10: ", "Numero no valido", 1, 10, 3)
    get_string("Ingrese una cadena: ", "Cadena no valida", 1, 10, 4)