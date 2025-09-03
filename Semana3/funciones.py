# Funcion basica sin parametros

# Funcion simple sin parametros
def saludar():
    print("Hola, bienvenido a la programacion en Python!")
    
# Funcion con 1 parametro
def saludar_param(nombre):
    print(f"Hola, {nombre}, bienvenido a la programacion en Python!")
    
#Funcion que retorna un valor
def sumar(a, b):
    return a + b

#Funcion con valor por defecto    
def presentar(nombre, edad=30):
    print(f"Me llamo {nombre} y tengo {edad} años.")
    
#Funcion que retorna varios valores
def operaciones(num1, num2):
    suma = num1 + num2
    resta = num1 - num2
    return suma, resta
    
#Funcion con *args lo toma como una lista dependiendo la cantidad que se pasen
def sumar_varios(*args):
    resu = 0
    for x in args:
        resu = x + resu
    return resu

#Funcio dentro de una funcion
def funcion_externa():
    print("Esta es la funcion externa.")
    
    def funcion_interna():
        print("Esta es la funcion interna.")
    
    funcion_interna()


# ========================================================= 
# Llamada a la funcion
# saludar()
# saludar_param("Juan")

# resultado = sumar(3, 5)
# print(f"La suma es: {resultado}")

# presentar("Emanuel", 25)
# presentar("Ana")

# suma, resta = operaciones(10, 4)
# print(f"Suma: {suma}, Resta: {resta}")

# print(sumar_varios(1, 2, 3, 4, 5))
# print(sumar_varios(10, 20, 50, 3.3))

# funcion_externa()
# funcion_interna() es un funcion local y no se puede llamar desde aqui

"""
Nivel Básico
1. Función que saluda a una persona

Enunciado:
Escribí una función que reciba un nombre y muestre un saludo personalizado. el nombre lo ingresa por consola
""" 
# def saludo(nombre):
#     print("Hola " + nombre)

# nombre = input("Ingresa tu nombre: ")

# saludo(nombre)

# =========================================================

# def saludar (persona):
#     print(f"Hola {persona}")

# nombre = input ("ingrese su nombre: ")

# saludar(nombre)

# ==========================================================
# def saludar_persona(nombre: str) -> None:
#     """Doc"""
#     print(f"Hola, {nombre}! :) Bienvenido/a.")
#     return

# saludar_persona(input("Ingrese su nombre: "))

# ==========================================================
# def saludar(nombre):
#     print(f"Hola, {nombre}")
# nombre = input("Ingrese su nombre: ")

# saludar(nombre)
"""
Enunciado:
Escribí una función que reciba base y altura, y devuelva el área.
Datos por consola un argumento por defecto =10
"""
# #Todo###################################################
# def calcular_area(base: float = 10, altura: float = 10) -> float:
#     area = base * altura
#     print(f"El área del rectángulo es: {area}")
#     return 

# base = float(input("Ingrese la base del rectángulo (por defecto 10): "))
# altura = float(input("Ingrese la altura del rectángulo (por defecto 10): "))
# #Todo###################################################

# calcular_area(base, altura) # Valores ingresados 
# calcular_area()  # valores predeterminados con valores por defecto :p
# #Todo###################################################
# =============================================================
# def devolver_Area_BaseX_Altura( base = 10, altura = 10):
#     return base * altura


# baseInput = int(input("Por favor ingrese un numero para la base: "))
# alturaInput = int(input("Por favor ingrese un numero para la altura: "))

# print(f"El area calculado es {devolver_Area_BaseX_Altura(baseInput,alturaInput)}")

# =============================================================
# def calculo_area(base=10, altura=10):
#     return base * altura 

# base = float(input("Ingrese la base del triángulo (por defecto 10): ")) 
# altura = float(input("Ingrese la altura del triángulo (por defecto 10): "))

# print(f"El área del triángulo es: {calculo_area(base, altura)}")
# ============================================================

# def calcular_area(base=10, altura=10):
#     return base * altura

# base = int(input("Ingrese la base: "))
# altura = int(input("Ingrese la altura: "))  
# area = calcular_area(base, altura)            

# print(f"El área del rectángulo es: {area}")

