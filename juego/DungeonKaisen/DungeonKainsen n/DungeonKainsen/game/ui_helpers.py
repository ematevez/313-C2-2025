# game/ui_helpers.py
# Helpers de UI reutilizables: barra de vida, barra de Energía Maldita (EM) y una UI de stats mínima.
# Coloca este archivo en tu proyecto y utiliza sus funciones/clase desde el bucle principal.
#
# Uso:
#   from game.ui_helpers import draw_health_bar, draw_em_bar, StatsUI
#   draw_health_bar(screen, 10, 10, player.hp, player.max_hp)
#   draw_em_bar(screen, 12, 30, em_obj, font=font_small)
#   stats_ui = StatsUI(player, font=font_small, puntos=2)
#   stats_ui.draw(screen, x=60, y=80)
#
# Nota: todo está documentado en español y protegido contra fallos si la API del objeto em o player difiere.

import pygame
from typing import Optional

# ---------------- Barra de vida ----------------
def draw_health_bar(screen: pygame.Surface, x: int, y: int, current: float, max_hp: float,
                    width: int = 120, height: int = 14,
                    color_bg=(80,20,20), color_fg=(220,40,40), border_color=(255,255,255)):
    """
    Dibuja una barra de vida simple.
    - screen: Surface de pygame donde dibujar.
    - x,y: esquina superior izquierda.
    - current,max_hp: valores numéricos (se manejan floats/ints).
    - width,height: tamaño de la barra.
    """
    try:
        if max_hp is None or max_hp <= 0:
            ratio = 0.0
        else:
            ratio = max(0.0, min(float(current) / float(max_hp), 1.0))
        # fondo
        pygame.draw.rect(screen, color_bg, (x, y, width, height))
        # parte llena
        pygame.draw.rect(screen, color_fg, (x, y, int(width * ratio), height))
        # borde
        pygame.draw.rect(screen, border_color, (x, y, width, height), 2)
    except Exception:
        # no queremos que un fallo de draw rompa el juego
        pass

# ---------------- Barra de Energía Maldita (EM) ----------------
def draw_em_bar(screen: pygame.Surface, x: int, y: int, em_obj, width: int = 160, height: int = 10,
                font: Optional[pygame.font.Font] = None,
                color_bg=(40,40,60), color_fg=(80,220,255), border_color=(255,255,255),
                txt_color=(200,220,255)):
    """
    Dibuja la barra de Energia Maldita y muestra Puño cargado.
    em_obj debe exponer (o al menos tener):
      - em_obj.max_total() -> int  (o em_obj.em_total_max)
      - em_obj.available_total() -> int (o em_obj.em_total)
      - em_obj.em_puño -> int
      - em_obj._per_punch_limit (o similar) opcional
    El dibujo es tolerante a ausencia de cualquier atributo.
    """
    if em_obj is None:
        return
    try:
        # intentar usar API preferida, con fallback a atributos
        try:
            maxv = int(em_obj.max_total())
        except Exception:
            maxv = int(getattr(em_obj, "em_total_max", 0) or 0)
        try:
            curv = int(em_obj.available_total())
        except Exception:
            curv = int(getattr(em_obj, "em_total", 0) or 0)
        maxv = max(1, maxv)
        pct = float(curv) / float(maxv) if maxv > 0 else 0.0

        pygame.draw.rect(screen, color_bg, (x, y, width, height))
        pygame.draw.rect(screen, color_fg, (x, y, int(width * pct), height))
        pygame.draw.rect(screen, border_color, (x, y, width, height), 1)

        # texto de puño cargado
        per_limit = getattr(em_obj, "_per_punch_limit", getattr(em_obj, "per_punch_limit", 0))
        puño = getattr(em_obj, "em_puño", 0)

        if font is None:
            try:
                font = pygame.font.SysFont("arial", 14)
            except Exception:
                font = None

        if font is not None:
            txt = font.render(f"Puño: {puño}/{per_limit}", True, txt_color)
            screen.blit(txt, (x + width + 8, y - 2))
    except Exception:
        # silenciosamente ignorar problemas de dibujo
        pass

