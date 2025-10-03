# class Perro:
#     #Atributo de clase
#     especie = "Mamifero"
    
#     #Contructor de la clase
#     def __init__(self, nombre= "Perro", raza= "Terbal"):
#         print(f"Se esta creado un perro llamado {nombre} de raza {raza}")
        
#         #Atributos de instancia
#         self.nombre = nombre
#         self.raza = raza
    
#     def ladrar(self):
#         print("Guau Guau")
        
#     def caminar(self, pasos):
#         print(f"Caminando {pasos} pasos")

# class Vector():
#     def __init__(self, data, nombre, peso, edad, etc):
#         self._data = data
#         self.nombre = nombre
#         self.peso = peso    
#         self.edad = edad
#         self.etc = etc  

#     def __str__(self):
#         return f" El valor de edad es: {self.edad} y el nombre es: {self.nombre}"
    
#     def __len__(self):
#         return len(self.nombre)

#     def __getitem__(self,   pos):
#         return self._data[pos]

#     def __setitem__(self, value):
#         self.edad = value
    


# v = Vector([1,2], "Vector1", 2.5, 3, None)
# print(v)
# # print(len(v))
# # print(len(v.nombre))
# # print(v[1])

# # modificar valor edad
# v = 34
# print(v)
# # print(Perro.especie)    
# # perro1 = Perro()
# # print(perro1.nombre)
# print(perro1.especie)

# perro2 = Perro("Firulais","Chihuahua")

# print(f"El perro2 se llama {perro2.nombre} y es de raza {perro2.raza}")

# perro3 = Perro(nombre="Tito",raza="Pastor Aleman")
# perro3.ladrar()
# perro3.caminar(10)

class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def __str__(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}"  
    
persona1 = Persona("Juan", 30)
print(persona1)
print("===============================")



# Modificación directa
persona1.nombre = "Pedro"
persona1.edad = 35

print(persona1.nombre, persona1.edad)
print("===============================")
print(persona1)
