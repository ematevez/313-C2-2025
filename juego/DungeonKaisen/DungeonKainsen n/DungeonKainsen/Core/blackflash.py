# core/blackflash.py
# Flash effect utility used for critical hits / special effects.
import pygame

class FlashEffect:
    def __init__(self, duracion=200):
        self.active = False
        self.start_time = 0
        self.duracion = duracion  # ms

    def trigger(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def draw(self, screen):
        if self.active:
            now = pygame.time.get_ticks()
            if now - self.start_time < self.duracion:
                flash_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                flash_surface.fill((80, 0, 40, 150))
                screen.blit(flash_surface, (0, 0))
            else:
                self.active = False