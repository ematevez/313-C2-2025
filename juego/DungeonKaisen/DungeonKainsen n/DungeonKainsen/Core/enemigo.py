# core/enemigo.py
import pygame
import math
import random

class Enemy:
    def __init__(self, x, y, size=48, color=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color if color else (
            random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)
        )
        self.ACD = max(1, int(size * 0.2))
        self.hp = max(1, int(size * 0.6))
        self.max_hp = self.hp
        self.velocidad = 2
        self.last_attack_time = 0
        self.attack_cooldown = 1000
        self.damage = max(1, int(size * 0.02))
        # experience/xp: expose as .xp (int) and keep .experience for compatibility
        self.experience = size * 0.5
        self.xp = int(max(1, round(self.experience)))
        self.vision_range = size * 8

    def seguir_jugador(self, player, world=None):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > self.vision_range:
            return
        if dist > 0:
            nx = dx / dist
            ny = dy / dist
            move_x = nx * self.velocidad
            move_y = ny * self.velocidad

            if world:
                old_x = self.rect.x
                self.rect.x += int(round(move_x))
                if world.is_pixel_solid(self.rect.centerx, self.rect.centery):
                    self.rect.x = old_x

                old_y = self.rect.y
                self.rect.y += int(round(move_y))
                if world.is_pixel_solid(self.rect.centerx, self.rect.centery):
                    self.rect.y = old_y
            else:
                self.rect.x += int(round(move_x))
                self.rect.y += int(round(move_y))

    def ataque(self, player):
        now = pygame.time.get_ticks()
        if not self.rect.colliderect(player.rect):
            return 0
        if now - self.last_attack_time < self.attack_cooldown:
            return 0
        self.last_attack_time = now
        dmg = int(self.damage)
        player.hp -= dmg
        if player.hp < 0:
            player.hp = 0
        return dmg

    def draw(self, screen, camera_offset):
        draw_x = int(self.rect.x - camera_offset[0])
        draw_y = int(self.rect.y - camera_offset[1])
        pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.rect.width, self.rect.height))
        pygame.draw.rect(screen, (255,255,255), (draw_x, draw_y, self.rect.width, self.rect.height), 1)