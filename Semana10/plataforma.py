import pygame
import sys

# Inicializar pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
GREEN = (50, 200, 50)
RED = (255, 50, 50)
YELLOW = (255, 220, 50)

# Configurar pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Plataformas")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Física
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 15
        self.gravity = 0.8
        self.on_ground = False
        
    def update(self, platforms):
        # Movimiento horizontal
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            
        # Salto
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
        
        # Aplicar gravedad
        self.vel_y += self.gravity
        
        # Limitar velocidad de caída
        if self.vel_y > 20:
            self.vel_y = 20
        
        # Mover horizontalmente
        self.rect.x += self.vel_x
        self.check_collision_x(platforms)
        
        # Mover verticalmente
        self.rect.y += self.vel_y
        self.on_ground = False
        self.check_collision_y(platforms)
        
        # Mantener en pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            
        # Morir si cae
        if self.rect.top > HEIGHT:
            self.rect.x = 100
            self.rect.y = 100
            self.vel_y = 0
    
    def check_collision_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:  # Moviendo a la derecha
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:  # Moviendo a la izquierda
                    self.rect.left = platform.rect.right
    
    def check_collision_y(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Cayendo
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Saltando
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=GREEN):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def main():
    # Crear jugador
    player = Player(100, 100)
    
    # Crear plataformas
    platforms = pygame.sprite.Group()
    platforms.add(Platform(0, HEIGHT - 40, WIDTH, 40))  # Suelo
    platforms.add(Platform(200, 450, 200, 20))
    platforms.add(Platform(500, 350, 150, 20))
    platforms.add(Platform(150, 300, 150, 20))
    platforms.add(Platform(450, 200, 200, 20))
    platforms.add(Platform(100, 150, 100, 20))
    platforms.add(Platform(600, 150, 150, 20))
    
    # Crear monedas
    coins = pygame.sprite.Group()
    coins.add(Coin(300, 400))
    coins.add(Coin(570, 300))
    coins.add(Coin(220, 250))
    coins.add(Coin(520, 150))
    coins.add(Coin(670, 100))
    
    score = 0
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        clock.tick(FPS)
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Actualizar
        player.update(platforms)
        
        # Recoger monedas
        collected_coins = pygame.sprite.spritecollide(player, coins, True)
        score += len(collected_coins)
        
        # Dibujar
        screen.fill(BLACK)
        
        platforms.draw(screen)
        coins.draw(screen)
        screen.blit(player.image, player.rect)
        
        # Mostrar puntuación
        score_text = font.render(f"Monedas: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Instrucciones
        inst_font = pygame.font.Font(None, 24)
        inst_text = inst_font.render("WASD/Flechas para mover | ESPACIO para saltar | ESC para salir", True, WHITE)
        screen.blit(inst_text, (WIDTH // 2 - inst_text.get_width() // 2, HEIGHT - 25))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()