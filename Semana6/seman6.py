# cadena = "Que tal"

# print (id(cadena))
# print(cadena)

# print("==============")
# cadena = cadena + "? "
# print (id(cadena))
# print(cadena)


# print("==============")
# print(cadena * 5 )

# texto = "Procesador"

# print(texto == "Procesador")   # True     
# print(texto != "Procesador")   # False
# print(texto > "Mother")        # True
# print(texto < "procesador")    # False 
# print("==============")
# print(1 == 1)  #True
# print(1 != 1)  #False
# print(5 < 1)   #False
# print(1 > 1)   #False
# print("==============") 
# print(False > True)   #False
# print(False == True)   #False

ejemplo = "               hOLa Mundo                  "
# =========================CADENAS===========================
# FUNCIONES Y METODOS COMUNES DE STRINGS
# print(ejemplo.strip())   #→ elimina espacios al inicio y al final
# print(ejemplo.lstrip())  #→ elimina solo a la izquierda
# print(ejemplo.rstrip())  #→ elimina solo a la derecha
# print("===================")
# print(ejemplo.upper())    #-> Mayuscula
# print(ejemplo.lower())    #-> Minuscula
# print(ejemplo.capitalize())   #-> Primera letra en mayusucla #!si hay espacios no lo toma
# print(ejemplo.title())    #-> Cada palabra en mayuscula
print("===================")
print(ejemplo.find("Mundo"))   #→ posición donde empieza "Mundo"
print(ejemplo.count("o"))      #→ cuántas veces aparece la letra "o"
print("Hola" in ejemplo)       # True → verifica si existe
print("Python" not in ejemplo) # True → verifica si no existe
print("===================")
print(ejemplo.replace("Mundo", "Python"))  # "  Hola Python  "
print("===================")


frase = "manzana,pera,banana"
lista = frase.split(",") 
print(lista)
print("===================")
print("-h-".join(lista))

lista1 = [1,2,3,4]
lista2 = ("a", "B", "HHH")
# ==============================
resu = lista1 + lista2
print (resu)