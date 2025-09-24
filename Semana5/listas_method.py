mi_lista = ["a","b","c","a"]

#!Agregar elementos
# append(x) → agrega un elemento al final.
# insert(i, x) → inserta un elemento en la posición i.
# extend(iterable) → agrega todos los elementos de otro iterable.
print("Lista original: ", mi_lista)
print("*--" * 20)

mi_lista.append("nuevo")
print("append: ", mi_lista)
print("--" * 20)
mi_lista.insert(2,[1,2,3,['a','b'],5])  # Por mas que sea una lista de listas no deja de ser un elemento
print("insert: ", mi_lista)
print("--" * 20)
mi_lista.extend([1,2,3,['a','b'],5])
print("extend: ", mi_lista)
print("--" * 20)

#! Eliminar elementos
# remove(x) → elimina la primera aparición de x. Si no esta #!ROMPE
# pop([i]) → elimina y devuelve el elemento en la posición i (por defecto el último).
# clear() → elimina todos los elementos de la lista.

mi_lista.remove('a')
print("remove: ", mi_lista)
print("--" * 20)
mi_lista.pop(4)
print("pop: ", mi_lista)
print("--" * 20)
mi_lista.clear()
print("clear: ", mi_lista)

#! Buscar elementos
new_lista = [1, 2, 3, 'elefante',2, 4, 'elefante']
# index(x[, start[, end]]) → devuelve el índice de la primera aparición de x.
# count(x) → devuelve cuántas veces aparece x.
# print("--" * 20)
print("index: ", new_lista.index('elefante'))
print("contador: ", new_lista.count('elefante'))
print("--" * 20)

#! Ordenar y revertir
# sort() → ordena la lista de menor a mayor.
# sort(reverse=True) → ordena de mayor a menor.
# reverse() → invierte el orden de los elementos.
lista_numeros = [7,1,5,6,9,0]
lista_strings = ['z','a','x','b']
lista_numeros.sort()
lista_strings.sort()

lista_numeros.sort(reverse=True) # ordena la lista de mayor a menor

#? https://docs.python.org/es/3/howto/sorting.html
print("sorted list: ", sorted(['z','a','x','b'])) 

palabras = ['javascript', 'java', 'c', 'go', 'python']
ordenado_por_longitud = sorted(palabras, key=len)
print(ordenado_por_longitud)  # ['c', 'go', 'java', 'python', 'javascript']

nums = [10, -5, 3, -20]
# Ordenar por el valor absoluto
print(sorted(nums, key=abs))

# ➡️ La función abs devuelve el valor absoluto, por eso -5 queda antes que 10.

# key es una función que transforma cada elemento en “la cosa por la que quiero ordenar”.
# Python llama a esa función una sola vez por elemento, usa ese resultado para ordenar,
# y al final te devuelve los elementos originales en el nuevo orden.


print("sort numeros: ", lista_numeros)
print("sort strings: ", lista_strings)
print("--" * 20)

#! Copiar lista
# copy() → devuelve una copia de la lista.
copiado_list = []
print("copialo_list original: ", copiado_list)
copiado_list = lista_strings.copy()
print("copialo_list Final: ", copiado_list)
lista_strings[0] = "rinoceronte"
print("copialo_list modificado: ", copiado_list)

# print("--" * 20)

#! Otras operaciones útiles
# len(lista) → longitud de la lista.
# sum(lista) → suma de los elementos (si son numéricos).
# max(lista) → mayor elemento.
# min(lista) → menor elemento.

otra_lista_numeros = [33,7,1,5,6,9,0,-1]
otra_lista_strings = ['z','h','a','x','b']
otra_lista_strings1 = ['zapato', 'zapatilla','helado','arbol','xanthorox','bolitas']
print("len de la lista: ", len(otra_lista_numeros))
print("suma la lista: ", sum(otra_lista_numeros))
print("muesta máximo de la lista: ", max(otra_lista_numeros))
print("muesta minimo de la lista: ", min(otra_lista_numeros))

print("len de la lista: ", len(otra_lista_strings))
# # print("suma la lista: ", sum(otra_lista_strings)) #!ROMPE
print("muesta máximo de la lista: ", max(otra_lista_strings))
print("muesta minimo de la lista: ", min(otra_lista_strings))

print("len de la lista: ", len(otra_lista_strings1))
print("muesta máximo de la lista: ", max(otra_lista_strings1))
print("muesta minimo de la lista: ", min(otra_lista_strings1))

otra_lista_strings1.sort()    
print("ordena las palabras: ", otra_lista_strings1)



