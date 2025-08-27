
import math
import os
import time

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def sumar(a, b):
  return a + b

def restar(a, b):
  return a - b

def dividir(a, b):
  if b == 0:
    return "Error: División por cero"
  return a / b

def seno(a):
  return math.sin(math.radians(a))

def coseno(a):
  return math.cos(math.radians(a))

def dibujar_grafica(funcion, nombre_funcion):
    """Dibuja una aproximación de la función en la consola."""
    maximo = 1.0
    minimo = -1.0
    ancho = 40  # Ajusta el ancho de la gráfica
    for y in range(int(minimo * 10), int(maximo * 10) + 1):
        linea = ""
        for x in range(ancho):
            valor_x = (x / ancho) * 360 - 180  # Ajusta el rango de x
            valor_y = funcion(valor_x)
            if (y / 10) <= valor_y < ((y + 1) / 10):  #Compara rangos para dibujar punto
                linea += "*"
            else:
                linea += " "
        print(linea)
    print(f"Gráfica de {nombre_funcion}")


def pantalla_inicio():
    limpiar_pantalla()
    print("\033[92m  _.--""--._                     \033[0m")
    print("\033[92m /         \\                    \033[0m")
    print("\033[92m|  O   O   |   CALCULADORA     \033[0m")
    print("\033[92m \\     _    /                    \033[0m")
    print("\033[92m  `-----'                      \033[0m")
    print("\033[91m-----------------------------------\033[0m")
    time.sleep(2)  # Esperar 2 segundos
    limpiar_pantalla()


while True:
  pantalla_inicio()
  print("\033[91m1. \033[0mSumar")
  print("\033[92m2. \033[0mRestar")
  print("\033[91m3. \033[0mDividir")
  print("\033[92m4. \033[0mSeno")
  print("\033[91m5. \033[0mCoseno")
  print("\033[92m6. \033[0mSalir")

  opcion = input("Selecciona una operación (1-6): ")

  try:
    opcion = int(opcion)
    if opcion == 1:
      a = float(input("Primer número: "))
      b = float(input("Segundo número: "))
      print("Resultado:", sumar(a, b))
    elif opcion == 2:
      a = float(input("Primer número: "))
      b = float(input("Segundo número: "))
      print("Resultado:", restar(a, b))
    elif opcion == 3:
      a = float(input("Primer número: "))
      b = float(input("Segundo número: "))
      print("Resultado:", dividir(a, b))
    elif opcion == 4:
      dibujar_grafica(seno, "Seno")
    elif opcion == 5:
      dibujar_grafica(coseno, "Coseno")
    elif opcion == 6:
      break
    else:
      print("Opción inválida")
  except ValueError:
    print("Entrada inválida. Por favor, ingresa un número.")

  input("Presiona Enter para continuar...") #Pausa antes de limpiar la pantalla
  limpiar_pantalla()
