

# # ========================================
# # PASAJE POR VALOR (tipos inmutables)
# # ========================================

# def modificar_numero(num):
#     """Los números son inmutables - se pasa una copia del valor"""
#     print(f"Dentro de la función, num original: {num}")
#     num = num * 2
#     print(f"Dentro de la función, num modificado: {num}")
#     return num

# def modificar_string(texto):
#     """Los strings son inmutables - se pasa una copia del valor"""
#     print(f"Dentro de la función, texto original: {texto}")
#     texto = texto + " modificado"
#     print(f"Dentro de la función, texto modificado: {texto}")
#     return texto

# # Ejemplos de pasaje por valor
# print("=== PASAJE POR VALOR ===")
# numero_original = 10
# print(f"Número antes de la función: {numero_original}")
# resultado = modificar_numero(numero_original)
# print(f"Número después de la función: {numero_original}")
# print(f"Valor retornado: {resultado}")

# print("\n" + "-" * 40)
# string_original = "Hola"
# print(f"String antes de la función: {string_original}")
# resultado_str = modificar_string(string_original)
# print(f"String después de la función: {string_original}")
# print(f"Valor retornado: {resultado_str}")

# ========================================
# PASAJE POR REFERENCIA (tipos mutables)
# ========================================

def modificar_lista(lista):
    """Las listas son mutables - se pasa la referencia al objeto"""
    print(f"Dentro de la función, lista original: {lista}")
    lista.append("nuevo elemento")
    lista[0] = "modificado"
    print(f"Dentro de la función, lista modificada: {lista}")

# def modificar_lista_con_slicing(lista):
#     """Usando slicing para crear una nueva lista (no modifica la original)"""
#     print(f"Dentro de la función, lista original: {lista}")
#     nueva_lista = lista[1:3]  # Slice de índices 1 a 2
#     nueva_lista.append("elemento del slice")
#     print(f"Slice creado [1:3]: {nueva_lista}")
    
#     # Modificar con slicing (SÍ modifica la original)
#     lista[1:3] = ["reemplazo1", "reemplazo2", "extra"]
#     print(f"Lista después de slice assignment: {lista}")

# def trabajar_con_diccionario(diccionario):
#     """Los diccionarios son mutables - se pasa la referencia"""
#     print(f"Dentro de la función, dict original: {diccionario}")
#     diccionario["nueva_clave"] = "nuevo_valor"
#     diccionario["edad"] = diccionario.get("edad", 0) + 1
#     print(f"Dentro de la función, dict modificado: {diccionario}")

# Ejemplos de pasaje por referencia con listas
print("\n\n=== PASAJE POR REFERENCIA - LISTAS ===")
lista_original = [1, 2, 3, 4, 5]
print(f"Lista antes de la función: {lista_original}")
modificar_lista(lista_original)
print(f"Lista después de la función: {lista_original}")

# print("\n" + "-" * 40)
# lista_para_slice = ["a", "b", "c", "d", "e"]
# print(f"Lista antes del slicing: {lista_para_slice}")
# modificar_lista_con_slicing(lista_para_slice)
# print(f"Lista después del slicing: {lista_para_slice}")

# # Ejemplos adicionales de slicing con listas
# print("\n=== EJEMPLOS ADICIONALES DE SLICING ===")
# numeros = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# print(f"Lista original: {numeros}")

# def demostrar_slicing(lista):
#     print(f"lista[2:6]: {lista[2:6]}")           # Del índice 2 al 5
#     print(f"lista[:4]: {lista[:4]}")             # Desde el inicio hasta el índice 3
#     print(f"lista[6:]: {lista[6:]}")             # Desde el índice 6 hasta el final
#     print(f"lista[::2]: {lista[::2]}")           # Cada 2 elementos
#     print(f"lista[1::3]: {lista[1::3]}")         # Desde índice 1, cada 3 elementos
#     print(f"lista[::-1]: {lista[::-1]}")         # Lista invertida
#     print(f"lista[-3:]: {lista[-3:]}")           # Últimos 3 elementos
#     print(f"lista[:-2]: {lista[:-2]}")           # Todos excepto los últimos 2
    
#     # Slicing que modifica la lista original
#     lista[2:5] = [100, 200, 300, 400]  # Reemplaza elementos del índice 2 al 4
#     print(f"Después de lista[2:5] = [100, 200, 300, 400]: {lista}")

# demostrar_slicing(numeros)

# # Ejemplos con diccionarios
# print("\n\n=== PASAJE POR REFERENCIA - DICCIONARIOS ===")
# persona = {"nombre": "Juan", "edad": 25, "ciudad": "Madrid"}
# print(f"Diccionario antes de la función: {persona}")
# trabajar_con_diccionario(persona)
# print(f"Diccionario después de la función: {persona}")

# # Ejemplos avanzados con diccionarios y slicing de sus valores
# def procesar_diccionario_con_listas(data):
#     """Ejemplo con diccionario que contiene listas"""
#     print(f"Data original: {data}")
    
#     # Modificar una lista dentro del diccionario
#     data["numeros"].append(6)
#     data["numeros"][0] = 100
    
#     # Usar slicing en las listas del diccionario
#     data["letras"] = data["letras"][1:4]  # Mantener solo elementos del índice 1 al 3
#     data["nueva_lista"] = data["numeros"][::2]  # Cada segundo elemento
    
#     print(f"Data modificada: {data}")

# print("\n" + "-" * 40)
# datos_complejos = {
#     "numeros": [1, 2, 3, 4, 5],
#     "letras": ["a", "b", "c", "d", "e", "f"],
#     "info": "datos importantes"
# }
# print(f"Datos antes de procesar: {datos_complejos}")
# procesar_diccionario_con_listas(datos_complejos)
# print(f"Datos después de procesar: {datos_complejos}")

# # Demostración de cómo evitar modificar la referencia original
# print("\n\n=== CÓMO EVITAR MODIFICAR LA REFERENCIA ORIGINAL ===")

# def no_modificar_original(lista):
#     """Crear una copia para no modificar la original"""
#     copia = lista.copy()  # o lista[:]
#     copia.append("no afecta original")
#     print(f"Copia modificada: {copia}")
#     return copia

# def no_modificar_dict_original(diccionario):
#     """Crear una copia para no modificar el original"""
#     copia = diccionario.copy()
#     copia["nueva_clave"] = "no afecta original"
#     print(f"Copia modificada: {copia}")
#     return copia

# lista_test = [1, 2, 3]
# dict_test = {"a": 1, "b": 2}

# print(f"Lista original: {lista_test}")
# copia_lista = no_modificar_original(lista_test)
# print(f"Lista original después: {lista_test}")

# print(f"Dict original: {dict_test}")
# copia_dict = no_modificar_dict_original(dict_test)
# print(f"Dict original después: {dict_test}")