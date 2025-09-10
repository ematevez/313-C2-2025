import math
import time
import tracemalloc
import timeit

print("Para calcular una potencia - Comparación de rendimiento")
print("=" * 55)

def potencia(base, exponente):
    return base ** exponente

def potenciamath(base, exponente):
    return math.pow(base, exponente)

def medir_rendimiento(func, base, exponente, nombre):
    """Función para medir tiempo y memoria de una función"""
    
    # Medir memoria
    tracemalloc.start()
    
    # Medir tiempo (una sola ejecución)
    inicio = time.perf_counter()
    resultado = func(base, exponente)
    fin = time.perf_counter()
    tiempo_single = fin - inicio
    
    # Obtener uso de memoria
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Medir tiempo promedio (múltiples ejecuciones para mayor precisión)
    tiempo_promedio = timeit.timeit(
        lambda: func(base, exponente), 
        number=100000
    ) / 100000
    
    print(f"\n{nombre}:")
    print(f"  Resultado: {resultado}")
    print(f"  Tiempo (1 ejecución): {tiempo_single:.2e} segundos")
    print(f"  Tiempo promedio (100k ejecuciones): {tiempo_promedio:.2e} segundos")
    print(f"  Memoria actual: {current / 1024:.2f} KB")
    print(f"  Memoria pico: {peak / 1024:.2f} KB")
    
    return {
        'resultado': resultado,
        'tiempo_single': tiempo_single,
        'tiempo_promedio': tiempo_promedio,
        'memoria_actual': current,
        'memoria_pico': peak
    }

# Solicitar datos al usuario
base = int(input("Ingrese la Base: "))
exponente = int(input("Ingrese el exponente: "))

print(f"\nComparando: {base}^{exponente}")

# Medir rendimiento de ambas funciones
stats_normal = medir_rendimiento(potencia, base, exponente, "Operador ** (potencia)")
stats_math = medir_rendimiento(potenciamath, base, exponente, "math.pow()")

# Comparación directa
print("\n" + "=" * 55)
print("COMPARACIÓN:")
print("=" * 55)

# Comparar tiempos
if stats_normal['tiempo_promedio'] < stats_math['tiempo_promedio']:
    factor_tiempo = stats_math['tiempo_promedio'] / stats_normal['tiempo_promedio']
    print(f"⚡ El operador ** es {factor_tiempo:.2f}x más RÁPIDO")
else:
    factor_tiempo = stats_normal['tiempo_promedio'] / stats_math['tiempo_promedio']
    print(f"⚡ math.pow() es {factor_tiempo:.2f}x más RÁPIDO")

# Comparar memoria
if stats_normal['memoria_pico'] < stats_math['memoria_pico']:
    factor_memoria = stats_math['memoria_pico'] / stats_normal['memoria_pico']
    print(f"💾 El operador ** usa {factor_memoria:.2f}x MENOS memoria")
else:
    factor_memoria = stats_normal['memoria_pico'] / stats_math['memoria_pico']
    print(f"💾 math.pow() usa {factor_memoria:.2f}x MENOS memoria")

print(f"\nDiferencia en memoria: {abs(stats_math['memoria_pico'] - stats_normal['memoria_pico']) / 1024:.2f} KB")
print(f"Diferencia en tiempo: {abs(stats_math['tiempo_promedio'] - stats_normal['tiempo_promedio']):.2e} segundos")

# Información adicional
print(f"\n📊 DETALLES TÉCNICOS:")
print(f"   • El operador ** trabaja con enteros nativos de Python")
print(f"   • math.pow() siempre devuelve float y usa funciones de C")
print(f"   • Para enteros pequeños, ** suele ser más eficiente")
print(f"   • Para números muy grandes o decimales, math.pow() puede ser mejor")