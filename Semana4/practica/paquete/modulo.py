
# practicas_semana4.py
"""
Prácticas – Semana 4: Funciones en Python
Incluye funciones básicas, parámetros, variables globales, paso por valor/referencia,
recursividad y documentación.
"""

# ----------------------------
# 1. FUNCIONES BÁSICAS
# ----------------------------
def saludar():
    print("Hola, bienvenido a Programación I")

def calcular_cuadrado(numero: int) -> int:
    return numero ** 2

def es_par(numero: int) -> bool:
    return numero % 2 == 0


# ----------------------------
# 2. PARÁMETROS Y RETORNO
# ----------------------------
def calcular_precio_con_iva(precio: float, iva: float = 21) -> float:
    return precio * (1 + iva / 100)

def restar(numero_a: int, numero_b: int = 5) -> int:
    return numero_a - numero_b


# ----------------------------
# 3. VARIABLES LOCALES Y GLOBALES
# ----------------------------
contador = 0  # variable global

def incrementar_contador():
    global contador
    contador += 1
    return contador


# ----------------------------
# 4. PASO POR VALOR Y REFERENCIA
# ----------------------------
def modificar_lista(lista: list):
    lista.append(100)
    return lista

def modificar_numero(n: int) -> int:
    n = n + 10
    return n


# ----------------------------
# 5. RECURSIVIDAD
# ----------------------------
def cuenta_regresiva(n: int):
    if n < 0:
        return
    print(n)
    cuenta_regresiva(n - 1)

def factorial(n: int) -> int:
    """
    Calcula el factorial de un número entero n.
    Parámetros:
        n (int): número entero no negativo
    Retorna:
        int: factorial de n
    """
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


# ----------------------------
# 6. PRUEBAS RÁPIDAS
# ----------------------------
if __name__ == "__main__":
    saludar()
    print("Cuadrado de 4:", calcular_cuadrado(4))
    print("¿10 es par?:", es_par(10))
    print("Precio con IVA:", calcular_precio_con_iva(100))
    print("Resta:", restar(15))
    print("Contador:", incrementar_contador())
    
    lista = [1, 2, 3]
    print("Lista modificada:", modificar_lista(lista))
    numero = 50
    print("Número modificado (por valor):", modificar_numero(numero))
    print("Número original:", numero)

    print("Cuenta regresiva desde 5:")
    cuenta_regresiva(5)
    print("Factorial de 5:", factorial(5))
    print("Fibonacci de 6:", fibonacci(6))
