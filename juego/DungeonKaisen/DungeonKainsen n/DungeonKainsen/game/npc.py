# game/npc.py
# Clase sencilla de NPC con posición, rect, nombre y dialog_id.
# Comportamiento: idle bobbing (visual) y método interact() para iniciar diálogo.

import pygame
import math
import time

class NPC:
    def __init__(self, name, x, y, dialog_id, color=(200,180,80), size=40, interact_radius=96):
        """
        name: str - nombre mostrado en diálogo
        x,y: int - posición en pixels (top-left)
        dialog_id: key para DialogueManager
        color: rect color for placeholder sprite
        size: visual square size in pixels
        interact_radius: distance in pixels to trigger interaction
        """
        self.name = name
        self.rect = pygame.Rect(int(x), int(y), int(size), int(size))
        self.dialog_id = dialog_id
        self.color = color
        self.size = size
        self.interact_radius = interact_radius
        self._bob_start = time.time()
        self.visible = True

    def update(self, dt=None):
        # simple bobbing effect for idle animation (for visual feedback)
        t = (time.time() - self._bob_start)
        bob = math.sin(t * 2.0) * 2.0  # +/- 2 pixels
        self._bob_offset = bob

    def draw(self, surface, camera_offset):
        if not self.visible:
            return
        ox = int(camera_offset[0])
        oy = int(camera_offset[1])
        x = int(self.rect.x - ox)
        y = int(self.rect.y - oy + getattr(self, "_bob_offset", 0))
        pygame.draw.rect(surface, self.color, (x, y, self.rect.width, self.rect.height))
        # outline
        pygame.draw.rect(surface, (255,255,255), (x, y, self.rect.width, self.rect.height), 1)

    def world_center(self):
        return (self.rect.centerx, self.rect.centery)

    def distance_to(self, px, py):
        dx = (self.rect.centerx - px)
        dy = (self.rect.centery - py)
        return (dx*dx + dy*dy) ** 0.5

    def can_interact(self, px, py):
        return self.distance_to(px, py) <= self.interact_radius

    def interact(self):
        """
        Returns the dialog_id to start the dialogue.
        """
        return self.dialog_id