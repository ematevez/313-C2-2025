# shooter2d_ursina.py
from ursina import *
import random, math

app = Ursina()

window.title = "Shooter 2D - Ursina (versión fácil)"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.color = color.rgb(30, 30, 40)

# Jugador
player = Entity(model='circle', color=color.azure, scale=0.4, collider='circle')
player.speed = 5

# UI
vida = 5
puntaje = 0
txt_vida = Text(text=f'Vida: {vida}', position=(-0.85, 0.45), scale=2, background=True)
txt_puntaje = Text(text=f'Puntaje: {puntaje}', position=(-0.85, 0.38), scale=2, background=True)
txt_mensaje = Text(text='Mueve con WASD - Click para disparar', position=(0, 0.45), origin=(0,0), scale=1.2)

bullets = []
enemies = []

def spawn_enemy():
    """Crea un enemigo en una posición aleatoria del borde"""
    side = random.choice(['top','bottom','left','right'])
    if side == 'top':
        pos = (random.uniform(-7,7), 5)
    elif side == 'bottom':
        pos = (random.uniform(-7,7), -5)
    elif side == 'left':
        pos = (-8, random.uniform(-4,4))
    else:
        pos = (8, random.uniform(-4,4))

    enemy = Entity(model='circle', color=color.red, scale=0.4, position=pos, collider='circle')
    enemy.speed = random.uniform(1.0, 2.5)
    enemies.append(enemy)

def input(key):
    if key == 'left mouse down':
        shoot()

def shoot():
    """Crea una bala hacia la dirección del mouse"""
    direction = (mouse.position - player.position).normalized()
    b = Entity(model='circle', color=color.yellow, scale=0.15, position=player.position, collider='circle')
    b.velocity = direction * 10
    bullets.append(b)

def update():
    global vida, puntaje

    # Movimiento del jugador
    move = Vec2(held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s'])
    player.position += move * time.dt * player.speed

    # Enemigos se mueven hacia el jugador
    for e in enemies[:]:
        direction = (player.position - e.position).normalized()
        e.position += direction * e.speed * time.dt

        if distance(player, e) < 0.5:
            vida -= 1
            txt_vida.text = f'Vida: {vida}'
            camera.shake()
            destroy(e)
            enemies.remove(e)
            if vida <= 0:
                game_over()

    # Balas se mueven
    for b in bullets[:]:
        b.position += b.velocity * time.dt
        # eliminar si se sale de la pantalla
        if abs(b.x) > 9 or abs(b.y) > 5:
            destroy(b)
            bullets.remove(b)
            continue

        # colisión con enemigos
        for e in enemies[:]:
            if distance(b, e) < 0.4:
                puntaje += 1
                txt_puntaje.text = f'Puntaje: {puntaje}'
                destroy(e)
                enemies.remove(e)
                destroy(b)
                bullets.remove(b)
                break

def spawn_cycle():
    spawn_enemy()
    invoke(spawn_cycle, delay=max(0.5, 2.5 - puntaje*0.03))

def game_over():
    txt_mensaje.text = f'GAME OVER - Puntaje final: {puntaje}\nPresiona R para reiniciar'
    txt_mensaje.color = color.red
    application.paused = True

def restart():
    global vida, puntaje, enemies, bullets
    for e in enemies: destroy(e)
    for b in bullets: destroy(b)
    enemies.clear(); bullets.clear()
    vida = 5; puntaje = 0
    txt_vida.text = f'Vida: {vida}'
    txt_puntaje.text = f'Puntaje: {puntaje}'
    txt_mensaje.text = 'Mueve con WASD - Click para disparar'
    txt_mensaje.color = color.white
    application.paused = False

def input(key):
    if key == 'r':
        restart()
        
    if key == 'left mouse down':
        shoot()

spawn_cycle()
app.run()
