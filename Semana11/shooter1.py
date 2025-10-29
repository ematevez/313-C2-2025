# shooter3d_esferas.py
from ursina import *
from random import uniform, randint

app = Ursina()

window.title = "Shooter 3D con Esferas - Ursina"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True
window.color = color.rgb(20, 20, 30)

# 🔹 Jugador
player = Entity(model='sphere', color=color.azure, scale=0.5, position=(0, 0, 0))
camera.parent = player
camera.position = (0, 1, -3)
camera.rotation = (10, 0, 0)
player.speed = 5

# 🔹 Texto en pantalla
vida = 10
puntaje = 0
txt_vida = Text(text=f'VIDA: {vida}', position=(-0.85, 0.45), scale=2)
txt_puntaje = Text(text=f'PUNTAJE: {puntaje}', position=(-0.85, 0.38), scale=2)
txt_mensaje = Text(text='Mover: WASD | Disparar: click | Reiniciar: R', position=(0, 0.45), origin=(0, 0), scale=1)

# 🔹 Listas globales
bullets = []
enemies = []

# 🔹 Crear piso
ground = Entity(model='plane', collider='box', scale=80, texture='white_cube', texture_scale=(80, 80), color=color.rgb(40, 60, 40), y=-2)

# =====================================================
# FUNCIONES
# =====================================================

def spawn_enemy():
    """Crea enemigos con tamaño y vida aleatoria"""
    size = uniform(0.4, 1.5)
    hp = int(size * 10)  # más grande = más vida
    pos = (uniform(-20, 20), uniform(0, 4), uniform(5, 25))
    e = Entity(model='sphere', color=color.red, scale=size, position=pos, collider='sphere')
    e.speed = uniform(1, 3)
    e.hp = hp
    e.txt = Text(text=str(hp), scale=1.5, position=(0, 0), world_parent=e, y=1.3)
    enemies.append(e)

def shoot():
    """Dispara una bala con ligera aleatoriedad"""
    spread_x = uniform(-0.05, 0.05)
    spread_y = uniform(-0.05, 0.05)
    direction = Vec3(spread_x, spread_y, 1).normalized()

    b = Entity(model='sphere', color=color.yellow, scale=0.15,
               position=player.position + Vec3(0, 0.5, 1), collider='sphere')
    b.velocity = direction * 20
    bullets.append(b)

def update():
    global vida, puntaje

    # Movimiento del jugador
    move = Vec3(
        held_keys['d'] - held_keys['a'],
        0,
        held_keys['w'] - held_keys['s']
    ).normalized() * time.dt * player.speed
    player.position += move
    camera.position = player.position + Vec3(0, 1, -3)

    # Actualizar enemigos
    for e in enemies[:]:
        dir_to_player = (player.position - e.position).normalized()
        e.position += dir_to_player * e.speed * time.dt
        e.txt.position = e.world_position + Vec3(0, 1.2, 0)
        e.txt.text = str(e.hp)

        # Si toca al jugador
        if distance(player, e) < 1.0:
            vida -= 1
            txt_vida.text = f'VIDA: {vida}'
            camera.shake()
            destroy(e.txt)
            destroy(e)
            enemies.remove(e)
            if vida <= 0:
                game_over()

    # Actualizar balas
    for b in bullets[:]:
        b.position += b.velocity * time.dt
        # Eliminar si sale lejos
        if abs(b.x) > 40 or abs(b.z) > 40:
            destroy(b)
            bullets.remove(b)
            continue

        # Colisión con enemigos
        for e in enemies[:]:
            if distance(b, e) < (e.scale_x + b.scale_x):
                e.hp -= randint(1, 5)  # daño aleatorio
                if e.hp <= 0:
                    puntaje += 1
                    txt_puntaje.text = f'PUNTAJE: {puntaje}'
                    destroy(e.txt)
                    destroy(e)
                    enemies.remove(e)
                destroy(b)
                bullets.remove(b)
                break

def input(key):
    if key == 'left mouse down':
        shoot()
    if key == 'r':
        restart()

def spawn_cycle():
    spawn_enemy()
    invoke(spawn_cycle, delay=max(0.5, 3 - puntaje * 0.05))

def game_over():
    txt_mensaje.text = f'💀 GAME OVER 💀\nPuntaje: {puntaje}\nPresiona R para reiniciar'
    txt_mensaje.color = color.red
    application.paused = True

def restart():
    global vida, puntaje, bullets, enemies
    for e in enemies:
        destroy(e)
        destroy(e.txt)
    for b in bullets:
        destroy(b)
    enemies.clear()
    bullets.clear()
    vida = 10
    puntaje = 0
    txt_vida.text = f'VIDA: {vida}'
    txt_puntaje.text = f'PUNTAJE: {puntaje}'
    txt_mensaje.text = 'Mover: WASD | Disparar: click | Reiniciar: R'
    txt_mensaje.color = color.white
    application.paused = False

spawn_cycle()
app.run()
