from ursina import *
import random

app = Ursina()

window.title = "Recolecta las Estrellas!"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.color = color.rgb(20, 20, 40)

# Jugador (cubo)
player = Entity(model='cube', color=color.azure, scale=1, position=(0,0,0))
speed = 5

# Suelo
ground = Entity(model='plane', scale=(20,1,20), color=color.light_gray, collider='box', y=-1)

# Estrellas para recolectar
stars = []
score = 0
txt_score = Text(text=f"Puntos: {score}", position=(-0.85, 0.45), scale=2, color=color.yellow)

def spawn_star():
    x = random.uniform(-8,8)
    z = random.uniform(-8,8)
    star = Entity(model='sphere', color=color.gold, scale=0.5, position=(x,0.5,z), collider='sphere')
    stars.append(star)

for i in range(5):
    spawn_star()

def update():
    global score
    # movimiento del jugador
    move = Vec3(held_keys['d'] - held_keys['a'], 0, held_keys['w'] - held_keys['s'])
    player.position += move * time.dt * speed

    # colisión con estrellas
    for star in stars[:]:
        if distance(player, star) < 1:
            destroy(star)
            stars.remove(star)
            score += 1
            txt_score.text = f"Puntos: {score}"
            spawn_star()  # genera otra estrella

    # asegurarse de que el jugador no se salga del área
    player.x = clamp(player.x, -9, 9)
    player.z = clamp(player.z, -9, 9)

def input(key):
    if key == 'escape':
        application.quit()

app.run()
