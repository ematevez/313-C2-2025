# nombres = ["Rosita", "Manuel", "Lucía", "Carlos", "Ana", "Luis"]

# print("Nombres en la lista:", nombres)

# num = ["a", 0, ["h", "o", "L"], 3**4+99 ,] * 5



# print("Contenido: ", num)


# print("=" * 30)
# mi_lista = [10, "hola", False, 3.5]

# #Acceder a primer elemento
# print(mi_lista[0])
# print(mi_lista[1]*10)
# print(mi_lista[-2]*5)
# print(mi_lista[-4])

# print(mi_lista[0]*mi_lista[-1])
# print("=" * 30)
# print("Lista original : ", mi_lista)
# print("=" * 30)
# mi_lista[1] = "chau"
# print("cambio valor por indice: ", mi_lista)
# print("=" * 30)
# mi_lista[-3] = "sigo"
# print("cambio valor por indice negativo: ", mi_lista)

# print("=" * 30)
# #Contar
# longitud = len(mi_lista)
# print("Longitud de la lista: ", longitud)

# print("=" * 30)
# #Iterar la lista dando un indice numerico
# for elemento in range(len(mi_lista)):
#     print(f"Elemento {elemento}: {mi_lista[elemento]}")

# print("=" * 30)    
# #Iterar la lista dando el elemento
# for elemento in mi_lista:
#     print(f"Elemento: {elemento}")


# notas = [7, 8.5, 6, 9, 10, 5.5]
# total = 0
# total1 = 0
# print("=" * 30) 
# #Iterar la lista para calcular el promedio
# for elemento in range(len(notas)):
#     total = total + notas[elemento]
    
# print("Total: ", total)
# print("Promedio: ", total/len(notas))
    
# print("=" * 30)
# #Iterar la lista para calcular el promedio sin indice 
# for elemento in notas:
#     total1 +=  elemento
    
# print("Total: ", total1)
# print("Promedio: ", total1/len(notas))

print("=" * 30)
list_1 = [1, 2, 3, 4, 5, 6]
print("Lista original: ", list_1)
print("=" * 30)
list_2 = list_1
print("Lista 2 : ", list_2)
print("=" * 30)
list_1[0] = 100
print("Lista 2 de nuevo : ", list_2)


