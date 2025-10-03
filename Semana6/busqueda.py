import random
import time
import tracemalloc

# =============================
# Algoritmos de Ordenamiento #!SELECTION_SORT
# =============================
#
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# =============================
# Algoritmos de Ordenamiento #!BUBBLE_SORT
# =============================

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

# =============================
# Algoritmos de Ordenamiento #!QUICK_SORT
# =============================

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# =============================
# Algoritmos de Ordenamiento #!MERGE_SORT
# =============================

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr


# =============================
# Algoritmos de Ordenamiento #!INSERTION_SORT
# =============================

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

# =============================
#? Función para medir rendimiento
# =============================
def medir(algoritmo, lista):
    copia = lista.copy()   # usamos copia para no alterar la original
    tracemalloc.start()
    inicio = time.time()
    algoritmo(copia)
    fin = time.time()
    memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return fin - inicio, memoria_pico / 1024  # tiempo en seg, memoria en KB

# =============================
# Listas de prueba
# =============================
lista_pequena = random.sample(range(1000), 100)
lista_mediana = random.sample(range(10000), 1000)
lista_grande  = random.sample(range(50000), 50000)

# =============================
# Pruebas paso a paso
# =============================

print("\n--- Lista Pequeña (100 elementos) ---")
t, m = medir(selection_sort, lista_pequena)
print(f"Selection Sort -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(bubble_sort, lista_pequena)
print(f"Bubble Sort    -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(insertion_sort, lista_pequena)
print(f"Insertion Sort -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(quicksort, lista_pequena)
print(f"QuickSort      -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(merge_sort, lista_pequena)
print(f"MergeSort      -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")


print("\n--- Lista Mediana (1000 elementos) ---")
t, m = medir(selection_sort, lista_mediana)
print(f"Selection Sort -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(bubble_sort, lista_mediana)
print(f"Bubble Sort    -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(insertion_sort, lista_mediana)
print(f"Insertion Sort -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(quicksort, lista_mediana)
print(f"QuickSort      -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(merge_sort, lista_mediana)
print(f"MergeSort      -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")


print("\n--- Lista Grande (5000 elementos) ---")
t, m = medir(selection_sort, lista_grande)
print(f"Selection Sort -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(bubble_sort, lista_grande)
print(f"Bubble Sort    -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(insertion_sort, lista_grande)
print(f"Insertion Sort -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(quicksort, lista_grande)
print(f"QuickSort      -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")

t, m = medir(merge_sort, lista_grande)
print(f"MergeSort      -> Tiempo: {t:.4f} seg | Memoria: {m:.2f} KB")
