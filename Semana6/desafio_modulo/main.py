from input import get_int, get_float, get_string

edad = get_int("Edad (0-120): ", "Edad inválida.", 0, 120, 3)
print("Edad ingresada:", edad)

precio = get_float("Precio (0-1000): ", "Precio inválido.", 0, 1000, 3)
print("Precio ingresado:", precio)

nombre = get_string("Nombre (1-20 caracteres): ", "Longitud inválida.", 1, 20, 3)
print("Nombre ingresado:", nombre)

