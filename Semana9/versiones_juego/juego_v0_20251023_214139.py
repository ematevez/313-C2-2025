# Versión 0
# Generado: 2025-10-23 21:41:39
# Mejora: Versión inicial
# ============================================

import pygame
import random

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Evolutivo")
reloj = pygame.time.Clock()

# Jugador
jugador = pygame.Rect(ANCHO//2, ALTO//2, 30, 30)
velocidad = 5

# Juego principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    # Controles
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.x > 0:
        jugador.x -= velocidad
    if teclas[pygame.K_RIGHT] and jugador.x < ANCHO - jugador.width:
        jugador.x += velocidad
    if teclas[pygame.K_UP] and jugador.y > 0:
        jugador.y -= velocidad
    if teclas[pygame.K_DOWN] and jugador.y < ALTO - jugador.height:
        jugador.y += velocidad
    
    # Dibujar
    pantalla.fill((0, 0, 0))
    pygame.draw.rect(pantalla, (0, 255, 0), jugador)
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
