# Crear una función que le solicite al usuario el ingreso de un número entero y lo retorne.
def pedir_entero():
        numero = int(input("Ingresa un numero entero: "))
        return numero
num = pedir_entero()
print(f"Ingresaste el numero {num}")
# =====================================================================================
# Crear una función que le solicite al usuario el ingreso de un número flotante y lo retorne.
def pedir_flotante():
        numero = float(input("Ingresa un numero flotante: "))
        return numero
num = pedir_flotante()
print(f"Ingresaste el numero flotante {num}")
# =====================================================================================
# Crear una función que le solicite al usuario el ingreso de una cadena y la retorne. 
def cadena():
    texto = input("ingrese un texto: ")
    return texto
texto = cadena()
print(f"Ingresaste el texto {texto}") 
# =====================================================================================
# Escribir una función que calcule el área de un rectángulo. La función recibe la base y la altura y retorna el área. 
def rectangulo(base: float, altura:float) -> float:
    return base * altura

base = float(input("ingrese el valor de la base: "))
altura = float(input("ingrese el valor de la altura: "))

area = rectangulo(base, altura)
print(f"el area seleccionada del rectángulo es de {area}")
# =====================================================================================
# Escribe una función que calcule el área de un círculo. La función debe recibir el radio como parámetro y devolver el área.
import math
def circulo_area():
    radio = float(input("ingrese el radio del circulo: "))
    area = math.pi * radio ** 2 #math.pi es una constante que basicamente representa todo el valor de pi
    return area
area = circulo_area()
print(f"el area de su circulo es: {area}")
# =====================================================================================
# Crea una función que verifique si un número dado es par o impar. La función debe imprimir un mensaje indicando si el número es par o impar.
def p_i(numero_a_verificar):
    if numero_a_verificar % 2 == 0:
        return print(f'el numero que usted ingreso es par')
    else:
        return print (f'el numero que usted ingreso es impar')
num = int(input("ingrese un numero: "))
p_i(num)            
# =====================================================================================
# Crea una función que verifique si un número dado es par o impar. La función retorna True si el número es par, False en caso contrario.
def p_i(numero_t_f):
    if numero_t_f % 2 == 0:
        return True
    else:
        return False
num = int(input('ingrese un numero:'))
p_i(num)
# =====================================================================================
# Define una función que encuentre el máximo de tres números. La función debe aceptar tres argumentos y devolver el número más grande.
def max(num1, num2, num3):
    if num1 > num2 > num3:
        return num1
    elif num2 > num1 > num3:
        return num2
    else:
        return num3
num1 = int(input('ingrese el primer numero: '))
num2 = int(input('ingrese el segundo numero: '))
num3 = int(input('ingrese el tercer numero: '))
mayor = max(num1, num2, num3)
print(f'el numero mas grande es: {mayor}')
# =====================================================================================
# Diseña una función que calcule la potencia de un número. La función debe recibir la base y el exponente como argumentos y devolver el resultado.
print("Para calcular una potencia Ingrese: Base y Exponente")
def potencia():
        base = int(input("Ingrese la Base: "))
        exponente = int(input("Ingrese el exponente: "))
        return base**exponente
resultado = potencia()
print(f"Resultado: {resultado}")
# =====================================================================================
# Crear una función que reciba un número y retorne True si el número es primo, False en caso contrario.
def es_primo(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
# =====================================================================================
# Crear una función que (utilizando el algoritmo del ejercicio de la guia de for), muestre todos los números primos comprendidos entre entre la unidad y un número ingresado como parámetro. La función retorna la cantidad de números primos encontrados. Modularizar todo lo posible.
def primo(num_p): #trato de que salga...
     contador = 0
     for numero in range(1, num_p +1):
          if num_p % numero == 0:
               contador += 1
               if contador == 2: True
               else: False

        

num_p = int(input('ingrese un numero'))
primo(num_p)
print(f'la cantidad de numeros primos encontrados es: {primo(num_p)}')

# =====================================================================================
# Crear una función que imprima la tabla de multiplicar de un número recibido como parámetro. La función debe aceptar parámetros opcionales (inicio y fin) para definir el rango de multiplicación. Por defecto es del 1 al 10.

def tabla_multiplicar(numero, inicio=1, fin=10):
    print(f"Tabla de multiplicar del {numero}:")
    print("-" * 25)
    
    for i in range(inicio, fin + 1):
        resultado = numero * i
        print(f"{numero} x {i} = {resultado}")

# Ejemplos de uso:
print("=== EJEMPLO 1: Tabla básica (1 al 10) ===")
tabla_multiplicar(5)

print("\n=== EJEMPLO 2: Tabla personalizada (3 al 10) ===")
tabla_multiplicar(3, 3)

print("\n=== EJEMPLO 3: Tabla extendida (1 al 15) ===")
tabla_multiplicar(2, 1, 15)

# Solicitar al usuario
print("\n" + "="*40)
numero = int(input("Ingresa un número: "))

# Preguntar si quiere rango personalizado
opcion = input("¿Quieres usar rango personalizado? (s/n): ").lower()

if opcion == 's':
    inicio = int(input("Desde qué número: "))
    fin = int(input("Hasta qué número: "))
    tabla_multiplicar(numero, inicio, fin)
else:
    tabla_multiplicar(numero)

# =====================================================================================
# Mejorar las funciones del punto 1, 2 y 3 para hacerlas reutilizables. Agregar validaciones.

# =====================================================================================

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
