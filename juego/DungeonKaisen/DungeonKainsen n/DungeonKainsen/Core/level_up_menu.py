# core/level_up_menu.py
import pygame

WHITE = (255,255,255)
BG = (30,30,50)
HIGHLIGHT = (80,80,180)

# Mostrar nombres con acentos (coincide con CharacterCreator y StatsUI)
STATS_DISPLAY = ["Fuerza", "Destreza", "Constitución", "Inteligencia", "Sabiduría", "Carisma"]
DISPLAY_TO_ATTR = {
    "Fuerza": "fuerza",
    "Destreza": "destreza",
    "Constitución": "constitucion",
    "Inteligencia": "inteligencia",
    "Sabiduría": "sabiduria",
    "Carisma": "carisma",
}

class LevelUpMenu:
    """Menú que aparece al subir nivel o matar enemigo, permite mejorar stats."""
    def __init__(self, player):
        self.player = player
        self.active = False
        self.selected = 0
        self.stats = STATS_DISPLAY
        self.font = pygame.font.SysFont("arial", 28)

    def open(self):
        self.active = True
        self.selected = 0

    def handle_event(self, event):
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.stats)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.stats)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.apply_stat(self.selected)
                self.active = False

    def apply_stat(self, idx):
        """Aumenta la stat seleccionada +1 y aplica efectos."""
        stat_label = self.stats[idx]
        attr = DISPLAY_TO_ATTR.get(stat_label, stat_label.lower())

        # subimos la stat y actualizamos propiedades relacionadas
        current = getattr(self.player, attr, 0)
        setattr(self.player, attr, current + 1)

        # efectos especiales para ciertas stats
        if attr == "constitucion":
            # Recalcular hp máximo usando jugador.actualizar_stats si existe
            try:
                self.player.actualizar_stats()
                # curar un poco al subir constitución
                self.player.hp = min(self.player.max_hp, self.player.hp + 2)
            except Exception:
                # fallback simple si no existe actualizar_stats
                try:
                    self.player.max_hp += 2
                    self.player.hp = min(self.player.max_hp, self.player.hp + 2)
                except Exception:
                    pass
        else:
            # para otras stats, intentar recalcular derivadas también
            try:
                self.player.actualizar_stats()
            except Exception:
                pass

    def draw(self, screen):
        if not self.active:
            return
        w, h = 400, 300
        x = screen.get_width()//2 - w//2
        y = screen.get_height()//2 - h//2
        pygame.draw.rect(screen, BG, (x,y,w,h))
        pygame.draw.rect(screen, WHITE, (x,y,w,h),3)
        for i, stat in enumerate(self.stats):
            color = HIGHLIGHT if i==self.selected else WHITE
            text = self.font.render(stat, True, color)
            screen.blit(text, (x+30, y+30 + i*40))