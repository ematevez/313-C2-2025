import pygame
import sys
import random
import math
import os

pygame.init()
pygame.mixer.init()

# Constantes
WIDTH, HEIGHT = 1000, 700
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (180, 20, 20)
DARK_RED = (100, 10, 10)
BLUE = (30, 50, 120)
DARK_BLUE = (15, 25, 60)
GREEN = (20, 120, 40)
DARK_GREEN = (10, 60, 20)
GRAY = (60, 60, 60)
PURPLE = (120, 40, 120)
BLOOD_RED = (139, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dark Hero: Misterio en 60 Segundos")
clock = pygame.time.Clock()

# Variables globales para sonidos e imágenes
sounds = {}
images = {}
textures = {}

def load_wolf3d_assets():
    """
    Carga assets del repositorio Wolfenstein-3D-Clone
    """
    global sounds, images, textures
    
    print("=" * 60)
    print("CARGANDO ASSETS DE WOLFENSTEIN 3D CLONE")
    print("=" * 60)
    print("Buscando assets en múltiples ubicaciones posibles...")
    
    # Múltiples rutas posibles para los assets
    base_paths = [
        '',  # Carpeta actual
        './',
        '../',
        'Wolfenstein-3D-Clone/',
        '../Wolfenstein-3D-Clone/',
    ]
    
    # TEXTURAS DE PAREDES
    wall_texture_files = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png']
    
    print("\n📦 Cargando texturas de pared...")
    for i, filename in enumerate(wall_texture_files):
        loaded = False
        for base in base_paths:
            possible_paths = [
                os.path.join(base, 'resources', 'textures', 'wall_textures', filename),
                os.path.join(base, 'textures', 'wall_textures', filename),
                os.path.join(base, 'resources', 'textures', filename),
                os.path.join(base, 'wall_textures', filename),
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    try:
                        texture = pygame.image.load(path).convert()
                        textures[f'wall_{i+1}'] = texture
                        print(f"  ✓ Cargado: {path}")
                        loaded = True
                        break
                    except Exception as e:
                        print(f"  ✗ Error cargando {path}: {e}")
            if loaded:
                break
        
        if not loaded:
            # Crear textura placeholder más detallada
            tex = pygame.Surface((64, 64))
            colors = [DARK_RED, DARK_BLUE, DARK_GREEN, GRAY, (80, 80, 100), (60, 40, 40), (40, 60, 80)]
            base_color = colors[i % len(colors)]
            tex.fill(base_color)
            
            # Añadir detalles
            for _ in range(20):
                x, y = random.randint(0, 63), random.randint(0, 63)
                variation = random.randint(-20, 20)
                detail_color = tuple(max(0, min(255, c + variation)) for c in base_color)
                pygame.draw.circle(tex, detail_color, (x, y), random.randint(2, 5))
            
            textures[f'wall_{i+1}'] = tex
            print(f"  ⚠ Usando placeholder para wall_{i+1}")
    
    # TEXTURAS DE SPRITES
    sprite_files = {
        'enemy': [
            ('npc', 'soldier', '0.png'),
            ('npc', 'soldier', '1.png'),
            ('sprites', 'soldier.png'),
        ],
        'victim': [
            ('npc', 'caco', '0.png'),
            ('npc', 'cyber', '0.png'),
            ('sprites', 'victim.png'),
        ],
        'health': [
            ('item', 'health', '0.png'),
            ('item', 'health.png'),
            ('sprites', 'health.png'),
        ],
        'clue': [
            ('item', 'ammo', '0.png'),
            ('item', 'key', '0.png'),
            ('sprites', 'ammo.png'),
        ],
    }
    
    print("\n👾 Cargando texturas de sprites...")
    for sprite_name, file_options in sprite_files.items():
        loaded = False
        for file_parts in file_options:
            for base in base_paths:
                possible_paths = [
                    os.path.join(base, 'resources', 'textures', 'sprite_textures', *file_parts),
                    os.path.join(base, 'textures', 'sprite_textures', *file_parts),
                    os.path.join(base, 'resources', 'textures', *file_parts),
                    os.path.join(base, 'sprite_textures', *file_parts),
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        try:
                            sprite = pygame.image.load(path).convert_alpha()
                            images[sprite_name] = sprite
                            print(f"  ✓ Cargado {sprite_name}: {path}")
                            loaded = True
                            break
                        except Exception as e:
                            print(f"  ✗ Error cargando {path}: {e}")
                if loaded:
                    break
            if loaded:
                break
        
        if not loaded:
            # Crear sprite placeholder
            surf = pygame.Surface((64, 64), pygame.SRCALPHA)
            if sprite_name == 'enemy':
                pygame.draw.rect(surf, (100, 100, 150), (10, 10, 44, 54))
                pygame.draw.circle(surf, (150, 100, 100), (32, 20), 10)
            elif sprite_name == 'victim':
                pygame.draw.rect(surf, BLOOD_RED, (15, 30, 34, 34))
                pygame.draw.circle(surf, (200, 50, 50), (32, 25), 8)
            elif sprite_name == 'health':
                pygame.draw.polygon(surf, RED, [(32, 10), (45, 25), (32, 40), (19, 25)])
                pygame.draw.rect(surf, RED, (27, 20, 10, 15))
            else:  # clue
                pygame.draw.circle(surf, PURPLE, (32, 32), 15)
                pygame.draw.circle(surf, WHITE, (32, 32), 10, 3)
            
            images[sprite_name] = surf
            print(f"  ⚠ Usando placeholder para {sprite_name}")
    
    # SONIDOS
    sound_files = {
        'player_attack': ['player_attack.wav', 'player_shot.wav', 'shoot.wav'],
        'player_pain': ['player_pain.wav', 'player_hurt.wav', 'pain.wav'],
        'player_death': ['player_death.wav', 'death.wav'],
        'npc_attack': ['npc_attack.wav', 'enemy_attack.wav', 'shot.wav'],
        'npc_pain': ['npc_pain.wav', 'enemy_pain.wav'],
        'npc_death': ['npc_death.wav', 'enemy_death.wav'],
        'door': ['door.wav', 'door_open.wav'],
        'item': ['item.wav', 'pickup.wav', 'collect.wav'],
        'theme': ['theme.ogg', 'theme.mp3', 'music.ogg', 'ambient.ogg'],
    }
    
    print("\n🔊 Cargando sonidos...")
    for sound_name, file_options in sound_files.items():
        loaded = False
        for filename in file_options:
            for base in base_paths:
                possible_paths = [
                    os.path.join(base, 'resources', 'sounds', filename),
                    os.path.join(base, 'sounds', filename),
                    os.path.join(base, 'audio', filename),
                    os.path.join(base, filename),
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        try:
                            if path.endswith(('.ogg', '.mp3')):
                                # Música de fondo
                                pygame.mixer.music.load(path)
                                sounds[sound_name] = 'music'
                                print(f"  ✓ Música cargada: {path}")
                            else:
                                sounds[sound_name] = pygame.mixer.Sound(path)
                                print(f"  ✓ Sonido cargado: {path}")
                            loaded = True
                            break
                        except Exception as e:
                            print(f"  ✗ Error cargando {path}: {e}")
                if loaded:
                    break
            if loaded:
                break
        
        if not loaded:
            sounds[sound_name] = None
            print(f"  ⚠ Sin sonido para {sound_name}")
    
    # Crear imagen de héroe
    hero_surf = pygame.Surface((40, 50), pygame.SRCALPHA)
    pygame.draw.rect(hero_surf, BLUE, (10, 15, 20, 35))
    pygame.draw.polygon(hero_surf, RED, [(5, 10), (35, 10), (38, 35), (2, 35)])
    pygame.draw.circle(hero_surf, (255, 200, 150), (20, 12), 8)
    images['hero'] = hero_surf
    
    print("=" * 60)
    print("✓ Carga de assets completada\n")
    print(f"Texturas cargadas: {len(textures)}")
    print(f"Imágenes cargadas: {len(images)}")
    print(f"Sonidos cargados: {sum(1 for s in sounds.values() if s is not None)}")
    print("=" * 60 + "\n")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        if images.get('hero'):
            self.image = pygame.transform.scale(images['hero'], (40, 50))
        else:
            self.image = pygame.Surface((40, 50))
            self.image.fill(BLUE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 7
        self.jump_power = 18  # Aumentado para llegar mejor a las plataformas
        self.gravity = 0.9
        self.on_ground = False
        self.facing_right = True
        self.health = 100
        
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True
            
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
            play_sound('player_attack')
        
        # Aplicar gravedad
        self.vel_y += self.gravity
        
        # Limitar velocidad de caída
        if self.vel_y > 25:
            self.vel_y = 25
        
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
        
        # Morir si cae fuera
        if self.rect.top > HEIGHT:
            self.health = 0
    
    def check_collision_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
    
    def check_collision_y(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
    
    def take_damage(self, amount):
        self.health -= amount
        play_sound('player_pain')
        if self.health <= 0:
            play_sound('player_death')

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, texture_key=None):
        super().__init__()
        self.width = width
        self.height = height
        
        if texture_key and textures.get(texture_key):
            base_texture = textures[texture_key]
            self.image = pygame.Surface((width, height))
            
            # Tile la textura
            tex_w, tex_h = base_texture.get_size()
            for i in range(0, width, tex_w):
                for j in range(0, height, tex_h):
                    self.image.blit(base_texture, (i, j))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(DARK_RED)
            # Añadir borde para visibilidad
            pygame.draw.rect(self.image, RED, (0, 0, width, height), 2)
        
        self.image.set_alpha(220)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Clue(pygame.sprite.Sprite):
    def __init__(self, x, y, clue_type):
        super().__init__()
        
        if images.get('clue'):
            self.image = pygame.transform.scale(images['clue'], (35, 35))
        else:
            self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
            pygame.draw.circle(self.image, PURPLE, (17, 17), 17)
            pygame.draw.circle(self.image, WHITE, (17, 17), 13, 3)
            pygame.draw.circle(self.image, PURPLE, (17, 17), 8)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clue_type = clue_type
        self.float_offset = random.uniform(0, math.pi * 2)
        self.base_y = y
        
    def update(self):
        self.float_offset += 0.08
        self.rect.y = self.base_y + math.sin(self.float_offset) * 8

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, npc_type):
        super().__init__()
        
        if npc_type == 'victim' and images.get('victim'):
            self.image = pygame.transform.scale(images['victim'], (45, 55))
        elif npc_type == 'enemy' and images.get('enemy'):
            self.image = pygame.transform.scale(images['enemy'], (45, 55))
        else:
            self.image = pygame.Surface((45, 55), pygame.SRCALPHA)
            if npc_type == 'victim':
                pygame.draw.rect(self.image, BLOOD_RED, (5, 10, 35, 45))
            else:
                pygame.draw.rect(self.image, DARK_GREEN, (5, 10, 35, 45))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.npc_type = npc_type
        self.vel_x = random.choice([-1.5, 1.5])
        self.patrol_range = random.randint(80, 150)
        self.start_x = x
        
    def update(self, platforms):
        if self.npc_type == 'enemy':
            self.rect.x += self.vel_x
            
            # Patrullar
            if abs(self.rect.x - self.start_x) > self.patrol_range:
                self.vel_x *= -1
            
            # Colisiones con bordes de pantalla
            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.vel_x *= -1
            
            # Colisiones con plataformas
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.vel_x > 0:
                        self.rect.right = platform.rect.left
                        self.vel_x *= -1
                    elif self.vel_x < 0:
                        self.rect.left = platform.rect.right
                        self.vel_x *= -1

class Enemy(NPC):
    def __init__(self, x, y):
        super().__init__(x, y, 'enemy')
        self.damage = 5
        self.attack_cooldown = 0
        
    def update(self, platforms, player=None):
        super().update(platforms)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Atacar al jugador si está cerca
        if player and self.attack_cooldown == 0:
            dist = math.sqrt((self.rect.centerx - player.rect.centerx)**2 + 
                           (self.rect.centery - player.rect.centery)**2)
            if dist < 60:
                player.take_damage(self.damage)
                play_sound('npc_attack')
                self.attack_cooldown = 90

def generate_level(level_num):
    """Genera niveles proceduralmente con mejor distribución de plataformas"""
    platforms = pygame.sprite.Group()
    clues = pygame.sprite.Group()
    npcs = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    # Seleccionar texturas según nivel
    level_textures = {
        1: ['wall_1', 'wall_2'],
        2: ['wall_3', 'wall_4'],
        3: ['wall_5', 'wall_6'],
    }
    
    textures_for_level = level_textures.get(level_num, ['wall_1'])
    
    # Suelo principal
    platforms.add(Platform(0, HEIGHT - 40, WIDTH, 40, random.choice(textures_for_level)))
    
    # Generar plataformas en capas
    num_platforms = 6 + level_num * 2
    
    # Dividir altura en secciones
    sections = [
        (HEIGHT - 200, HEIGHT - 100),  # Baja
        (HEIGHT - 350, HEIGHT - 200),  # Media
        (HEIGHT - 500, HEIGHT - 350),  # Alta
    ]
    
    for i in range(num_platforms):
        section = sections[i % len(sections)]
        x = random.randint(50, WIDTH - 250)
        y = random.randint(section[0], section[1])
        w = random.randint(100, 220)
        
        # Evitar superposiciones
        valid = True
        new_rect = pygame.Rect(x, y, w, 20)
        for platform in platforms:
            if new_rect.colliderect(platform.rect.inflate(30, 30)):
                valid = False
                break
        
        if valid:
            platforms.add(Platform(x, y, w, 20, random.choice(textures_for_level)))
    
    # Añadir pistas sobre plataformas elevadas
    platform_list = [p for p in platforms if HEIGHT - 500 < p.rect.y < HEIGHT - 80]
    clue_types = ['huella', 'arma', 'nota', 'testigo']
    
    clues_added = 0
    attempts = 0
    while clues_added < 3 and attempts < 20:
        attempts += 1
        if platform_list:
            platform = random.choice(platform_list)
            if platform.rect.width > 50:
                x = platform.rect.x + random.randint(10, max(11, platform.rect.width - 45))
                y = platform.rect.y - 45
                
                # Verificar que no haya otra pista muy cerca
                too_close = False
                for clue in clues:
                    if abs(clue.rect.x - x) < 60 and abs(clue.rect.y - y) < 60:
                        too_close = True
                        break
                
                if not too_close:
                    clues.add(Clue(x, y, random.choice(clue_types)))
                    clues_added += 1
    
    # Añadir víctima
    if platform_list:
        victim_platform = random.choice([p for p in platform_list if p.rect.width > 80])
        npcs.add(NPC(victim_platform.rect.x + 30, victim_platform.rect.y - 60, 'victim'))
    
    # Añadir enemigos
    num_enemies = level_num + 1
    for i in range(num_enemies):
        if platform_list:
            enemy_platform = random.choice([p for p in platform_list if p.rect.width > 100])
            enemy = Enemy(enemy_platform.rect.x + 50, enemy_platform.rect.y - 60)
            enemies.add(enemy)
    
    # Background
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg_colors = [
        (15, 10, 20),   # Mansión oscura
        (10, 15, 25),   # Laboratorio azul
        (10, 20, 10),   # Cementerio verde
    ]
    bg.fill(bg_colors[level_num - 1])
    
    # Añadir estrellas/detalles de fondo
    for _ in range(100):
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT - 100)
        size = random.randint(1, 3)
        brightness = random.randint(100, 200)
        pygame.draw.circle(bg, (brightness, brightness, brightness), (x, y), size)
    
    return platforms, clues, npcs, enemies, bg

def play_sound(sound_key):
    """Helper para reproducir sonidos"""
    if sounds.get(sound_key) and sounds[sound_key] != 'music' and sounds[sound_key] is not None:
        try:
            sounds[sound_key].play()
        except:
            pass

class Game:
    def __init__(self):
        self.state = 'menu'
        self.level = 1
        self.score = 0
        self.time_limit = 60
        self.start_time = 0
        self.clues_collected = 0
        self.clues_needed = 3
        
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.player = None
        self.platforms = None
        self.clues = None
        self.npcs = None
        self.enemies = None
        self.background = None
        
        self.screen_shake = 0
        self.darkness = 0
        
    def start_level(self, level):
        self.level = level
        self.clues_collected = 0
        self.player = Player(100, HEIGHT - 150)
        self.platforms, self.clues, self.npcs, self.enemies, self.background = generate_level(level)
        self.start_time = pygame.time.get_ticks()
        self.state = 'playing'
        
        # Música de fondo
        if sounds.get('theme') == 'music':
            try:
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)
            except:
                pass
    
    def update(self):
        if self.state == 'playing':
            self.player.update(self.platforms)
            self.clues.update()
            self.enemies.update(self.platforms, self.player)
            
            # Recoger pistas
            collected = pygame.sprite.spritecollide(self.player, self.clues, True)
            if collected:
                self.clues_collected += len(collected)
                self.score += 100
                play_sound('item')
            
            # Verificar tiempo
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            remaining = self.time_limit - elapsed
            
            if remaining <= 0 or self.player.health <= 0:
                self.state = 'defeat'
                play_sound('player_death')
                try:
                    pygame.mixer.music.stop()
                except:
                    pass
            
            # Verificar victoria
            if self.clues_collected >= self.clues_needed:
                if self.level < 3:
                    self.level += 1
                    self.start_level(self.level)
                else:
                    self.state = 'victory'
                    try:
                        pygame.mixer.music.stop()
                    except:
                        pass
            
            # Efecto de shake
            if random.random() < 0.008:
                self.screen_shake = 8
            
            if self.screen_shake > 0:
                self.screen_shake -= 1
    
    def draw(self):
        offset_x = random.randint(-self.screen_shake, self.screen_shake)
        offset_y = random.randint(-self.screen_shake, self.screen_shake)
        
        if self.state == 'menu':
            screen.fill(BLACK)
            
            title = self.font_large.render("DARK HERO", True, RED)
            subtitle = self.font_medium.render("Misterio en 60 Segundos", True, WHITE)
            inst1 = self.font_small.render("Recolecta 3 pistas antes de que acabe el tiempo", True, WHITE)
            inst2 = self.font_small.render("Evita a los enemigos patrullando", True, GRAY)
            inst3 = self.font_small.render("WASD/Flechas - Mover | ESPACIO - Saltar", True, GRAY)
            inst4 = self.font_medium.render("Presiona ENTER para comenzar", True, GREEN)
            
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
            screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 200))
            screen.blit(inst1, (WIDTH // 2 - inst1.get_width() // 2, 320))
            screen.blit(inst2, (WIDTH // 2 - inst2.get_width() // 2, 370))
            screen.blit(inst3, (WIDTH // 2 - inst3.get_width() // 2, 420))
            screen.blit(inst4, (WIDTH // 2 - inst4.get_width() // 2, 520))
            
        elif self.state == 'playing':
            if self.background:
                screen.blit(self.background, (offset_x, offset_y))
            else:
                screen.fill(BLACK)
            
            self.platforms.draw(screen)
            self.npcs.draw(screen)
            self.enemies.draw(screen)
            self.clues.draw(screen)
            screen.blit(self.player.image, (self.player.rect.x + offset_x, self.player.rect.y + offset_y))
            
            # HUD
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            remaining = max(0, self.time_limit - elapsed)
            
            time_text = self.font_medium.render(f"Tiempo: {int(remaining)}s", True, RED if remaining < 10 else WHITE)
            level_text = self.font_small.render(f"Nivel: {self.level}/3", True, WHITE)
            clues_text = self.font_small.render(f"Pistas: {self.clues_collected}/{self.clues_needed}", True, PURPLE)
            score_text = self.font_small.render(f"Puntos: {self.score}", True, WHITE)
            health_text = self.font_small.render(f"Salud: {max(0, self.player.health)}%", True, RED if self.player.health < 30 else GREEN)
            
            screen.blit(time_text, (WIDTH - 250, 20))
            screen.blit(level_text, (20, 20))
            screen.blit(clues_text, (20, 60))
            screen.blit(score_text, (20, 100))
            screen.blit(health_text, (20, 140))
            
            # Oscurecer cuando queda poco tiempo
            if remaining < 10:
                dark_surf = pygame.Surface((WIDTH, HEIGHT))
                dark_surf.fill(BLACK)
                dark_surf.set_alpha(int((10 - remaining) * 12))
                screen.blit(dark_surf, (0, 0))
        
        elif self.state == 'victory':
            screen.fill(BLACK)
            title = self.font_large.render("¡CASO RESUELTO!", True, GREEN)
            score_text = self.font_medium.render(f"Puntuación Final: {self.score}", True, WHITE)
            inst = self.font_small.render("Presiona ENTER para volver al menú", True, GRAY)
            
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 250))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 350))
            screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, 450))
        
        elif self.state == 'defeat':
            screen.fill(BLACK)
            title = self.font_large.render("MISIÓN FALLIDA", True, RED)
            
            if self.player.health <= 0:
                subtitle = self.font_medium.render("Has sido eliminado...", True, DARK_RED)
            else:
                subtitle = self.font_medium.render("El asesino escapó...", True, DARK_RED)
            
            inst = self.font_small.render("Presiona ENTER para volver al menú", True, GRAY)
            
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 250))
            screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 350))
            screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, 450))
        
        pygame.display.flip()

def main():
    load_wolf3d_assets()
    game = Game()
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.key == pygame.K_RETURN:
                    if game.state == 'menu':
                        game.start_level(1)
                    elif game.state in ['victory', 'defeat']:
                        game.state = 'menu'
                        game.score = 0
                        game.level = 1
        
        game.update()
        game.draw()
    
    try:
        pygame.mixer.music.stop()
    except:
        pass
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()