# =============================================================
# def devolverArea(base=10, altura=10):
#     area=(base*altura)/2
#     return area

# base=int(input("Ingresar Base: "))
# altura=int(input("Ingresar Altura: "))

# print(f"Tu Area es de: {devolverArea(base, altura)} (por defecto =10)")
# =============================================================
# def calculo (base = 10, altura = 0):
#     return (base * altura) / 2

# altura = float(input("Ingresa la altura del triangulo: "))

# resultado = calculo(altura = altura)

# print(f"Base: 10, Altura: {altura}")
# print(f"El área del triángulo es: {resultado}")

# ============================================================
"""Nivel Intermedio
Función que devuelva suma, resta y multiplicación

Enunciado:
Escribí una función que reciba dos números y devuelva los tres resultados: suma, resta y multiplicación."""

# def operaciones(a, b):
#     suma = a + b
#     resta = a - b
#     multiplicacion = a * b
#     return suma, resta, multiplicacion

# numero1 = int(input("Ingrese el primer número: "))
# numero2 = int(input("Ingrese el segundo número: "))
# suma, resta, multiplicacion = operaciones(numero1, numero2)

# print(f"La suma es: {suma}")
# print(f"La resta es: {resta}")
# print(f"La multiplicación es: {multiplicacion}")

####################################################################
# def operaciones_basicas(numero_1: float, numero_2: float) -> None:
# #!Documentacion    
#     suma = numero_1 + numero_2
#     resta = numero_1 - numero_2
#     multiplicacion = numero_1 * numero_2
    
#     print(f"los operadores son: {numero_1} y {numero_2}")
#     print(f"La suma es: {suma}")
#     print(f"La resta es: {resta}")
#     print(f"La multiplicación es: {multiplicacion}")
#     return
# ###Todo###################################################
# #?Entrada
# numero_ingresado_1 = float(input("Ingrese el primer número: "))
# numero_ingresado_2 = float(input("Ingrese el segundo número: "))
# resultados = operaciones_basicas(numero_ingresado_1, numero_ingresado_2)


# =============================================================

# def devuelve_Suma_Resta_Multi(numero1,numero2):
#     suma = numero1 + numero2
#     resta = numero1 - numero2
#     multiplicacion = numero1 * numero2
#     return suma,resta,multiplicacion

# primerNumero = int(input("Por favor ingrese un numero entero valido: "))
# segundoNumero = int(input("Por favor ingrese un numero entero valido: "))
# suma1 , resta2 , multiplicacion3 = devuelve_Suma_Resta_Multi(primerNumero,segundoNumero)

# mensaje =\
#     f"""
#     La suma de los numeros es de {suma1}
#     La resta de los numeros es {resta2}
#     La multiplicacion de los numeros es de {multiplicacion3}
#     """

# print(mensaje)

# =============================================================
# def numeros(a,b):
#     suma = a + b
#     resta =a - b
#     multiplicacion = a * b
#     return suma, resta, multiplicacion

# numero1= int(input("ingrese un numero "))
# numero2= int(input("ingrese un numero "))

# suma, resta, multiplicacion = numeros(numero1,numero2)


# print(f"La resta es: {resta}")
# print(f"La multiplicación es: {multiplicacion}")
# print(f"La suma es: {suma}")

# ==============================================================

# def operaciones(numero_1, numero_2):
#     suma = numero_1 + numero_2
#     resta = numero_1 - numero_2
#     multiplicación = numero_1 * numero_2
#     return suma, resta, multiplicación

# numero_1 = float(input("Ingrese un numero: "))
# numero_2 = float(input("Ingrese un segundo numero: "))
# suma, resta, multiplicación = operaciones(numero_1, numero_2)

# print(f"Suma: {suma}")
# print(f"resta: {resta}")
# print(f"multiplicación: {multiplicación}")

# ==============================================================

# def operatoria (num_1, num_2):
#     suma = num_1 + num_2
#     resta = num_1 - num_2
#     multiplicacion = num_1 * num_2

#     return suma,resta,multiplicacion

# numero_1 = float(input("ingrese primer numero a operar: "))
# numero_2 = float(input("ingrese segundo numero a operar: "))

