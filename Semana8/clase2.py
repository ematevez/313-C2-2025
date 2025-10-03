# class Sueldo:  
#     def __init__(self,sueldo):
#         self.sueldo = sueldo
        
#     def __str__(self):
#         return f"\nEl sueldo es: {self.sueldo}"
    
#     class Empleado:
#         def __init__(self, nombre, puesto):
#             self.nombre = nombre
#             self.puesto = puesto
#             self.sueldo = Sueldo(1200)
            
#         def __str__(self):
#             return f"NOMBRE {self.nombre}\nPUESTO {self.puesto}\n" + self.sueldo.__str__()

# sueldo1 = Sueldo(200)
# empleado1 = Sueldo.Empleado("Juan", "Programador")

# print("RESULTADO 1: " + sueldo1.__str__())
# print("RESULTADO 2: " + empleado1.__str__())

#ENCAPSULAMIENTO
class Persona:
    tipo = "Humano"  # Atributo de clase 
    __sueldo = 1000  # Atributo privado de clase
    
    def __init__(self, nombre, apellido):
        self.nombre = nombre # Atributo público de instancia
        self.__apellido = apellido # Atributo privado de instancia
        
    def __soy_feliz(self):
        print("No les importa :)")
        
    def edad(self):
        return 31 # Método público de instancia
    
    
persona1 = Persona("Juan", "Perez")
print(f"Resultado 1: {persona1.tipo}\n")  # SI
# print(f"Resultado 2: {persona1.__sueldo}\n") # NO
print(f"Resultado 3: {persona1.nombre}\n") # SI
# print(f"Resultado 4: {persona1.__apellido}\n") # NO
# print(f"Resultado 5: {persona1.__soy_feliz()}\n") # SI
print(f"Resultado 6: {persona1.edad()}\n") # SI