# game/ui.py
# Contiene utilidades de UI reutilizables: barra de vida y efectos (arm swing) y barra de XP.

import pygame
import time

def draw_health_bar(screen, x, y, current, max_hp, width=120, height=14):
    ratio = max(0, min(current / max_hp, 1)) if max_hp > 0 else 0
    pygame.draw.rect(screen, (80, 20, 20), (x, y, width, height))
    pygame.draw.rect(screen, (220, 40, 40), (x, y, int(width * ratio), height))
    pygame.draw.rect(screen, (255,255,255), (x, y, width, height), 2)

ARM_COLOR = (40, 140, 255)
ARM_DURATION_MS = 220

class ArmEffect:
    def __init__(self, start_pos, end_pos, created_time=None, color=ARM_COLOR, duration_ms=ARM_DURATION_MS):
        self.start = start_pos
        self.end = end_pos
        self.created = created_time if created_time is not None else pygame.time.get_ticks()
        self.duration = duration_ms
        self.color = color

    def alive(self, now):
        return (now - self.created) < self.duration

    def draw(self, screen, camera_offset):
        sx = int(self.start[0] - camera_offset[0])
        sy = int(self.start[1] - camera_offset[1])
        ex = int(self.end[0] - camera_offset[0])
        ey = int(self.end[1] - camera_offset[1])
        elapsed = (pygame.time.get_ticks() - self.created)
        t = max(0.0, min(1.0, elapsed / self.duration))
        width = max(2, int(8 * (1 - t)))
        pygame.draw.line(screen, self.color, (sx, sy), (ex, ey), width)
        pygame.draw.circle(screen, self.color, (ex, ey), max(3, int(6 * (1 - t/1.2))))

# ---------------- XP bar ----------------
def draw_xp_bar(screen, x, y, width, height, current_xp, xp_to_next, level, font):
    """
    Draws an XP bar at (x,y) of size width x height showing current_xp / xp_to_next and level.
    font: a pygame Font to draw text.
    """
    pct = 0.0
    if xp_to_next > 0:
        pct = max(0.0, min(1.0, current_xp / xp_to_next))
    # background
    pygame.draw.rect(screen, (30, 30, 40), (x, y, width, height))
    # filled portion (blue/cyan)
    pygame.draw.rect(screen, (80, 180, 255), (x, y, int(width * pct), height))
    # border
    pygame.draw.rect(screen, (255,255,255), (x, y, width, height), 2)
    # text: Level and percent
    try:
        level_text = font.render(f"Lv {level}", True, (220,220,220))
        screen.blit(level_text, (x + 6, y - level_text.get_height() - 2))
        pct_text = font.render(f"{int(current_xp)}/{int(xp_to_next)} XP", True, (220,220,220))
        # center pct_text in the bar
        tx = x + (width - pct_text.get_width()) // 2
        ty = y + (height - pct_text.get_height()) // 2
        screen.blit(pct_text, (tx, ty))
    except Exception:
        pass