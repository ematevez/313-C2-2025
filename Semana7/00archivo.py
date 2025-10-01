#Primero arbrir archivo y guardar cadenas

# archivo = open("archivo.txt", "w")
# archivo.write("Primer linea de texto\n")
# archivo.write("Segunda linea de texto\n")
# archivo.write("Tercera linea de texto\n")
# archivo.close()

#Segundo arbrir archivo y guardar lista de cadenas
# archivo = open("archivo.txt", "w")
# lineas_texto = ["Primer linea de texto\n", "Segunda linea de texto\n", "Tercera linea de texto\n"]
# archivo.writelines(lineas_texto)
# archivo.close()

#Tercero abrir archivo leer +
# archivo = open("archivo.txt", "r+")
# texto = archivo.read()
# print('El contenido del archivo es: ' + texto)
# archivo.close()

#Cuarto abrir archivo leer lineas +
# archivo = open("archivo1.txt", "r+", encoding='utf-8')
# lista_lineas = archivo.readlines()
# for linea in lista_lineas:
#     print(linea)
# archivo.close()

#CSV dataset
# with open("callero.csv", "r", encoding= 'utf-8-sig') as archivo:
#     matriz = []
#     monbre_columnas = archivo.readline().strip().split(",")
#     print("==========Los headers=====================")
#     print( monbre_columnas)
#     print("===============================")
    
#     for linea in archivo:
        
#         linea = linea.rstrip('\n')
#         print("==========Una linea=====================")
#         print(linea)
#         print("========================================")
#         fila = []
#         valores = linea.split(",")
        
#         for valor in valores:
#             if valor.isdigit():
#                 fila.append(int(valor))
#             else: 
#                 try:  
#                     fila.append(float(valor))
#                 except ValueError:
#                     fila.append(valor if valor.strip() != "" else None)
#         print("==========fila=====================")
#         print(fila)
#         print("========================================")
#         matriz.append(fila)

# print(monbre_columnas)
# print("==========CSV FINAL=====================")
# for fila in matriz:
#     print(fila) 
    
#! Esto utilizar los datos con pandas     
# import pandas as pd

# # Leer el archivo con pandas
# df = pd.read_csv("callero.csv", encoding="utf-8-sig")

# # Mostrar las primeras filas
# print(df.head())

# # Si querés ver todas las columnas siempre
# pd.set_option("display.max_columns", None)
# pd.set_option("display.width", None)

# # Mostrar de nuevo con todas las columnas
# print(df.head())


#Escribir CSV
# nombre_columnas = ["Nombre", "Edad", "Ciudad"]
# matriz = [["Juan", 28, "Madrid"],["Ana", 22, "Barcelona"],["Luis", 35, "Valencia"],["Marta", 30, "Sevilla"]]

# with open("personas.csv", "w", encoding="utf-8-sig") as archivo:
#     archivo.write(",".join(nombre_columnas) + "\n")
    
#     for fila in matriz:
#         linea = ""
#         for i in range(len(fila)):
#             linea += str(fila[i])
#             if i < len(fila) - 1:
#                 linea += ","
        
#         archivo.write(linea + "\n")

# Leer JSON
# import json

# with open("datos.json", "r", encoding="utf-8-sig") as archivo_json:
#     datos = json.load(archivo_json) 
#     print(datos)
#     print(type(datos))


# Escribir JSON
import json
datos = {
    "nombre": "Juan",
    "edad": 28,
    "ciudad": "Madrid",
    "hijos": ["Ana", "Luis"],
    "trabajo": {
        "empresa": "Tech Solutions",
        "puesto": "Desarrollador"
    }
}
datos1 = {
        "codigo": "011",
        "titulo": "T",
        "colaboradores": ["B"],
        "vistas": 4000,
        "duracion": 2,
        "link": "https://youtu.be/LLLLLLLL",
        "fecha": "2025-03-15"
}

with open("datos.json", "w", encoding="utf-8-sig") as archivo_json:
    json.dump(datos1, archivo_json, indent=4)
    archivo_json.write("\n")
 