# ---------------- Stats UI mínima ----------------
class StatsUI:
    """
    UI minimal para ver/editar stats básicos del jugador.
    - Muestra: Fuerza, Destreza, Constitución, Inteligencia, Sabiduría, Carisma.
    - Evita problemas por acentos mapeando los labels a atributos internos.
    - Métodos principales:
        draw(screen, x, y)
        handle_key(key)  # para manejar navegación y edición via teclado
    - No gestiona persistencia: tras cambiar stats se sugiere llamar a player.actualizar_stats() si existe.
    """

    DISPLAY = ["Fuerza", "Destreza", "Constitución", "Inteligencia", "Sabiduría", "Carisma"]
    MAP = {
        "Fuerza": "fuerza",
        "Destreza": "destreza",
        "Constitución": "constitucion",
        "Inteligencia": "inteligencia",
        "Sabiduría": "sabiduria",
        "Carisma": "carisma",
    }

    def __init__(self, player, font: Optional[pygame.font.Font] = None, puntos: int = 0):
        self.player = player
        try:
            self.font = font or pygame.font.SysFont("arial", 20)
        except Exception:
            # fallback si no hay inicializado pygame.font (muy raro)
            self.font = None
        self.selected = 0
        self.puntos = int(puntos or 0)

    def draw(self, screen: pygame.Surface, x: int = 60, y: int = 80, width: int = 300, bg_color=(24,24,34), border_color=(200,200,200), title_color=(230,230,230)):
        """
        Dibuja el panel de stats en (x,y).
        """
        try:
            h_est = 28
            h = 40 + len(self.DISPLAY) * h_est + 36
            # fondo y borde
            panel = pygame.Rect(x-8, y-8, width+16, h+16)
            s = pygame.Surface((panel.width, panel.height))
            s.set_alpha(230)
            s.fill(bg_color)
            screen.blit(s, (panel.x, panel.y))
            pygame.draw.rect(screen, border_color, panel, 2)

            # título
            if self.font:
                title = self.font.render("Estadísticas", True, title_color)
                screen.blit(title, (x, y))
                yy = y + 34
            else:
                yy = y + 6

            # líneas de info (nivel, HP, EXP) si el player tiene esos atributos
            info_lines = []
            try:
                lvl = getattr(self.player, "nivel", None)
                hp = getattr(self.player, "hp", None)
                max_hp = getattr(self.player, "max_hp", None)
                exp = getattr(self.player, "exp", None)
                if lvl is not None:
                    info_lines.append(f"Nivel: {lvl}")
                if hp is not None and max_hp is not None:
                    info_lines.append(f"HP: {int(hp)}/{int(max_hp)}")
                if exp is not None:
                    info_lines.append(f"EXP: {int(exp)}")
            except Exception:
                pass

            for line in info_lines:
                if self.font:
                    surf = self.font.render(line, True, (200,200,200))
                    screen.blit(surf, (x + 6, yy))
                yy += 20
            if info_lines:
                yy += 6

            # stats editables
            for i, label in enumerate(self.DISPLAY):
                attr = self.MAP.get(label, label.lower())
                val = getattr(self.player, attr, 0)
                color = (255,255,120) if i == self.selected else (220,220,220)
                if self.font:
                    stat_txt = self.font.render(f"{label}: {val}", True, color)
                    screen.blit(stat_txt, (x + 6, yy))
                yy += h_est

            # puntos restantes
            if self.font:
                pts_txt = self.font.render(f"Puntos disponibles: {self.puntos}", True, (180,200,255))
                screen.blit(pts_txt, (x + 6, yy + 4))
        except Exception:
            pass

    def handle_key(self, key):
        """
        Manejo básico de teclado:
         - UP/DOWN (o W/S) para navegar
         - RIGHT/D (o ENTER) para subir la stat si hay puntos
         - LEFT/A para decrementar (si >1)
        """
        try:
            if key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.DISPLAY)
            elif key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.DISPLAY)
            elif key in (pygame.K_RIGHT, pygame.K_d, pygame.K_RETURN, pygame.K_SPACE):
                if self.puntos > 0:
                    label = self.DISPLAY[self.selected]
                    attr = self.MAP.get(label, label.lower())
                    cur = getattr(self.player, attr, 0) or 0
                    setattr(self.player, attr, cur + 1)
                    # intentar recalcular stats derivados si existe el método
                    try:
                        self.player.actualizar_stats()
                    except Exception:
                        pass
                    self.puntos -= 1
            elif key in (pygame.K_LEFT, pygame.K_a):
                label = self.DISPLAY[self.selected]
                attr = self.MAP.get(label, label.lower())
                cur = getattr(self.player, attr, 0) or 0
                if cur > 1:
                    setattr(self.player, attr, cur - 1)
                    try:
                        self.player.actualizar_stats()
                    except Exception:
                        pass
        except Exception:
            pass

    def handle_event(self, event):
        """
        Atajo: pasar eventos pygame.KEYDOWN directamente.
        """
        if event.type == pygame.KEYDOWN:
            self.handle_key(event.key)

# ---------------- Ejemplo de integración (documentación) ----------------
USAGE_TEXT = """
Integración rápida (ejemplo en el loop principal):
  # imports
  from game.ui_helpers import draw_health_bar, draw_em_bar, StatsUI

  # al crear/poner player y em en tu Game:
  self.stats_ui = StatsUI(self.player, font=self.font_small, puntos=2)

  # dentro del event loop:
  if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
      self.stats_open = not self.stats_open
      if self.stats_open:
          # mantener la instancia si quieres preservar puntos seleccionados
          if not getattr(self, "stats_ui", None):
              self.stats_ui = StatsUI(self.player, font=self.font_small, puntos=2)
      else:
          # opcional: descartar la UI al cerrarla
          pass

  # si stats_open y quieres manejar teclas:
  if self.stats_open and event.type == pygame.KEYDOWN:
      try:
          self.stats_ui.handle_key(event.key)
      except Exception:
          pass

  # en la sección de dibujo por frame (HUD):
  draw_health_bar(screen, 10, 10, self.player.hp, self.player.max_hp, width=160, height=16)
  draw_em_bar(screen, 12, 30, self.em, width=160, height=10, font=self.font_small)
  if self.stats_open and self.stats_ui:
      self.stats_ui.draw(screen, x=60, y=80)
"""

# Exportar el texto de uso para debugging si alguien lo importa
__usage__ = USAGE_TEXT