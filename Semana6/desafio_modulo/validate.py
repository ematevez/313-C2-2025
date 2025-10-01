# Validate.py

def validate_number(valor, minimo, maximo):
    """
    Devuelve True si valor está entre [minimo, maximo], False en caso contrario.
    """
    try:
        numero = float(valor)
        return minimo <= numero <= maximo
    except ValueError:
        return False


def validate_length(cadena, minimo, maximo):
    """
    Devuelve True si la longitud de la cadena está entre [minimo, maximo].
    """
    return minimo <= len(cadena) <= maximo