# suma ,resta ,multiplicacion = operatoria(numero_1,numero_2)
# print(f"la suma de sus numeros es : {suma}")
# print(f"la resta de sus numeros es : {resta}")
# print(f"la multiplicacion de sus numeros es : {multiplicacion}")

# =============================================================
# def operacion(num1, num2):
#     suma = num1 + num2
#     resta = num1 - num2
#     multiplicacion = num1 * num2
#     return suma, resta, multiplicacion

# num1 = float(input("Ingrese el primer numero:"))
# num2 = float(input("Ingrese el segundo numero:"))

# suma, resta, multiplicacion = operacion(num1, num2)

# print(f'La suma es: {suma}')
# print(f'La resta es: {resta}')
# print(f'La multiplicacion es: {multiplicacion}')
# =============================================================

# def carcular_operaciones(numero_a,numero_b):
#     suma = numero_a + numero_b
#     resta = numero_a - numero_b
#     multiplicacion = numero_a * numero_b
#     return suma,resta,multiplicacion

# numero_uno = int(input("INGRESA EL PRIMER NUMERO: "))
# numero_dos = int(input("INGRESA EL SEGUNDO NUMERO: "))

# suma,resta,multiplicacion = carcular_operaciones(numero_uno,numero_dos)

# print(f" La suma es igual a: {suma}\n La resta es igual a: {resta}\n La multiplicaicion es: {multiplicacion}")
# =============================================================
# def calculadora(numA, numB):
#     suma=numA+numB
#     resta=numA-numB
#     multiplicacion=numA*numB
#     return(suma,resta,multiplicacion)

# numA=int(input("Colocar un numeroA: "))
# numB=int(input("Colocar un numeroB: "))

# suma,resta,multiplicacion= calculadora(numA,numB)

# print(f"La suma de {numA} + {numB} es: {suma}")
# print(f"La resta de {numA} - {numB} es: {resta}")
# print(f"La multiplicacion de {numA} x {numB} es: {multiplicacion}")

# ============================================================
"""
Enunciado:
Escribí una función que reciba cualquier cantidad de números y los suma los parametros por consola.

Ayuda: pedir al usuario cuantos numeros cargar, luego usar ese valor para iterar"""

# #TODO###############################################################
# def multiplicar_numeros(*args: float) -> None:
#     resultado = 1   # acumulador de cantidad total de la multiplicacion
#     cantidad_numeros = int(input("¿Cuántos números deseas multiplicar? ")) #Cant de ingresos    
    
#     for numero_ingresado in range(cantidad_numeros):
#         numero_ingresado = float(input(f"Ingrese un numero: "))
#         resultado *= numero_ingresado
#     print(f"El resultado de la multiplicación es: {resultado}")
#     return
# #Todo###############################################################

# multiplicar_numeros()
            
# ============================================================
# def sumar_numeros(numeroA):
#     suma = 0
#     for i in range(1,numeroA+1):
#         # si pongo el input dentro del for me va a pedir el numeroA tantas veces como el valor que ingrese
#         suma = suma + i
#     return suma

# numero = int(input("INGRESE LA CANTIDAD DE NUMEROS QUE QUIERE SUMAR: "))

    
# print(sumar_numeros(numero))
# ============================================================
# def multiplicar_numeros():
#     cantidad = int(input("ingrese Cuántos números quiere multiplicar: "))
#     resultado = 1
    
#     for i in range(0,cantidad):
#         numero = float(input(f"Ingresa el número {i + 1}: "))
#         resultado *= numero
    
#     print(f"El resultado de la multiplicación es: {resultado}")

# multiplicar_numeros()
#! EL MEJOR ============================================================
# def multiplicar_numeros(*args):
#     resultado = 1
#     for numero in args:
#         resultado *= numero
#     return resultado

# cantidad_numeros = int(input('Cuantos numeros va a  ingresar?: '))
# numeros = []

# for i in range(cantidad_numeros):
#     num = int(input(f'Ingrese un numero: '))
#     numeros.append(num)

# print(f'La multiplicación de los números ingresados es: {multiplicar_numeros(*numeros)}')
# ============================================================