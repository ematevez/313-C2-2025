from ursina import *

# Inicializa la ventana del juego
app = Ursina()

# Crea un cubo 3D en la posición (0, 0, 0)
cube = Entity(model='cube', color=color.orange, scale=(2,2,2), texture='white_cube')

# Crea un suelo
ground = Entity(model='plane', scale=(10,10,1), color=color.dark_gray, y=-1)

# Función que se ejecuta en cada frame
def update():
# Rota el cubo cada frame
    cube.rotation_y += 1

# Inicia el bucle de juego
app.run()
