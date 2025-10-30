from ursina import *
from random import uniform

app = Ursina()

window.title = "Snow Bros 3D"
window.borderless = False
window.fullscreen = False
window.color = color.azure

# --- Escenario ---
ground = Entity(model='plane', scale=(20, 1, 20), texture='white_cube', texture_scale=(20,20), collider='box', color=color.light_gray)
wall_left = Entity(model='cube', scale=(1, 5, 20), position=(-10, 2.5, 0), collider='box', color=color.gray)
wall_right = Entity(model='cube', scale=(1, 5, 20), position=(10, 2.5, 0), collider='box', color=color.gray)

# --- Jugador ---
player = Entity(model='cube', color=color.orange, scale_y=2, collider='box', position=(0, 1, 0))
camera.parent = player
camera.position = (0, 2, -8)
camera.rotation_x = 15

speed = 5
jump_height = 0.3
is_jumping = False
gravity = -0.5
velocity_y = 0

# --- Lista de bolas de nieve ---
snowballs = []

# --- Enemigos ---
enemies = []
for i in range(3):
    e = Entity(model='cube', color=color.red, scale=(1,2,1), position=(uniform(-8,8),1,uniform(-8,8)), collider='box')
    e.direction = 1
    enemies.append(e)

def input(key):
    global is_jumping, velocity_y

    if key == 'space' and not is_jumping:
        is_jumping = True
        velocity_y = jump_height

    if key == 'left mouse down':
        snowball = Entity(model='sphere', color=color.white, scale=0.5, position=player.position + Vec3(0,1,1), collider='sphere')
        snowball.direction = Vec3(0,0,1)
        snowballs.append(snowball)
        Audio('assets/snowball.wav', autoplay=True) if os.path.exists('assets/snowball.wav') else None

def update():
    global is_jumping, velocity_y

    # --- Movimiento jugador ---
    move_x = held_keys['d'] - held_keys['a']
    move_z = held_keys['w'] - held_keys['s']
    player.x += move_x * time.dt * speed
    player.z += move_z * time.dt * speed

    # --- Gravedad y salto ---
    if is_jumping:
        player.y += velocity_y
        velocity_y += gravity * time.dt
        if player.y <= 1:
            player.y = 1
            is_jumping = False

    # --- Mover bolas de nieve ---
    for snowball in snowballs[:]:
        snowball.z += snowball.direction.z * time.dt * 10
        # Colisión con enemigos
        for e in enemies:
            if snowball.intersects(e).hit:
                e.color = color.cyan
                enemies.remove(e)
                destroy(e)
                destroy(snowball)
                snowballs.remove(snowball)
                break
        if abs(snowball.z) > 20:
            destroy(snowball)
            snowballs.remove(snowball)

    # --- Movimiento enemigos ---
    for e in enemies:
        e.x += e.direction * time.dt * 2
        if e.x > 8 or e.x < -8:
            e.direction *= -1

app.run()
