#PARA COMPILAR COMO APK(PARA EL CELU), SE USA UNA LIBRERIA LLAMADA KIVY
# ES COMPLEJO PERO FUNCIONA MUCHOS VIDEOS EN YOTUBE

import random
# CREAR E INICIALIZAR UNA MATRIZ 

# def inicializar_matriz(cant_filas: int, cant_columnas: int, valor_inicial: any) -> list:
#     matriz = []
#     for i in range(cant_filas):
#         fila = [valor_inicial] * cant_columnas
#         # matriz.append(fila)       
#         matriz += [fila]
#     return matriz

# mi_matriz = inicializar_matriz(4, 4, 1)
# print(mi_matriz,end="\n")



def matriz_aleatoria(filas: int, columnas: int, minimo: int = 0, maximo: int = 9) -> list:
    """
    Crea una matriz (lista de listas) de tamaño filas x columnas
    con números enteros aleatorios entre minimo y maximo (inclusive).
    """
    matriz = []
    for _ in range(filas):
        #! ACOMODEN ESTA LINEA CON LO QUE SABEN ==========================
        fila = [random.randint(minimo, maximo) for _ in range(columnas)] #!-> ojo con esto no es normal 
        #! ACOMODEN ESTA LINEA CON LO QUE SABEN ==========================
        matriz.append(fila)
    return matriz


mi_matriz = matriz_aleatoria(4,4,0,9)

def imprimir_matriz_con_end(matriz: list) -> None:
    for fila in matriz:
        for valor in fila:
            # Imprime cada número seguido de un espacio en la misma línea
            print(valor, end=" ")
        # Al terminar la fila, hacemos un salto de línea
        print()  # <- este print vacío vuelve a la siguiente fila

# Crear una matriz 4x4 de ceros
# matriz_4x4 = inicializar_matriz(4, 4, 0)
# imprimir_matriz_con_end(mi_matriz)



# =====================================================================  


# def cargar_matriz_secuencialmente(matriz:list):
# # Agregar las validaciones/retorno que sean necesarias
#     for i in range(len(matriz)):
#         for j in range(len(matriz[i])):
#             matriz[i][j] = int(input(f"Fila {i} Columna {j}: "))

# cargar_matriz_secuencialmente(mi_matriz)
# print(mi_matriz,end="\n")


# ============================================
# def cargar_matriz_aleatoriamente(matriz:list):
# 	# Agregar las validaciones/retorno que sean necesarias
#     seguir = "S"
#     while seguir == "S": 
#         fila = int(input("Indice de fila: "))
#         columna = int(input("Indice de columna: "))
#         dato = int(input("Ingrese el numero a cargar: "))
#         matriz[fila][columna] = dato 
#         seguir = input("Desea seguir cargando? S/N: ")
#         imprimir_matriz_con_end(mi_matriz)

# cargar_matriz_aleatoriamente(mi_matriz)

imprimir_matriz_con_end(mi_matriz)


# ===========BUSCAR VALORES EN UNA MATRIZ==============
def buscar_valor_entero(matriz:list, valor:int):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == valor:
                print(f"Se encontró el número en fila {i} columna {j}!")
                # return -> solo si quiere mostrar el primero

buscar_valor_entero(mi_matriz, 5)
# ============================================================
def sumar_matrices(A, B):
    """
    Suma dos matrices del mismo tamaño.
    """
    # Verificar que las dimensiones coincidan
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        print("Las matrices deben tener el mismo tamaño")
        return
    
    resultado = []
    for i in range(len(B)):
        fila = []
        for j in range(len(A[0])):
            fila.append(A[i][j] + B[i][j])
        resultado.append(fila)
    return resultado

#SUMA DE MATRICES POR COMPRENSION
# C = [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


# ============================================================
def multiplicar_por_escalar(matriz, escalar):
    """
    Multiplica cada elemento de la matriz por un escalar.
    """
    # resultado = []
    # for fila in matriz:
    #     nueva_fila = [valor * escalar for valor in fila]
    #     resultado.append(nueva_fila)
    # return resultado
    resultado = []
    for i in range(len(matriz)):
        nueva_fila = []
        for j in range(len(matriz[i])):
            nueva_fila.append(matriz[i][j] * escalar)
        resultado.append(nueva_fila)
    return resultado

# ============================================================

def multiplicar_matrices(A, B):
    # Verificar si se puede multiplicar
    if len(A[0]) != len(B):
        print("Número de columnas de A debe ser igual al número de filas de B")
        return

    resultado = []
    for i in range(len(A)):
        fila = []
        for j in range(len(B[0])):
            suma = 0
            for k in range(len(B)):
                suma += A[i][k] * B[k][j]
            fila.append(suma)
        resultado.append(fila)
    return resultado




#SUMA DE MATRICES======================================
print("=====Matriz 1================")
mtrz_suma1 = matriz_aleatoria(2,2,0,9)
imprimir_matriz_con_end(mtrz_suma1)
print("=====Matriz 2================")
mtrz_suma2 = matriz_aleatoria(2,2,0,9)
imprimir_matriz_con_end(mtrz_suma2)
print("=====RESULTADO=== SUMA=============")
mtrz_resu = sumar_matrices(mtrz_suma1,mtrz_suma2)
imprimir_matriz_con_end(mtrz_resu)


print("=====RESULTADO=== MULTIPLICA POR ESCALAR=============")
mtrz_resu1 = multiplicar_por_escalar(mtrz_suma1, 3)
imprimir_matriz_con_end(mtrz_resu1) 



print("=====RESULTADO=== MULTIPLICA 2 MTRZ=============")
mtrz_resu2 = multiplicar_matrices(mtrz_suma1, mtrz_suma2)
imprimir_matriz_con_end(mtrz_resu2) 



















