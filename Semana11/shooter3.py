from ursina import *
import random

app = Ursina()

window.title = "Shooter Espacial 3D"
window.color = color.black
camera.fov = 90

# === Jugador ===
player = Entity(model='sphere', color=color.azure, scale=0.6, position=(0,0,0))
camera.parent = player
camera.position = (0, 1.5, -3)
camera.rotation = (0, 0, 0)

speed = 5
vida_jugador = 100
texto_vida = Text(text=f"Vida: {vida_jugador}", scale=2, x=-0.85, y=0.45, color=color.cyan)

# === Balas ===
balas = []

def disparar():
    offset_x = random.uniform(-0.05, 0.05)
    offset_y = random.uniform(-0.05, 0.05)
    direccion = Vec3(camera.forward.x + offset_x, camera.forward.y + offset_y, camera.forward.z)
    bala = Entity(model='sphere', color=color.yellow, scale=0.1, position=player.world_position + camera.forward * 1.5)
    bala.velocity = direccion * 20
    balas.append(bala)

# === Enemigos ===
enemigos = []
vidas_enemigos = {}

def crear_enemigo():
    tamaño = random.uniform(0.5, 2)
    vida = int(tamaño * 50)
    enemigo = Entity(
        model='sphere',
        color=color.red,
        scale=tamaño,
        position=(random.uniform(-20, 20), random.uniform(-5, 5), random.uniform(5, 30))
    )
    texto = Text(text=str(vida), scale=2, world_parent=enemigo, position=(0, 0.7, 0), color=color.white)
    enemigos.append((enemigo, texto))
    vidas_enemigos[enemigo] = vida

for _ in range(7):
    crear_enemigo()

# === Funciones ===
def update():
    global vida_jugador

    # Movimiento libre en el espacio
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
        # Si la bala se aleja mucho, se destruye
        if distance(bala, player) > 50:
            destroy(bala)
            balas.remove(bala)
            continue

        # Colisión con enemigos
        for enemigo, texto in enemigos[:]:
            if distance(bala, enemigo) < (enemigo.scale_x / 2 + bala.scale_x):
                vidas_enemigos[enemigo] -= random.randint(10, 30)
                texto.text = str(vidas_enemigos[enemigo])
                destroy(bala)
                balas.remove(bala)
                if vidas_enemigos[enemigo] <= 0:
                    destroy(enemigo)
                    destroy(texto)
                    enemigos.remove((enemigo, texto))
                break

    # Movimiento de enemigos hacia el jugador
    for enemigo, texto in enemigos:
        direccion = (player.position - enemigo.position).normalized()
        enemigo.position += direccion * time.dt * random.uniform(1, 2)

        # Rotación y actualización de vida visible
        enemigo.rotation_y += time.dt * 40
        texto.position = (0, enemigo.scale_y * 0.7, 0)

        # Si colisionan con el jugador
        if distance(player, enemigo) < (enemigo.scale_x / 2 + player.scale_x):
            vida_jugador -= 20 * time.dt
            texto_vida.text = f"Vida: {int(vida_jugador)}"
            player.color = color.red if int(time.time() * 10) % 2 == 0 else color.azure

    # Si el jugador muere
    if vida_jugador <= 0:
        Text(text="💀 GAME OVER 💀", scale=4, origin=(0,0), color=color.red)
        application.pause()

def input(key):
    if key == 'left mouse down':
        disparar()

app.run()
