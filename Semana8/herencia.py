class Animal:
    def __init__(self, especie, edad):
        self.especie = especie
        self.edad = edad

    #Metodo generico pero con implementacion particular
    def hablar(self):
        pass
    
    def moverse(self):
        pass
    
    def describime(self):
        print(f"Soy un {self.especie} y tengo {self.edad} años")
    
    
# class Perro(Animal): #Herencia
#      def __init__(self, especie, edad, dueno):
#         self.especie = especie
#         self.edad = edad
#         self.dueno = dueno

class Perro(Animal): #Herencia
    def __init__(self, especie, edad, dueno):
        super().__init__(especie, edad) #Llamada al constructor de la clase padre
        self.dueno = dueno

mi_perro = Perro("mamifero", 10, "Juan")
mi_perro.describime()
print(f"Mi dueño es {mi_perro.dueno}")
