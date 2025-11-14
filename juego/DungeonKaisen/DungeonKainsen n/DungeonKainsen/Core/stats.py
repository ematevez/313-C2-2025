# core/stats.py
# UI para subir/ver stats — usa un mapeo entre nombres "visibles" y atributos internos
import pygame

# Nombres para mostrar (coinciden con CharacterCreator)
STAT_DISPLAY = ["Fuerza", "Destreza", "Constitución", "Inteligencia", "Sabiduría", "Carisma"]

# Mapear nombre visible -> atributo interno del Player (sin tildes)
DISPLAY_TO_ATTR = {
    "Fuerza": "fuerza",
    "Destreza": "destreza",
    "Constitución": "constitucion",
    "Inteligencia": "inteligencia",
    "Sabiduría": "sabiduria",
    "Carisma": "carisma",
}

class StatsUI:
    def __init__(self, player):
        self.player = player
        self.selected = 0
        self.points_to_allocate = 2  # puntos que das por enemigo (puedes ajustarlo dinámicamente)
        self.font = pygame.font.SysFont("arial", 22)

    def draw(self, screen):
        x, y = 100, 100
        pygame.draw.rect(screen, (30,30,30), (x-10, y-10, 400, 300))
        title = self.font.render("Sube tus stats", True, (255,255,255))
        screen.blit(title, (x, y))
        y += 40

        for i, stat_label in enumerate(STAT_DISPLAY):
            color = (255,255,0) if i == self.selected else (255,255,255)
            attr = DISPLAY_TO_ATTR.get(stat_label, stat_label.lower())
            val = getattr(self.player, attr, 0)
            text = self.font.render(f"{stat_label}: {val}", True, color)
            screen.blit(text, (x, y))
            y += 30

        info = self.font.render(f"Puntos disponibles: {self.points_to_allocate}", True, (200,200,200))
        screen.blit(info, (x, y + 10))

    def handle_input(self, keys):
        """
        keys: resultado de pygame.key.get_pressed()
        Uso simple: flechas para moverse y ENTER para asignar.
        """
        if self.points_to_allocate <= 0:
            return

        if keys[pygame.K_UP]:
            self.selected = (self.selected - 1) % len(STAT_DISPLAY)
        elif keys[pygame.K_DOWN]:
            self.selected = (self.selected + 1) % len(STAT_DISPLAY)
        elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            stat_label = STAT_DISPLAY[self.selected]
            attr = DISPLAY_TO_ATTR.get(stat_label, stat_label.lower())
            current = getattr(self.player, attr, 0)
            setattr(self.player, attr, current + 1)
            # si el jugador tiene método para recalc stats, llamarlo
            try:
                self.player.actualizar_stats()
            except Exception:
                pass
            self.points_to_allocate -= 1