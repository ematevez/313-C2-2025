import pygame
class DeathScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_big = pygame.font.SysFont("arial", 64)
        self.font = pygame.font.SysFont("arial", 32)
        self.selected = 0
        self.options = ["Reanudar (Reaparecer)", "Volver al Menú"]
        self.final_font = pygame.font.SysFont("arial", 40)

    def draw(self, screen):
        # Fondo semi-transparente
        s = pygame.Surface((self.width, self.height))
        s.set_alpha(180)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))

        text = self.font_big.render("HAS MUERTO", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 3))
        screen.blit(text, text_rect)

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (180, 180, 180)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 50))
            screen.blit(text, text_rect)

    def draw_final(self, screen):
        s = pygame.Surface((self.width, self.height))
        s.set_alpha(220)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))
        title = self.final_font.render("GAME OVER", True, (255, 80, 80))
        title_rect = title.get_rect(center=(self.width//2, self.height//2 - 40))
        screen.blit(title, title_rect)
        subtitle = self.font.render("Te has quedado sin vidas. Volviendo al menú...", True, (220,220,220))
        subtitle_rect = subtitle.get_rect(center=(self.width//2, self.height//2 + 30))
        screen.blit(subtitle, subtitle_rect)