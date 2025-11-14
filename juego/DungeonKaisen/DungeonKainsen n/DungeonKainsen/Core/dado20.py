# core/dado20.py (kept but minor cleanups)
import pygame
import random
import math

class DiceUI:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.resultado = 0
        self.mensaje = ""
        self.font_big = pygame.font.SysFont("fancy", 60)
        self.font_small = pygame.font.SysFont("arial", 20)
        self.font_result = pygame.font.SysFont("arial", 24, bold=True)
        self.damage_dice = 6
        self.available_dice = [4, 6, 10, 12]
        self.last_roll_time = 0
        self.roll_animating = False
        self.roll_value = 0

    def update(self, resultado, mensaje):
        self.resultado = resultado
        self.mensaje = mensaje
        self.last_roll_time = pygame.time.get_ticks()
        self.roll_animating = True

    def set_damage_dice_by_key(self, key):
        if key == pygame.K_1:
            self.damage_dice = 4
        elif key == pygame.K_2:
            self.damage_dice = 6
        elif key == pygame.K_3:
            self.damage_dice = 10
        elif key == pygame.K_4:
            self.damage_dice = 12

    def roll_damage(self, critical=False):
        base = random.randint(1, self.damage_dice)
        if critical:
            base += random.randint(1, self.damage_dice)
        return base

    def draw(self, screen):
        pygame.draw.rect(screen, (30, 30, 80), (self.x, self.y, 250, 110))
        text = self.font_big.render(f"D20: {self.resultado}", True, (255, 255, 255))
        msg = self.font_small.render(self.mensaje, True, (255, 200, 80))
        screen.blit(text, (self.x + 10, self.y + 5))
        screen.blit(msg, (self.x + 10, self.y + 75))

        start_y = self.y + 130
        start_x = self.x + 10
        spacing = 80

        for i, sides in enumerate(self.available_dice):
            color = (255, 255, 0) if sides == self.damage_dice else (160, 160, 160)
            cx = start_x + i * spacing + 30
            cy = start_y + 40

            if sides == 4:
                self._draw_d4(screen, cx, cy, color)
            elif sides == 6:
                self._draw_d6(screen, cx, cy, color)
            elif sides == 10:
                self._draw_d10(screen, cx, cy, color)
            elif sides == 12:
                self._draw_d12(screen, cx, cy, color)

            text_surface = self.font_result.render(f"D{sides}", True, color)
            tw, th = text_surface.get_size()
            screen.blit(text_surface, (cx - tw//2, cy - th//2))

        active = self.font_small.render(f"Dado actual: D{self.damage_dice}", True, (255, 255, 255))
        screen.blit(active, (self.x + 10, start_y + 80))

    def _draw_d4(self, screen, cx, cy, color):
        size = 26
        pts = [(cx, cy - size), (cx - size, cy + size), (cx + size, cy + size)]
        pygame.draw.polygon(screen, color, pts, 2)

    def _draw_d6(self, screen, cx, cy, color):
        size = 28
        rect = pygame.Rect(cx - size, cy - size, size * 2, size * 2)
        pygame.draw.rect(screen, color, rect, 2)

    def _draw_d10(self, screen, cx, cy, color):
        size = 28
        pts = [
            (cx, cy - size),
            (cx - size * 0.8, cy - size * 0.3),
            (cx - size * 0.6, cy + size * 0.9),
            (cx, cy + size * 1.1),
            (cx + size * 0.6, cy + size * 0.9),
            (cx + size * 0.8, cy - size * 0.3),
        ]
        pygame.draw.polygon(screen, color, pts, 2)

    def _draw_d12(self, screen, cx, cy, color):
        size = 30
        pts = []
        for i in range(12):
            ang = math.radians(30 * i)
            px = cx + math.cos(ang) * size
            py = cy + math.sin(ang) * size
            pts.append((px, py))
        pygame.draw.polygon(screen, color, pts, 2)