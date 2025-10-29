from ursina import *
import random

app = Ursina()

window.title = "Shooter Espacial"
window.color = color.black
camera.fov = 90

# === Jugador ===
player = Entity(model='sphere', color=color.azure, scale=0.5, position=(0,0,0))
camera.parent = player
camera.position = (0,1.5,-3)
camera.rotation = (0,0,0)

speed = 5

# === Balas ===
balas = []

def disparar():
    # Crea una bala con dirección aleatoria ligera
    offset_x = random.uniform(-0.05, 0.05)
    offset_y = random.uniform(-0.05, 0.05)
    direccion = Vec3(camera.forward.x + offset_x, camera.forward.y + offset_y, camera.forward.z)
    bala = Entity(model='sphere', color=color.yellow, scale=0.1, position=player.world_position, velocity=direccion * 10)
    balas.append(bala)

# === Enemigos ===
enemigos = []
vidas = {}

def crear_enemigo():
    tamaño = random.uniform(0.5, 2)
    vida = int(tamaño * 50)
    enemigo = Entity(model='sphere', color=color.red, scale=tamaño,
                     position=(random.uniform(-20,20), random.uniform(-5,5), random.uniform(5,25)))
    texto_vida = Text(text=str(vida), origin=(0,0), scale=2, position=(0, 0.5))
    texto_vida.world_parent = enemigo
    enemigos.append((enemigo, texto_vida))
    vidas[enemigo] = vida

for i in range(5):
    crear_enemigo()

# === Movimiento y actualización ===
def update():
    # Movimiento espacial libre
    if held_keys['w']:
        player.position += camera.forward * time.dt * speed
    if held_keys['s']:
        player.position -= camera.forward * time.dt * speed
    if held_keys['a']:
        player.position -= camera.right * time.dt * speed
    if held_keys['d']:
        player.position += camera.right * time.dt * speed
    if held_keys['space']:
        player.position += camera.up * time.dt * speed
    if held_keys['shift']:
        player.position -= camera.up * time.dt * speed

    # Movimiento de balas
    for bala in balas:
        bala.position += bala.velocity * time.dt

        # Verifica colisiones con enemigos
        for enemigo, texto_vida in enemigos:
            if distance(bala, enemigo) < (enemigo.scale_x / 2 + bala.scale_x):
                vidas[enemigo] -= random.randint(10, 30)
                texto_vida.text = str(vidas[enemigo])
                destroy(bala)
                balas.remove(bala)
                if vidas[enemigo] <= 0:
                    destroy(enemigo)
                    destroy(texto_vida)
                    enemigos.remove((enemigo, texto_vida))
                break

    # Rota lentamente los enemigos
    for enemigo, _ in enemigos:
        enemigo.rotation_y += time.dt * 30

def input(key):
    if key == 'left mouse down':
        disparar()

app.run()
