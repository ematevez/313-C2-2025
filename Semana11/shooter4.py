from ursina import *
import random

app = Ursina()

window.title = "Shooter Espacial Extendido"
window.color = color.black
camera.fov = 90

# === Jugador ===
player = Entity(model='sphere', color=color.azure, scale=0.5, position=(0, 0, 0))
camera.parent = player
camera.position = (0, 1.5, -3)
camera.rotation = (0, 0, 0)

speed = 6
player_vida = 100
texto_vida = Text(text=f"Vida: {player_vida}", position=(-0.85, 0.45), scale=2, color=color.lime)

# === Balas ===
balas = []

def disparar():
    # Crea una bala con leve aleatoriedad de dirección
    offset_x = random.uniform(-0.05, 0.05)
    offset_y = random.uniform(-0.05, 0.05)
    direccion = Vec3(camera.forward.x + offset_x, camera.forward.y + offset_y, camera.forward.z)
    bala = Entity(model='sphere', color=color.yellow, scale=0.1, position=player.world_position, velocity=direccion * 10)
    balas.append(bala)

# === Enemigos ===
enemigos = []
vidas = {}

colores = [color.red, color.orange, color.violet, color.magenta, color.green, color.pink]

def crear_enemigo():
    tamaño = random.uniform(0.5, 2)
    vida = int(tamaño * 50)
    color_aleatorio = random.choice(colores)
    enemigo = Entity(model='sphere', color=color_aleatorio, scale=tamaño,
                     position=(random.uniform(-25, 25), random.uniform(-5, 5), random.uniform(10, 30)))
    texto_vida_enemigo = Text(text=str(vida), origin=(0, 0), scale=2, position=(0, 0.6))
    texto_vida_enemigo.world_parent = enemigo
    enemigos.append((enemigo, texto_vida_enemigo))
    vidas[enemigo] = vida

# Crear algunos enemigos iniciales
for i in range(5):
    crear_enemigo()

# === Timer para generar nuevos enemigos ===
tiempo_generacion = 0
intervalo_generacion = 3  # cada 3 segundos aparece uno nuevo

# === Actualización principal ===
def update():
    global player_vida, tiempo_generacion

    # Movimiento espacial
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
    for bala in balas[:]:
        bala.position += bala.velocity * time.dt

        # Colisiones con enemigos
        for enemigo, texto_vida_enemigo in enemigos[:]:
            if distance(bala, enemigo) < (enemigo.scale_x / 2 + bala.scale_x):
                daño = random.randint(10, 30)
                vidas[enemigo] -= daño
                texto_vida_enemigo.text = str(vidas[enemigo])
                destroy(bala)
                if bala in balas:
                    balas.remove(bala)
                if vidas[enemigo] <= 0:
                    destroy(enemigo)
                    destroy(texto_vida_enemigo)
                    enemigos.remove((enemigo, texto_vida_enemigo))
                break

    # Enemigos que se acercan al jugador
    for enemigo, texto_vida_enemigo in enemigos[:]:
        direccion = (player.position - enemigo.position).normalized()
        enemigo.position += direccion * time.dt * random.uniform(1.5, 3)

        # Si tocan al jugador, le bajan vida
        if distance(player, enemigo) < (enemigo.scale_x / 2 + player.scale_x / 2):
            player_vida -= random.randint(5, 10)
            texto_vida.text = f"Vida: {player_vida}"
            destroy(enemigo)
            destroy(texto_vida_enemigo)
            enemigos.remove((enemigo, texto_vida_enemigo))
            if player_vida <= 0:
                print("💀 GAME OVER 💀")
                application.pause()

    # Generar nuevos enemigos con el tiempo
    tiempo_generacion += time.dt
    if tiempo_generacion >= intervalo_generacion:
        crear_enemigo()
        tiempo_generacion = 0


def input(key):
    if key == 'left mouse down':
        disparar()

app.run()
