import pygame
import random
import sys

# Inicialización
pygame.init()
ANCHO, ALTO = 600, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego con listas - Dispara y esquiva")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (200, 0, 0)
VERDE = (0, 200, 0)

# Jugador
jugador = pygame.Rect(50, ALTO//2, 40, 40)
velocidad_jugador = 5

# Balas
balas = []
velocidad_bala = 7

# Enemigos
enemigos = []
velocidad_enemigo = 3
spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_event, 1500)

# Función para disparar
def disparar(x, y):
    bala = pygame.Rect(x + 40, y + 15, 10, 5)
    balas.append(bala)

# Función para crear enemigo
def crear_enemigo():
    y = random.randint(0, ALTO - 40)
    enemigo = pygame.Rect(ANCHO - 40, y, 40, 40)
    enemigos.append(enemigo)

# Bucle principal
reloj = pygame.time.Clock()
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                disparar(jugador.x, jugador.y)
        if evento.type == spawn_event:
            crear_enemigo()

    # Movimiento jugador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] and jugador.y > 0:
        jugador.y -= velocidad_jugador
    if teclas[pygame.K_DOWN] and jugador.y < ALTO - 40:
        jugador.y += velocidad_jugador

    # Movimiento balas
    for bala in balas[:]:
        bala.x += velocidad_bala
        if bala.x > ANCHO:
            balas.remove(bala)

    # Movimiento enemigos
    for enemigo in enemigos[:]:
        enemigo.x -= velocidad_enemigo
        if enemigo.x < 0:
            enemigos.remove(enemigo)

    # Colisiones
    for bala in balas[:]:
        for enemigo in enemigos[:]:
            if bala.colliderect(enemigo):
                balas.remove(bala)
                enemigos.remove(enemigo)
                break

    # Dibujar
    ventana.fill(NEGRO)
    pygame.draw.rect(ventana, VERDE, jugador)
    for bala in balas:
        pygame.draw.rect(ventana, BLANCO, bala)
    for enemigo in enemigos:
        pygame.draw.rect(ventana, ROJO, enemigo)

    pygame.display.flip()
    reloj.tick(30)
