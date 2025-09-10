# Escribir una función que calcule el área de un rectángulo. La función recibe la base y la altura y retorna el área. 
def rectangulo(base: float, altura:float) -> float:
    return base * altura

base = float(input("ingrese el valor de la base: "))
altura = float(input("ingrese el valor de la altura: "))

area = rectangulo(base, altura)
print(f"el area seleccionada del rectángulo es de {area}")