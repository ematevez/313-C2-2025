import random
import time
import tracemalloc

# =====================================================
# 1. HEAP SORT
# -----------------------------------------------------
# Idea: Se basa en la estructura de datos "Heap" (árbol binario).
#       Convierte la lista en un heap y luego va extrayendo el máximo.
# Complejidad: O(n log n) en todos los casos.
# Ventaja: muy eficiente y estable en rendimiento.
# =====================================================
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr


# =====================================================
# 2. COUNTING SORT
# -----------------------------------------------------
# Idea: No compara elementos. Cuenta cuántas veces aparece cada valor.
#       Funciona muy bien si los números están en un rango pequeño.
# Complejidad: O(n + k), donde k es el rango de los valores.
# Limitación: Solo funciona con enteros (no con strings o floats).
# =====================================================
def counting_sort(arr):
    max_val = max(arr)
    min_val = min(arr)
    rango = max_val - min_val + 1

    count = [0] * rango
    salida = [0] * len(arr)

    for num in arr:
        count[num - min_val] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for num in reversed(arr):
        salida[count[num - min_val] - 1] = num
        count[num - min_val] -= 1

    return salida


# =====================================================
# 3. RADIX SORT
# -----------------------------------------------------
# Idea: Ordena los números por "dígitos", usando Counting Sort como subrutina.
# Ejemplo: Primero ordena por unidades, luego decenas, luego centenas...
# Complejidad: O(n * k), donde k es el número de dígitos del número más grande.
# =====================================================
def counting_sort_radix(arr, exp):
    n = len(arr)
    salida = [0] * n
    count = [0] * 10

    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % 10
        salida[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1

    for i in range(len(arr)):
        arr[i] = salida[i]

def radix_sort(arr):
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_radix(arr, exp)
        exp *= 10
    return arr


# =====================================================
# 4. SHELL SORT
# -----------------------------------------------------
# Idea: Es una mejora del Insertion Sort.
#       Usa "saltos" (gaps) que van disminuyendo hasta llegar a 1.
# Complejidad: depende de la secuencia de gaps, suele ser O(n log^2 n).
# Ventaja: más rápido que Insertion en listas grandes.
# =====================================================
def shell_sort(arr):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


# =====================================================
# 5. BUCKET SORT
# -----------------------------------------------------
# Idea: Divide los elementos en "baldes" (intervalos).
#       Cada balde se ordena individualmente y luego se juntan.
# Complejidad: O(n + k), depende de cómo se reparten los datos.
# Ventaja: muy bueno si los datos están distribuidos uniformemente.
# =====================================================
def bucket_sort(arr):
    max_val = max(arr)
    size = max_val / len(arr)

    buckets = [[] for _ in range(len(arr))]

    for num in arr:
        index = int(num / size)
        if index != len(arr):
            buckets[index].append(num)
        else:
            buckets[len(arr) - 1].append(num)

    for bucket in buckets:
        bucket.sort()

    salida = []
    for bucket in buckets:
        salida.extend(bucket)
    return salida


# =====================================================
# Función para medir rendimiento
# =====================================================
def medir(algoritmo, lista):
    copia = lista.copy()
    tracemalloc.start()
    inicio = time.time()
    algoritmo(copia)
    fin = time.time()
    memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return fin - inicio, memoria_pico / 1024


# =====================================================
# Listas de prueba
# =====================================================
lista_pequena = random.sample(range(1000), 100)
lista_mediana = random.sample(range(10000), 1000)
lista_grande  = random.sample(range(50000), 5000)


# =====================================================
# Ejecución paso a paso (ejemplo con lista mediana)
# =====================================================
print("\n--- Lista Mediana (1000 elementos) ---")

t, m = medir(heap_sort, lista_mediana)
print(f"Heap Sort     -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(counting_sort, lista_mediana)
print(f"Counting Sort -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(radix_sort, lista_mediana)
print(f"Radix Sort    -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(shell_sort, lista_mediana)
print(f"Shell Sort    -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(bucket_sort, lista_mediana)
print(f"Bucket Sort   -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")
