import pygame
import random
import time

# ---------- LÓGICA ----------
class Personaje:
    def __init__(self, nombre, vida, ataque, defensa, crit=0.1):
        self.nombre = nombre
        self.max_vida = vida
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa
        self.crit_chance = crit

    def esta_vivo(self):
        return self.vida > 0

    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0
        return not self.esta_vivo()

    def calcular_daño(self, otro):
        base = self.ataque - otro.defensa
        base = max(1, base)
        # variación aleatoria
        variacion = random.randint(-2, 3)
        dano = max(1, base + variacion)
        # crítico
        if random.random() < self.crit_chance:
            dano = int(dano * 1.8)
            crit = True
        else:
            crit = False
        return dano, crit

    def atacar(self, otro):
        dano, crit = self.calcular_daño(otro)
        muerto = otro.recibir_daño(dano)
        return dano, crit, muerto

# ---------- PYGAME ----------
pygame.init()
WIDTH, HEIGHT = 900, 520
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Batalla OOP - Solución")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 48)

# Colors
BG = (18, 18, 30)
PLAYER_COLOR = (50, 130, 230)
ENEMY_COLOR = (200, 80, 80)

# Crear personajes
jugador = Personaje("Heroe", 120, 20, 4, crit=0.12)
enemigo = Personaje("Orco", 90, 16, 3, crit=0.08)

mensajes = []
turno_jugador = True
delay_action = 0.0
flash_effects = []  # (rect, color, ttl)

def dibujar_barra_vida(x, y, w, h, current, maximum):
    ratio = current / maximum if maximum>0 else 0
    # fondo
    pygame.draw.rect(screen, (80,80,80), (x, y, w, h))
    # color escala de verde a rojo
    green = int(200 * ratio)
    red = 200 - green
    pygame.draw.rect(screen, (red, green, 0), (x, y, int(w*ratio), h))
    pygame.draw.rect(screen, (255,255,255), (x, y, w, h), 2)

def draw_text_center(text, x, y, size=28, color=(255,255,255)):
    f = pygame.font.SysFont(None, size)
    img = f.render(text, True, color)
    r = img.get_rect(center=(x,y))
    screen.blit(img, r)

def aplicar_flash(rect, color=(255,255,255), ttl=0.12):
    flash_effects.append([rect, color, ttl])

def reiniciar():
    global jugador, enemigo, mensajes, turno_jugador
    jugador = Personaje("Heroe", 120, 20, 4, crit=0.12)
    enemigo = Personaje("Orco", 90, 16, 3, crit=0.08)
    mensajes = []
    turno_jugador = True

running = True
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and turno_jugador and jugador.esta_vivo() and enemigo.esta_vivo():
                dano, crit, muerto = jugador.atacar(enemigo)
                msg = f"{jugador.nombre} ataca y causa {dano} daño"
                if crit:
                    msg += " (CRÍTICO!)"
                mensajes.append(msg)
                # flash en enemigo
                aplicar_flash(pygame.Rect(540,150,160,160), (255,200,200), 0.18)
                turno_jugador = False
                delay_action = 0.6
            if event.key == pygame.K_r:
                reiniciar()

    # lógica del retardo y respuesta del enemigo
    if not turno_jugador:
        delay_action -= dt
        if delay_action <= 0:
            if enemigo.esta_vivo() and jugador.esta_vivo():
                dano, crit, muerto = enemigo.atacar(jugador)
                msg = f"{enemigo.nombre} contraataca y causa {dano} daño"
                if crit:
                    msg += " (CRÍTICO!)"
                mensajes.append(msg)
                aplicar_flash(pygame.Rect(100,150,160,160), (200,200,255), 0.14)
            turno_jugador = True

    # actualizar flashes
    for f in flash_effects[:]:
        f[2] -= dt
        rect, color, ttl = f
        if f[2] <= 0:
            flash_effects.remove(f)

    # Dibujado
    screen.fill(BG)
    # personajes (rects)
    player_rect = pygame.Rect(100,150,160,160)
    enemy_rect = pygame.Rect(540,150,160,160)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    pygame.draw.rect(screen, ENEMY_COLOR, enemy_rect)

    # aplicar flashes (si hay)
    for rect, color, ttl in flash_effects:
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((*color, 120))
        screen.blit(s, (rect.x, rect.y))

    # Barras de vida
    dibujar_barra_vida(60, 330, 260, 24, jugador.vida, jugador.max_vida)
    dibujar_barra_vida(520, 330, 260, 24, enemigo.vida, enemigo.max_vida)

    # Nombres y vidas
    draw_text_center(f"{jugador.nombre}  {jugador.vida}/{jugador.max_vida}", 180, 300)
    draw_text_center(f"{enemigo.nombre}  {enemigo.vida}/{enemigo.max_vida}", 660, 300)

    # Mensajes (últimos 5)
    yy = 30
    for m in mensajes[-5:]:
        txt = font.render(m, True, (220,220,220))
        screen.blit(txt, (20, yy))
        yy += 24

    # Indicadores
    if not jugador.esta_vivo():
        draw_text_center("Has muerto. Presiona R para reiniciar", WIDTH//2, HEIGHT//2, size=42, color=(255,80,80))
    elif not enemigo.esta_vivo():
        draw_text_center("Has ganado! Presiona R para reiniciar", WIDTH//2, HEIGHT//2, size=42, color=(80,255,80))
    else:
        draw_text_center("Presiona SPACE para atacar", WIDTH//2, 480-20)

    pygame.display.flip()

pygame.quit()

