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
mi_lista.insert(2,"insertado2")
print("insert: ", mi_lista)
print("--" * 20)
mi_lista.extend([7, 'f'])
print("extend: ", mi_lista)
print("--" * 20)

#! Eliminar elementos
# remove(x) → elimina la primera aparición de x. Si no esta #!ROMPE
# pop([i]) → elimina y devuelve el elemento en la posición i (por defecto el último).
# clear() → elimina todos los elementos de la lista.

mi_lista.remove('a')
print("remove: ", mi_lista)
print("--" * 20)
mi_lista.pop(1)
print("pop: ", mi_lista)
print("--" * 20)
mi_lista.clear()
print("clear: ", mi_lista)

#! Buscar elementos
new_lista = [1, 2, 3, 'elefante',2, 4, 'elefante']
# index(x[, start[, end]]) → devuelve el índice de la primera aparición de x.
# count(x) → devuelve cuántas veces aparece x.
print("--" * 20)
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

print("--" * 20)

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
# print("suma la lista: ", sum(otra_lista_strings)) #!ROMPE
print("muesta máximo de la lista: ", max(otra_lista_strings))
print("muesta minimo de la lista: ", min(otra_lista_strings))

print("len de la lista: ", len(otra_lista_strings1))
print("muesta máximo de la lista: ", max(otra_lista_strings1))
print("muesta minimo de la lista: ", min(otra_lista_strings1))

otra_lista_strings1.sort()    
print("ordena las palabras: ", otra_lista_strings1)


#! Ejemplos sencillos para practicar
# Crear una lista con números del 1 al 5, agregar el 6, y luego eliminar el 2.
# Crear una lista con nombres de tus amigos y ordenarla alfabéticamente.
# Contar cuántas veces aparece el número 3 en una lista.
# Invertir una lista de frutas.
# Hacer la suma de todos los números en una lista.

