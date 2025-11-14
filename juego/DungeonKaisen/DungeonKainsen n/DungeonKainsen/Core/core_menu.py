import pygame
import os

class MainMenu:
    def __init__(self, ancho, altura, titulo="Dungeon Kaisen"):
        self.ancho = ancho
        self.altura = altura
        self.titulo = titulo
        self.options = ["Nuevo Juego", "Tutorial", "Cargar", "Crear personaje", "Cambiar resolución", "Salir"]
        self.selected = 0
        self.font_title = pygame.font.SysFont("arial", 44, bold=True)
        self.font_option = pygame.font.SysFont("arial", 32)

        # Submenú de resolución
        self.in_resolution_menu = False
        self.resolutions = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1600, 900),
            (1920, 1080)
        ]
        self.res_selected = 0

    def handle_event(self, event):
        """Procesa entrada del teclado"""
        if event.type != pygame.KEYDOWN:
            return None

        # --- Submenú de resolución ---
        if self.in_resolution_menu:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.res_selected = (self.res_selected - 1) % len(self.resolutions)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.res_selected = (self.res_selected + 1) % len(self.resolutions)
            elif event.key == pygame.K_RETURN:
                nueva = self.resolutions[self.res_selected]
                self.in_resolution_menu = False
                return ("change_resolution", nueva)
            elif event.key == pygame.K_ESCAPE:
                self.in_resolution_menu = False
            return None

        # --- Menú principal ---
        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % len(self.options)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % len(self.options)
        elif event.key == pygame.K_RETURN:
            if self.options[self.selected] == "Cambiar resolución":
                self.in_resolution_menu = True
                return None
            else:
                return self.selected
        return None

    def draw(self, screen):
        screen.fill((20, 20, 40))

        # --- Submenú de resolución ---
        if self.in_resolution_menu:
            title_surf = self.font_title.render("Cambiar resolución", True, (230, 200, 50))
            title_rect = title_surf.get_rect(center=(self.ancho // 2, 120))
            screen.blit(title_surf, title_rect)

            for i, res in enumerate(self.resolutions):
                color = (255, 255, 180) if i == self.res_selected else (220, 220, 220)
                text = f"{res[0]} x {res[1]}"
                opt_surf = self.font_option.render(text, True, color)
                opt_rect = opt_surf.get_rect(center=(self.ancho // 2, 220 + i * 60))
                screen.blit(opt_surf, opt_rect)
            return

        # --- Menú principal ---
        title_surf = self.font_title.render(self.titulo, True, (230, 200, 50))
        title_rect = title_surf.get_rect(center=(self.ancho // 2, 120))
        screen.blit(title_surf, title_rect)

        for i, option in enumerate(self.options):
            color = (255, 255, 180) if i == self.selected else (220, 220, 220)
            opt_surf = self.font_option.render(option, True, color)
            opt_rect = opt_surf.get_rect(center=(self.ancho // 2, 220 + i * 60))
            screen.blit(opt_surf, opt_rect)
