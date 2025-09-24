import random

#! Ejemplos sencillos para practicar
# Crear una lista con números del 1 al 5, agregar el 6, y luego eliminar el 3.

# mi_lista = [1, 3, 5, 7, 9, 11, 13]
# mi_lista.append(6)
# mi_lista.remove(3)
# mi_lista.sort()

# print(mi_lista)
# =====================================================================
# mi_lista = [1,2,3,4,5]
# print(f"lista inicial: {mi_lista}\n")

# mi_lista.append(6)        # append(x) → agrega un elemento al final.
# mi_lista.remove(2)        # remove(x) → elimina la primera aparición de 2. Si no esta #!ROMPE
# print(f"lista final: {mi_lista}")

# Crear una lista con nombres de tus amigos y ordenarla alfabéticamente.

# amigos = ["Carlos", "Ana", "Beatriz", "David", "Elena"]
# print("Lista original:", amigos)

# # Ordenada
# amigos.sort()
# print("Lista ordenada:", amigos)

# Contar cuántas veces aparece el número 3 en una lista.
# lista_numeros = []
# for i in range(10):
#     num_random = random.randint(1,10)
#     lista_numeros.append(num_random)
# print("lista creada: " ,lista_numeros)
# apareciones = lista_numeros.count(3)
# print("apariciones del 3: " , apareciones)


# Invertir una lista de frutas.

# lista_frutas = ["manzana", "banana", "cereza", "durazno"]
# print(lista_frutas)
# print(lista_frutas.reverse)

# listaFrutas = ["banana","manzana","frutilla"]
# print("Lista original: ",listaFrutas)
# listaFrutas.sort(reverse= True)
# print("Lista invertida",listaFrutas)
# print("---" * 20 )

# # Hacer la suma de todos los números en una lista.

# lista2Numeros = [2,4,5,6,2,2,2,2,2]
# print(sum(lista2Numeros))

# Slicing (rebanado) rápido
letras = [1,2,3,4,5,6,7,8,9]
print(letras[2:6])   # [3,4,5,6]  -> desde índice 2 hasta 6
print(letras[:5])    # [1,2,3,4,5,6]  -> desde el inicio hasta 5
print(letras[::3])   #  de 3 en 3 [1,4,7]
print(letras[::-2])  # [9,7,5,3,1] -> invertida 

# ======================================================================

mi_lista = [1, 3, 5, 7, 9, 11, 13, 40, 39, 73, 115]
buscar = 40
numeros = [1,2,3,4,5,6,7,8,9,10]
encontrar_numero = 5
#  1 -Búsqueda lineal (el más simple)

for numero in numeros:
    if numero == encontrar_numero:
        print(f"Numero {encontrar_numero} encontrado")
        break

    
#  2 -Buscar el índice de un valor
busqueda = mi_lista.index(buscar)
print(f"Indice donde esta el numero 40: {busqueda}")

# =======================
def buscar_Indice(valorABuscar):
    indiceEncontrado = None
    for valor in mi_lista:
        if valor == valorABuscar:
            indiceEncontrado = mi_lista.index(valor)
            break
    return indiceEncontrado

print(buscar_Indice(3))

#  3 -Búsqueda binaria (requiere lista ordenada)
# import bisect

# ordenada = [1, 3, 5, 7, 9]
# objetivo = 7

# # bisect_left devuelve la posición donde debería insertarse
# pos = bisect.bisect_left(ordenada, objetivo)

# if pos < len(ordenada) and ordenada[pos] == objetivo:
#     print(f"Encontrado en la posición {pos}")
# else:
#     print("No está en la lista")
# # Encontrado en la posición 3

# Ordenamiento
nums = [5, 1, 9, 3, 7]

# Ascendente
asc = sorted(nums)
print("Ascendente:", asc)          # [1, 3, 5, 7, 9]

# Descendente
desc = sorted(nums, reverse=True)
print("Descendente:", desc)        # [9, 7, 5, 3, 1]


# Ordena por longitud de palabras
palabras = ["uva", "manzana", "pera", "kiwi"]

ordenadas = sorted(palabras, key=len)
print("Por longitud:", ordenadas) # ['uva', 'pera', 'kiwi', 'manzana']
