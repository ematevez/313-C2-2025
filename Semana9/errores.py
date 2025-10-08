# while (True):
#    try:   
#       a = float(input("Introduce un número: "))
#       b = float(input("Introduce otro número: "))
#       print(a + b)
#    except:
#       print("Ha ocurrido un error. Tienes que introducir 2 números.")
#    else:
#       print("La suma se ha realizado correctamente.")
#       break   # Importante romper la iteración si todo ha ido bien.
#    finally:
#       print("Fin del bucle") # Esto se ejecuta siempre.

# while (True):
#     try:
#         n = int(input("Introduce un número: "))  # no transformamos a número
#         print(5/n)
#     except Exception as e:  # guardamos la excepción como una variable e
#         print("Ha ocurrido un error =>", type(e).__name__)

while (True):
    try:
            n = float(input("Introduce un número divisor: "))
            print(5/n)
    except TypeError:
            print("No se puede dividir el número entre una cadena")
    except ValueError:
            print("Debes introducir una cadena que sea un número")
    except ZeroDivisionError:
            print("No se puede dividir por cero, prueba otro número")
    except Exception as e:
    		print("Ha ocurrido un error no previsto", type(e).__name__ )
