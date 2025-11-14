# core/jugador.py
import pygame
from Core.stats_logic import bonus_constitucion, stat_modifier
from settings import PIXELS_PER_METER

class Player:
    def __init__(self, x, y, camara_offset=(0,0), tipo="humano", lives=3, height_m=1.8):
        pixel_h = max(8, int(round(height_m * PIXELS_PER_METER)))
        pixel_w = max(6, int(round(pixel_h * 0.45)))

        self.rect = pygame.Rect(x, y, pixel_w, pixel_h)
        self.color = (120, 220, 255)
        self.velocidad = 4

        # Stats default
        self.fuerza = 12
        self.destreza = 14
        self.sabiduria = 10
        self.constitucion = 12
        self.inteligencia = 10
        self.carisma = 8

        # Level / XP
        self.nivel = 1
        self.exp = 0
        self.experience = 0

        self.lives = lives

        # HP: usar bonus_constitucion para dar más peso
        self.max_hp = 12 + bonus_constitucion(self.constitucion)
        self.hp = self.max_hp

        # Modificadores calculados mediante stat_modifier (escala configurable)
        self.fuerza_mod = stat_modifier(self.fuerza)
        self.destreza_mod = stat_modifier(self.destreza)
        self.bonificador = self.destreza_mod

        self.camara_offset = camara_offset
        self.tipo = tipo
        self.last_attack_time = 1000

    def handle_input(self, world=None):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.velocidad
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.velocidad
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.velocidad
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.velocidad

        if world is not None and (dx != 0 or dy != 0):
            old_x = self.rect.x
            new_x = old_x + dx
            if hasattr(world, "is_area_solid"):
                if not world.is_area_solid(new_x, self.rect.y, self.rect.width, self.rect.height):
                    self.rect.x = new_x
            else:
                self.rect.x = new_x
                if world.is_pixel_solid(self.rect.centerx, self.rect.centery):
                    self.rect.x = old_x

            old_y = self.rect.y
            new_y = old_y + dy
            if hasattr(world, "is_area_solid"):
                if not world.is_area_solid(self.rect.x, new_y, self.rect.width, self.rect.height):
                    self.rect.y = new_y
            else:
                self.rect.y = new_y
                if world.is_pixel_solid(self.rect.centerx, self.rect.centery):
                    self.rect.y = old_y
        else:
            self.rect.x += dx
            self.rect.y += dy

    def draw(self, screen, camera_offset):
        draw_x = int(self.rect.x - camera_offset[0])
        draw_y = int(self.rect.y - camera_offset[1])
        pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.rect.width, self.rect.height))

    @classmethod
    def from_character(cls, character_dict, x, y):
        c = character_dict or {}
        scores = c.get("scores", {})
        def get_score(stat, default):
            v = scores.get(stat)
            if isinstance(v, dict):
                return int(v.get("value", default))
            try:
                return int(v)
            except Exception:
                return default
        obj = cls(x, y)
        obj.fuerza = get_score("Fuerza", 12)
        obj.destreza = get_score("Destreza", 14)
        obj.constitucion = get_score("Constitución", 12)
        obj.inteligencia = get_score("Inteligencia", 10)
        obj.sabiduria = get_score("Sabiduría", 10)
        obj.carisma = get_score("Carisma", 8)

        # Recompute derived stats using centralized logic
        obj.max_hp = 12 + bonus_constitucion(obj.constitucion)
        obj.hp = obj.max_hp
        obj.fuerza_mod = stat_modifier(obj.fuerza)
        obj.destreza_mod = stat_modifier(obj.destreza)
        obj.bonificador = obj.destreza_mod

        obj.name = c.get("name", "Player")
        obj.age = c.get("age", 18)
        obj.lives = getattr(obj, "lives", 3)
        return obj

    def actualizar_stats(self):
        """Recalcula max_hp y modificadores (llamar después de cambiar stats)."""
        self.max_hp = 12 + bonus_constitucion(self.constitucion)
        self.hp = min(self.hp, self.max_hp)
        self.fuerza_mod = stat_modifier(self.fuerza)
        self.destreza_mod = stat_modifier(self.destreza)
        self.bonificador = self.destreza_mod

    def respawn_at(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.hp = max(1, int(self.max_hp * 0.5))