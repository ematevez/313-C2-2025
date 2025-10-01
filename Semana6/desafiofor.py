# Números ascendentes del 1 al 10
for i in range(1, 11):
    print(i)

# Números descendentes del 10 al 1
for i in range(10, 0, -1):
    print(i)

# De 0 hasta un número ingresado
n = int(input("Ingrese un número: "))
for i in range(0, n + 1):
    print(i)

# Tabla de multiplicar de un número
n = int(input("Ingrese un número: "))
for i in range(0, 11):
    print(f"{n} x {i} = {n * i}")

# Ingresar hasta 10 números o hasta que se ingrese 0, mostrar suma y promedio
suma = 0
contador = 0
for i in range(10):
    num = int(input("Ingrese un número (0 para salir): "))
    if num == 0:
        break
    suma += num
    contador += 1

if contador > 0:
    promedio = suma / contador
    print(f"Suma: {suma}, Promedio: {promedio}")
else:
    print("No se ingresaron números.")

# Múltiplos de 3 entre 1 y 10
for i in range(1, 11):
    if i % 3 == 0:
        print(i)

# Números pares desde 1 hasta 50
for i in range(2, 51, 2):
    print(i)

# Pirámide de números
n = int(input("Ingrese un número: "))
for i in range(1, n + 1):
    for j in range(1, i + 1):
        print(j, end=" ")
    print()   # Salto de línea

# Divisores de un número y cantidad
n = int(input("Ingrese un número: "))
contador = 0
for i in range(1, n + 1):
    if n % i == 0:
        print(i)
        contador += 1
print(f"Cantidad de divisores: {contador}")

# Determinar si un número es primo
n = int(input("Ingrese un número: "))
es_primo = True
if n < 2:
    es_primo = False
else:
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            es_primo = False
            break

print("Es primo" if es_primo else "No es primo")

# Primos entre 1 y un número ingresado
n = int(input("Ingrese un número: "))
contador_primos = 0
for num in range(2, n + 1):
    es_primo = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            es_primo = False
            break
    if es_primo:
        print(num)
        contador_primos += 1
print(f"Cantidad de números primos: {contador_primos}")