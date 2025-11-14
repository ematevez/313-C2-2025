# core/camara.py
# Compat shim: ofrece una Camera simple y la función actualizar_camara antigua.
# Esto mantiene compatibilidad con código que importaba camara.actualizar_camara.
import pygame

class Camera:
    def __init__(self, screen_w=1000, screen_h=1000, tile_size=32):
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.tile_size = tile_size
        self.smooth = 0.12
        self.center_immediately = True

    def center_on(self, px, py):
        desired_x = px - (self.screen_w // 2)
        desired_y = py - (self.screen_h // 2)
        if desired_x < 0:
            desired_x = 0.0
        if desired_y < 0:
            desired_y = 0.0
        if self.center_immediately:
            self.offset_x = float(desired_x)
            self.offset_y = float(desired_y)
        else:
            self.offset_x += (desired_x - self.offset_x) * self.smooth
            self.offset_y += (desired_y - self.offset_y) * self.smooth
            if self.offset_x < 0:
                self.offset_x = 0.0
            if self.offset_y < 0:
                self.offset_y = 0.0

# Backwards-compatible global camera state + helper function
posicion_camara = [0, 0]
limite_de_pantalla = 150

def actualizar_camara(jugador_rect):
    """Compat wrapper: actualiza posicion_camara y devuelve (x,y)."""
    px = jugador_rect.centerx
    py = jugador_rect.centery
    desired_x = px - (limite_de_pantalla)
    desired_y = py - (limite_de_pantalla)
    desired_x = max(0, desired_x)
    desired_y = max(0, desired_y)
    posicion_camara[0] = desired_x
    posicion_camara[1] = desired_y
    return posicion_camara[0], posicion_camara[1]