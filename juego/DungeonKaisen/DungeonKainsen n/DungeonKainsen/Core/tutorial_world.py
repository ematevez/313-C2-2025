import pygame
import time

TILE_SIZE = 32
TILE_WALL = 1
TILE_FLOOR = 0

# Mapa tutorial mucho más grande y con varios pasillos para practicar movimiento y combate.
TUTORIAL_MAP = [
    [1]*40,
]
for i in range(1, 29):
    row = [1]
    for j in range(1, 39):
        if i in (1,28):
            row.append(1)
        elif j in (1,38):
            row.append(1)
        elif i % 5 == 0 and 5 < j < 35:
            row.append(1)
        elif j % 7 == 0 and 5 < i < 25:
            row.append(1)
        else:
            row.append(0)
    row.append(1)
    TUTORIAL_MAP.append(row)
TUTORIAL_MAP.append([1]*40)

class TutorialWorld:
    def __init__(self, tile_size=32):
        self.tile_size = tile_size
        self.width = len(TUTORIAL_MAP[0])
        self.height = len(TUTORIAL_MAP)
        self.objectives = [
            {"text": "¡Bienvenido! Usa WASD o flechas para moverte por el mapa.", "condition": self.moved},
            {"text": "Ahora presiona E para abrir el panel de estadísticas.", "condition": self.opened_stats},
            {"text": "Haz click izquierdo para atacar al dummy (cuadrado rojo).", "condition": self.attacked_dummy},
            {"text": "Presiona T para preguntar al shikigami (IA).", "condition": self.asked_ai},
            {"text": "Ve a la casilla verde para terminar el tutorial.", "condition": self.reached_exit},
        ]
        self.current_objective = 0
        self.last_objective_time = 0
        self.dummy_rect = pygame.Rect(10*TILE_SIZE, 5*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.dummy_alive = True
        self.stats_opened = False
        self.moved_flag = False
        self.attacked_flag = False
        self.asked_flag = False

    def draw(self, screen, camera_offset):
        for y, row in enumerate(TUTORIAL_MAP):
            for x, tile in enumerate(row):
                color = (80,80,80) if tile==TILE_WALL else (220,220,180)
                rect = pygame.Rect(x*self.tile_size - camera_offset[0], y*self.tile_size - camera_offset[1], self.tile_size, self.tile_size)
                pygame.draw.rect(screen, color, rect)

        # Dummy enemigo (rojo)
        if self.dummy_alive:
            pygame.draw.rect(screen, (220,40,40), self.dummy_rect)

        # Salida del tutorial (esquina opuesta)
        exit_rect = pygame.Rect((self.width-3)*self.tile_size, (self.height-3)*self.tile_size, self.tile_size, self.tile_size)
        pygame.draw.rect(screen, (50,255,80), exit_rect)

        self.draw_objective(screen)

    def draw_objective(self, screen):
        font = pygame.font.SysFont("arial", 28)
        if self.current_objective < len(self.objectives):
            msg = self.objectives[self.current_objective]["text"]
            surface = font.render(f"Shikigami: {msg}", True, (180,220,255))
            screen.blit(surface, (40, 920))

    def update(self, player, event, stats_open, fairy_input_active):
        # Detecta movimiento
        if not self.moved_flag and (player.rect.x != 100 or player.rect.y != 100):
            self.moved_flag = True

        # Detecta apertura de stats
        if stats_open:
            self.stats_opened = True

        # Detecta ataque al dummy
        if event and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.dummy_alive and player.rect.colliderect(self.dummy_rect):
                self.dummy_alive = False
                self.attacked_flag = True

        # Detecta pregunta al AI
        if fairy_input_active:
            self.asked_flag = True

        self.check_objective_progress(player)

    def check_objective_progress(self, player):
        if self.current_objective >= len(self.objectives):
            return
        condition = self.objectives[self.current_objective]["condition"]
        if condition(player):
            self.current_objective += 1
            self.last_objective_time = time.time()

    def moved(self, player):
        return self.moved_flag

    def opened_stats(self, player):
        return self.stats_opened

    def attacked_dummy(self, player):
        return self.attacked_flag

    def asked_ai(self, player):
        return self.asked_flag

    def reached_exit(self, player):
        exit_rect = pygame.Rect((self.width-3)*self.tile_size, (self.height-3)*self.tile_size, self.tile_size, self.tile_size)
        return player.rect.colliderect(exit_rect)

    def check_exit(self, player_rect):
        # Permite salir solo si completó todos los objetivos
        if self.current_objective >= len(self.objectives):
            exit_rect = pygame.Rect((self.width-3)*self.tile_size, (self.height-3)*self.tile_size, self.tile_size, self.tile_size)
            return player_rect.colliderect(exit_rect)
        return False
    def is_pixel_solid(self, px, py, check_radius=0):
        tx = int(px // self.tile_size)
        ty = int(py // self.tile_size)
        if 0 <= ty < self.height and 0 <= tx < self.width:
            return TUTORIAL_MAP[ty][tx] == TILE_WALL
        return False