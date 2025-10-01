# Input.py
from validate import validate_number, validate_length


def get_int(mensaje, mensaje_error, minimo, maximo, reintentos):
    """
    Pide un entero por consola validando rango y reintentos.
    Devuelve int o None si no se logra una entrada válida.
    """
    for _ in range(reintentos):
        dato = input(mensaje)
        if dato.isdigit() or (dato.startswith("-") and dato[1:].isdigit()):
            numero = int(dato)
            if validate_number(numero, minimo, maximo):
                return numero
        print(mensaje_error)
    return None


def get_float(mensaje, mensaje_error, minimo, maximo, reintentos):
    """
    Pide un float por consola validando rango y reintentos.
    Devuelve float o None si no se logra una entrada válida.
    """
    for _ in range(reintentos):
        dato = input(mensaje)
        try:
            numero = float(dato)
            if validate_number(numero, minimo, maximo):
                return numero
        except ValueError:
            pass
        print(mensaje_error)
    return None


def get_string(mensaje, mensaje_error, minimo, maximo, reintentos):
    """
    Pide una cadena por consola validando longitud y reintentos.
    Devuelve str o None si no se logra una entrada válida.
    """
    for _ in range(reintentos):
        cadena = input(mensaje)
        if validate_length(cadena, minimo, maximo):
            return cadena
        print(mensaje_error)
    return None
