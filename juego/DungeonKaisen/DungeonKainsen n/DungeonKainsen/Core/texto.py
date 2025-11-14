# core/texto.py
import pygame

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color, font=None, lifetime=800):
        super().__init__()
        if font is None:
            self.font = pygame.font.SysFont("arial", 28)
        else:
            self.font = font
        self.text = str(damage)
        self.color = color
        self.image = self.font.render(self.text, True, self.color).convert_alpha()
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.start_time = pygame.time.get_ticks()
        self.lifetime = lifetime
        self.alpha = 255
        self.rise_speed = 1.0

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        self.rect.y -= self.rise_speed
        progress = elapsed / self.lifetime
        if progress >= 1.0:
            self.kill()
            return
        self.alpha = int(255 * (1.0 - progress))
        self.image.set_alpha(self.alpha)