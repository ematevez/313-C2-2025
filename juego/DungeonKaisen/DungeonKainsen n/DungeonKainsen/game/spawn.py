# game/spawn.py
# Lógica de spawn y funciones relacionadas a enemigos.

import random
import math
from Core.enemigo import Enemy

def spawn_random_enemies(game, count, min_size=24, max_size=64, near_player=True):
    """
    Añade 'count' enemigos a game.enemies. Usa game.player para calcular radios seguros.
    """
    safe_radius = 100
    if not hasattr(game, "max_enemies"):
        game.max_enemies = 15
    for _ in range(count):
        if len(game.enemies) >= game.max_enemies:
            break
        size = random.randint(min_size, max_size)
        color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
        angle = random.random() * math.tau
        radius = random.randint(safe_radius + 1, 420)
        if game.player:
            x = int(game.player.rect.centerx + math.cos(angle) * radius)
            y = int(game.player.rect.centery + math.sin(angle) * radius)
        else:
            x = random.randint(0, game.screen.get_width())
            y = random.randint(0, game.screen.get_height())
        try:
            if game.world.is_pixel_solid(x, y):
                continue
        except Exception:
            pass
        enemy = Enemy(x, y, size=size, color=color)
        game.enemies.append(enemy)