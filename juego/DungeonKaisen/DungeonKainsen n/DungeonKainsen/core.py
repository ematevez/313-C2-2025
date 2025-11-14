# game/core.py
# Núcleo del juego — Game con XP system, HUD (HP/EM/Último golpe), chat con IA (T) y retroceso (knockback).
# Esta versión: la lógica de progresión por nivel se delega totalmente a game/lvl_up_player_logic.py
# y se añadió separación física entre jugador y enemigos para evitar atravesamientos.

import pygame
import sys
import time
import os
import math
import random
import json
import threading

from Core.dado20 import DiceUI
from Core.jugador import Player
from Core.enemigo import Enemy
from Core.combate import calcular_ataque
from Core.world import World
from Core.core_menu import MainMenu
from Core.fairy_ai import FairyAI
from Core.blackflash import FlashEffect
from Core.Pausa import pausa
from Core.texto import DamageText
from Core.energia_maldita import EnergiaMaldita
from Core.stats import StatsUI
from Core.DeathScreen import DeathScreen
from Core.level_up_menu import LevelUpMenu
from Core.character_creator import CharacterCreator
from Core.tutorial_world import TutorialWorld
from Core.audio import AudioManager
from settings import *

from game.camera import Camera
from game.ui import draw_health_bar, ArmEffect, draw_xp_bar
from game.spawn import spawn_random_enemies
from game.save_load import save_game_data, load_game_data
from game.npc import NPC
from game.dialogue import DialogueManager
from game.npc_ui import DialogueUI

# Importar la lógica de niveles centralizada (no duplicar tablas en core)
from game.lvl_up_player_logic import (
    get_proficiency_bonus,
    get_level_point_bonus,
    apply_level_progression_to_player,
)

# Fallbacks para helpers opcionales (draw_em_bar, HUD_StatsUI)
try:
    from game.ui_helpers import draw_em_bar, StatsUI as HUD_StatsUI
except Exception:
    def draw_em_bar(screen, x, y, em_obj, width=160, height=10, font=None, *a, **kw):
        try:
            if em_obj is None:
                return
            try:
                maxv = int(em_obj.max_total())
            except Exception:
                maxv = int(getattr(em_obj, "em_total_max", 1) or 1)
            try:
                curv = int(em_obj.available_total())
            except Exception:
                curv = int(getattr(em_obj, "em_total", 0) or 0)
            maxv = max(1, maxv)
            pct = float(curv) / float(maxv) if maxv > 0 else 0.0
            pygame.draw.rect(screen, (40,40,60), (x, y, width, height))
            pygame.draw.rect(screen, (80,220,255), (x, y, int(width * pct), height))
            pygame.draw.rect(screen, (255,255,255), (x, y, width, height), 1)
            per_limit = getattr(em_obj, "_per_punch_limit", getattr(em_obj, "per_punch_limit", 0))
            puño = getattr(em_obj, "em_puño", 0)
            if font is None:
                try:
                    font = pygame.font.SysFont("arial", 14)
                except Exception:
                    font = None
            if font is not None:
                txt = font.render(f"Puño: {puño}/{per_limit}", True, (200,220,255))
                screen.blit(txt, (x + width + 8, y - 2))
        except Exception:
            pass

    class HUD_StatsUI:
        DISPLAY = ["Fuerza", "Destreza", "Constitución", "Inteligencia", "Sabiduría", "Carisma"]
        MAP = {
            "Fuerza": "fuerza",
            "Destreza": "destreza",
            "Constitución": "constitucion",
            "Inteligencia": "inteligencia",
            "Sabiduría": "sabiduria",
            "Carisma": "carisma",
        }
        def __init__(self, player, font=None, puntos=0):
            self.player = player
            try:
                self.font = font or pygame.font.SysFont("arial", 20)
            except Exception:
                self.font = None
            self.selected = 0
            self.puntos = int(puntos or 0)
        def draw(self, screen, x=60, y=80):
            try:
                w = 300
                h_est = 28
                h = 40 + len(self.DISPLAY) * h_est + 36
                panel = pygame.Rect(x-8, y-8, w+16, h+16)
                surf = pygame.Surface((panel.width, panel.height))
                surf.set_alpha(230)
                surf.fill((24,24,34))
                screen.blit(surf, (panel.x, panel.y))
                pygame.draw.rect(screen, (200,200,200), panel, 2)
                if self.font:
                    title = self.font.render("Estadísticas", True, (230,230,230))
                    screen.blit(title, (x, y))
                    yy = y + 34
                else:
                    yy = y + 6
                for i, label in enumerate(self.DISPLAY):
                    attr = self.MAP.get(label, label.lower())
                    val = getattr(self.player, attr, 0)
                    color = (255,255,120) if i == self.selected else (220,220,220)
                    if self.font:
                        stat_txt = self.font.render(f"{label}: {val}", True, color)
                        screen.blit(stat_txt, (x + 6, yy))
                    yy += h_est
                if self.font:
                    pts_txt = self.font.render(f"Puntos disponibles: {self.puntos}", True, (180,200,255))
                    screen.blit(pts_txt, (x + 6, yy + 4))
            except Exception:
                pass
        def handle_key(self, key):
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
                        try:
                            self.player.actualizar_stats()
                        except Exception:
                            pass
                        self.puntos -= 1
                # left / a intentionally ignored to avoid decrementing stats during gameplay
            except Exception:
                pass


DEFAULT_SEED = 12121

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("ChronoCraft Style D&D")
        self.screen = pygame.display.set_mode((ANCHO, ALTURA))
        self.clock = pygame.time.Clock()

        # audio
        self.audio = AudioManager()
        try:
            self.audio.load_sfx("hit", "hit.wav")
            self.audio.load_sfx("crit", "crit.wav")
            self.audio.load_sfx("xp", "xp.wav")
        except Exception:
            pass

        # UI/menu
        self.menu = MainMenu(ANCHO, ALTURA)
        if "Crear personaje" not in self.menu.options:
            if "Salir" in self.menu.options:
                idx = self.menu.options.index("Salir")
                self.menu.options.insert(idx, "Crear personaje")
            else:
                self.menu.options.append("Crear personaje")
        if "Tutorial" not in self.menu.options:
            self.menu.options.insert(1, "Tutorial")

        self.running = True
        self.in_menu = True
        self.paused = False

        self.character = CharacterCreator.load_if_exists()
        self.require_character = True if not self.character else False
        self.player = None

        ts = globals().get("TILE_SIZE", None)
        if ts is None:
            ppm = globals().get("PIXELS_PER_METER", 12)
            mpt = globals().get("METERS_PER_TILE", 4)
            ts = int(ppm * mpt)
        self.tile_size = ts

        # world
        major_spacing_m = 400
        minor_spacing_m = 80
        major_road_width_m = 12
        minor_road_width_m = 6
        try:
            meters_per_tile = METERS_PER_TILE
        except Exception:
            meters_per_tile = 4
        major_road_width_tiles = max(1, int(round(major_road_width_m / meters_per_tile)))
        minor_road_width_tiles = max(1, int(round(minor_road_width_m / meters_per_tile)))
        try:
            self.world = World(
                mapa=None,
                tile_size=self.tile_size,
                seed=DEFAULT_SEED,
                major_spacing_meters=major_spacing_m,
                minor_spacing_meters=minor_spacing_m,
                major_road_width=major_road_width_tiles,
                minor_road_width=minor_road_width_tiles,
                sidewalk_width=1,
                bike_lane_width=1
            )
        except Exception:
            self.world = World(mapa=None, tile_size=self.tile_size, seed=DEFAULT_SEED)

        # camera + zoom
        self.camera = Camera(self.tile_size, screen_size=(ANCHO, ALTURA))
        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 2.5
        self.zoom_step = 0.1
        self.camera.center_immediately = True

        self.pausa_menu = pausa(self)
        self.level_up_menu = LevelUpMenu(None)

        self.enemies = []
        self.max_enemies = 10
        self.dice_ui = DiceUI(ANCHO - 300, 20)
        self.flash = FlashEffect()

        self.damage_texts = pygame.sprite.Group()
        self.arms = []

        self.enemy_shakes = {}
        self.enemy_knockbacks = {}

        # legacy/compat fields
        self.fairy = None
        self.fairy_request_thread = None
        self.fairy_waiting = False
        self.fairy_input_active = False
        self.fairy_input_text = ""

        # user-facing chat state
        self.fairy_chat_active = False
        self.fairy_chat_input = ""
        self.fairy_chat_history = []
        self.fairy_chat_waiting = False
        self.fairy_request_thread = None

        self.stats_open = False
        self.stats_ui = None

        self.font_input = pygame.font.SysFont("arial", 22)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.font_big = pygame.font.SysFont("arial", 28)

        self.death_screen = DeathScreen(ANCHO, ALTURA)
        self.is_dead = False
        self.no_lives_left = False
        self.pending_death_pos = None
        self.last_checkpoint = (200, 300)

        self.char_creator = None
        self.tutorial_active = False
        self.tutorial_enemies = []
        self.spawn_timer = 0

        self.em = None

        self.autosave_interval = 30.0
        self._last_autosave = time.time()

        self.default_xp_formula = lambda lvl: 50 * max(1, lvl)

        self.npcs = []
        self.dialogue = DialogueManager()
        self.dialogue_ui = DialogueUI(ANCHO, ALTURA, font=self.font_input)
        self.dialogue_active = False

        try:
            self.npcs.append(NPC("Vendedor", 600, 420, dialog_id="vendor_intro", color=(180,140,80), size=44))
            self.npcs.append(NPC("Guardia", 760, 420, dialog_id="guard_greet", color=(120,160,220), size=44))
        except Exception:
            try:
                self.npcs.append(NPC("Vendedor", 600, 420, "vendor_intro", color=(180,140,80), size=44))
                self.npcs.append(NPC("Guardia", 760, 420, "guard_greet", color=(120,160,220), size=44))
            except Exception:
                pass

        self.dialogue.register("vendor_intro", [
            {"speaker":"Vendedor","text":"¡Hola viajero! ¿Buscas provisiones?"},
            {"speaker":"Vendedor","text":"Tengo manzanas frescas y mapas antiguos."},
            {"speaker":"Vendedor","text":"Vuelve si quieres comerciar."}
        ])
        self.dialogue.register("guard_greet", [
            {"speaker":"Guardia","text":"No pases sin permiso."},
            {"speaker":"Guardia","text":"Si necesitas hablar con el alcalde, busca la casa azul."}
        ])

        # HUD extras
        self.last_hit = None
        self.last_hit_time = 0
        self.last_hit_duration = 1800  # ms

        # init fairy (non-fatal)
        self._ensure_fairy_initialized()

    # helpers
    def _set_zoom(self, new_zoom):
        self.zoom = max(self.min_zoom, min(self.max_zoom, new_zoom))

    def _change_zoom(self, delta):
        self._set_zoom(self.zoom + delta)

    def _shrink_player(self, scale=1.0):
        if not getattr(self, "player", None):
            return
        try:
            cx, cy = self.player.rect.center
            new_w = max(4, int(round(self.player.rect.width * scale)))
            new_h = max(4, int(round(self.player.rect.height * scale)))
            self.player.rect.width = new_w
            self.player.rect.height = new_h
            self.player.rect.center = (cx, cy)
        except Exception:
            pass

    # FAIRY IA helpers
    def _ensure_fairy_initialized(self):
        try:
            api_key = os.environ.get("FAIRY_API_KEY")
            if not api_key:
                try:
                    path = os.path.join(os.getcwd(), "api_key.txt")
                    if os.path.exists(path):
                        with open(path, "r", encoding="utf-8") as f:
                            api_key = f.read().strip()
                except Exception:
                    api_key = None
            if api_key:
                try:
                    self.fairy = FairyAI(api_key=api_key)
                except Exception:
                    self.fairy = None
            else:
                self.fairy = None
        except Exception:
            try:
                self.fairy = None
            except Exception:
                pass

    def _ask_fairy_thread(self, prompt_text):
        try:
            if not self.fairy or not getattr(self.fairy, "api_key", None):
                response = "Shikigami: No hay clave API configurada. Coloca FAIRY_API_KEY o api_key.txt."
            else:
                try:
                    response = self.fairy.preguntar(prompt_text)
                    if response is None:
                        response = "Shikigami: (respuesta vacía)"
                except Exception as e:
                    response = f"Error al contactar IA: {getattr(e, 'args', e)}"
        except Exception as e:
            response = f"Error inesperado en hilo IA: {e}"
        try:
            self.fairy_chat_history.append(("ai", response))
        except Exception:
            try:
                self.fairy_chat_history = [("ai", response)]
            except Exception:
                pass
        finally:
            try:
                self.fairy_chat_waiting = False
            except Exception:
                pass

    def start_fairy_request(self, question):
        if getattr(self, "fairy_chat_waiting", False):
            return
        if not getattr(self, "fairy", None):
            try:
                self._ensure_fairy_initialized()
            except Exception:
                pass
        if not getattr(self, "fairy", None) or not getattr(self.fairy, "api_key", None):
            try:
                self.fairy_chat_history.append(("ai", "Shikigami: No hay clave API configurada. Añadila a FAIRY_API_KEY o a api_key.txt"))
            except Exception:
                pass
            self.fairy_chat_waiting = False
            return
        try:
            self.fairy_chat_waiting = True
            t = threading.Thread(target=self._ask_fairy_thread, args=(question,), daemon=True)
            t.start()
            self.fairy_request_thread = t
        except Exception:
            try:
                resp = self.fairy.preguntar(question)
                self.fairy_chat_history.append(("ai", resp if resp is not None else "Shikigami: (sin respuesta)"))
            except Exception as e:
                try:
                    self.fairy_chat_history.append(("ai", f"Error al contactar IA: {e}"))
                except Exception:
                    pass
            finally:
                try:
                    self.fairy_chat_waiting = False
                except Exception:
                    pass

    # Save/Load/Quit
    def save_game(self):
        return save_game_data(self)

    def load_game(self):
        return load_game_data(self)

    def quit_and_cleanup(self, save=True):
        try:
            if save:
                self.save_game()
        except Exception:
            pass
        try:
            if getattr(self, "world", None):
                self.world.stop()
        except Exception:
            pass
        try:
            self.audio.stop_music()
        except Exception:
            pass
        pygame.quit()
        sys.exit()

    # XP / leveling (delegated rules)
    def xp_to_next(self):
        lvl = getattr(self.player, "nivel", 1) if self.player else 1
        return self.default_xp_formula(lvl)

    def award_xp(self, amount, show_text=True, src_pos=None):
        """
        Awards XP and handles level-ups. Delegates level-specific rules to game.lvl_up_player_logic:
         - get_level_point_bonus(level) -> points to award (only at milestones)
         - apply_level_progression_to_player(player, level) -> set derived attrs (proficiency, cursed energy, movement, martial arts die)
        """
        if not self.player:
            return
        try:
            cur = int(getattr(self.player, "exp", 0))
            cur += int(amount)
            self.player.exp = cur
            if show_text:
                if src_pos:
                    tx = src_pos[0] - int(self.camera.offset_x)
                    ty = src_pos[1] - int(self.camera.offset_y) - 10
                else:
                    tx = self.player.rect.centerx - int(self.camera.offset_x)
                    ty = self.player.rect.top - int(self.camera.offset_y) - 30
                try:
                    self.damage_texts.add(DamageText(tx, ty, f"+{amount} XP", (120, 220, 180)))
                except Exception:
                    pass
            try:
                if getattr(self, "audio", None):
                    self.audio.play_sfx("xp", volume=0.6)
            except Exception:
                pass
            leveled = False
            while self.player.exp >= self.xp_to_next():
                needed = self.xp_to_next()
                self.player.exp -= needed
                self.player.nivel = int(getattr(self.player, "nivel", 1)) + 1

                # modest HP increase on level
                try:
                    self.player.max_hp = int(getattr(self.player, "max_hp", 10)) + 5
                    self.player.hp = min(self.player.max_hp, int(getattr(self.player, "hp", self.player.max_hp)) + 5)
                except Exception:
                    pass
                try:
                    self.player.actualizar_stats()
                except Exception:
                    pass

                # show level up message
                try:
                    cx = self.player.rect.centerx - int(self.camera.offset_x)
                    cy = self.player.rect.top - int(self.camera.offset_y) - 40
                    self.damage_texts.add(DamageText(cx, cy, "LEVEL UP!", (240, 200, 80)))
                except Exception:
                    pass

                # Use external module to decide points & derived attrs
                try:
                    lvl_now = int(getattr(self.player, "nivel", 0))

                    # 1) points (milestones only)
                    try:
                        point_bonus = get_level_point_bonus(lvl_now)
                        if point_bonus:
                            try:
                                cur_pts = int(getattr(self.player, "stat_points", 0))
                            except Exception:
                                cur_pts = 0
                            try:
                                self.player.stat_points = cur_pts + int(point_bonus)
                            except Exception:
                                try:
                                    setattr(self.player, "stat_points", cur_pts + int(point_bonus))
                                except Exception:
                                    pass
                            # Open the stats UI so the player can spend the points
                            try:
                                pts = int(getattr(self.player, "stat_points", 0))
                                try:
                                    self.stats_ui = HUD_StatsUI(self.player, font=self.font_small, puntos=pts)
                                except Exception:
                                    try:
                                        self.stats_ui = StatsUI(self.player)
                                        try:
                                            self.stats_ui.puntos = pts
                                        except Exception:
                                            pass
                                    except Exception:
                                        self.stats_ui = None
                                self.stats_open = True
                            except Exception:
                                pass
                    except Exception:
                        pass

                    # 2) Derived attributes (proficiency, cursed energy, movement, martial arts die)
                    try:
                        apply_level_progression_to_player(self.player, lvl_now)
                    except Exception:
                        pass

                except Exception:
                    pass

                try:
                    self.level_up_menu.player = self.player
                    self.level_up_menu.open()
                except Exception:
                    pass

                leveled = True
            return leveled
        except Exception:
            return False
    def char_creation_loop(self):
        if not getattr(self, "char_creator", None):
            return
        cc = self.char_creator
        self.in_menu = False
        try:
            while not getattr(cc, "done", False):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        try:
                            cc.done = True
                        except Exception:
                            pass
                        try:
                            self.save_game()
                        except Exception:
                            pass
                        try:
                            self.quit_and_cleanup()
                        except Exception:
                            sys.exit(0)
                    else:
                        try:
                            cc.handle_event(event)
                        except Exception:
                            pass
                try:
                    self.screen.fill((12, 12, 18))
                    try:
                        cc.draw()
                    except Exception:
                        pass
                    pygame.display.flip()
                    try:
                        self.clock.tick(FPS)
                    except Exception:
                        time.sleep(0.016)
                except Exception:
                    time.sleep(0.016)
        finally:
            try:
                if getattr(cc, "cancelled", False):
                    pass
                else:
                    try:
                        saved = False
                        try:
                            saved = cc.save()
                        except Exception:
                            saved = False
                        if saved:
                            try:
                                self.character = CharacterCreator.load_if_exists()
                            except Exception:
                                self.character = None
                        else:
                            try:
                                self.character = CharacterCreator.load_if_exists()
                            except Exception:
                                self.character = None
                        if self.character:
                            self.require_character = False
                    except Exception:
                        pass
            finally:
                try:
                    self.char_creator = None
                except Exception:
                    self.char_creator = None
                self.in_menu = True
    # menu/event handlers...
    def _handle_menu_event(self, event):
            """Procesa eventos del menú principal"""
            accion = self.menu.handle_event(event)

            # Si el jugador cambia la resolución
            if isinstance(accion, tuple) and accion[0] == "change_resolution":
                nueva_res = accion[1]
                globals()["ANCHO"], globals()["ALTURA"] = nueva_res

                # 🪄 Centramos la ventana antes de crearla
                os.environ['SDL_VIDEO_CENTERED'] = '1'

                # Recreamos la ventana con nueva resolución y modo redimensionable
                self.screen = pygame.display.set_mode(nueva_res, pygame.RESIZABLE)

                # Recreamos el menú con el nuevo tamaño
                self.menu = MainMenu(*nueva_res)
                return

            # Si selecciona una opción normal
            if isinstance(accion, int):
                opt = self.menu.options[accion]
                if opt == "Nuevo Juego":
                    if self.require_character:
                        self.char_creator = CharacterCreator(self.screen)
                        self.in_menu = False
                        self.char_creation_loop()
                    else:
                        ok = self.start_new_game()
                        if ok:
                            self.in_menu = False
                elif opt == "Tutorial":
                    self._start_tutorial()
                elif opt == "Cargar":
                    ok = self.load_game()
                    if ok:
                        self.in_menu = False
                elif opt == "Crear personaje":
                    self.char_creator = CharacterCreator(self.screen)
                    self.in_menu = False
                    self.char_creation_loop()
                elif opt == "Salir":
                    self.save_game()
                    self.quit_and_cleanup()

    def _handle_in_game_event(self, event):
        # toggle stats manual
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if not self.in_menu and not self.paused and not self.is_dead:
                if not self.stats_open:
                    puntos = int(getattr(self.player, "stat_points", 0))
                    try:
                        self.stats_ui = HUD_StatsUI(self.player, font=self.font_small, puntos=puntos)
                    except Exception:
                        try:
                            self.stats_ui = StatsUI(self.player)
                            try:
                                self.stats_ui.puntos = puntos
                            except Exception:
                                pass
                        except Exception:
                            self.stats_ui = None
                    self.stats_open = True
                else:
                    # persist remaining points then close
                    try:
                        if getattr(self, "stats_ui", None):
                            remaining = getattr(self.stats_ui, "puntos", getattr(self.stats_ui, "points", None))
                            if remaining is not None:
                                try:
                                    self.player.stat_points = int(remaining)
                                except Exception:
                                    try:
                                        setattr(self.player, "stat_points", int(remaining))
                                    except Exception:
                                        pass
                    except Exception:
                        pass
                    self.stats_open = False

        # other keys (zoom, dialog, pause...)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                self._change_zoom(self.zoom_step)
            elif event.key in (pygame.K_MINUS,):
                self._change_zoom(-self.zoom_step)
            elif event.key == pygame.K_z:
                self.camera.center_immediately = not self.camera.center_immediately
            elif event.key == pygame.K_x:
                self._set_zoom(1.0)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_PLUS:
            self._change_zoom(self.zoom_step)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_MINUS:
            self._change_zoom(-self.zoom_step)
        if event.type == pygame.MOUSEWHEEL:
            self._change_zoom(event.y * self.zoom_step)

        if self.dialogue.is_active():
            consumed = self.dialogue_ui.handle_event(event)
            if consumed:
                has_next = self.dialogue.advance()
                if self.dialogue.is_active():
                    line = self.dialogue.current()
                    if line:
                        self.dialogue_ui.show(line.get("speaker"), line.get("text"))
                else:
                    self.dialogue_ui.hide()
                    self.dialogue_active = False
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.paused = not self.paused

        # EM right click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if getattr(self, "em", None) is not None:
                try:
                    charged = self.em.cargar_punio()
                    tx = self.player.rect.centerx - int(self.camera.offset_x)
                    ty = self.player.rect.top - int(self.camera.offset_y) - 20
                    if charged:
                        self.damage_texts.add(DamageText(tx, ty, "+EM", (80,220,255)))
                    else:
                        self.damage_texts.add(DamageText(tx, ty, "No EM", (180,180,180)))
                except Exception:
                    pass
            return

        # attacks...
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            in_range = []
            for enemy in self.enemies:
                if enemy.hp > 0:
                    dx = enemy.rect.centerx - self.player.rect.centerx
                    dy = enemy.rect.centery - self.player.rect.centery
                    distancia = math.hypot(dx, dy)
                    if distancia <= RANGO_GOLPE:
                        in_range.append((distancia, enemy))
            in_range.sort(key=lambda x: x[0])
            targets = [e for _, e in in_range[:2]]
            now = pygame.time.get_ticks()
            for enemy in targets:
                resultado, exito, critico, mensaje = calcular_ataque(enemy.ACD, getattr(self.player, "fuerza_mod", 0))
                self.dice_ui.update(resultado, mensaje)
                try:
                    self.arms.append(ArmEffect(start_pos=self.player.rect.center, end_pos=enemy.rect.center, created_time=now))
                except Exception:
                    try:
                        self.arms.append((self.player.rect.center, enemy.rect.center, now))
                    except Exception:
                        pass
                if exito:
                    try:
                        em_part = 0
                        if getattr(self, "em", None) and getattr(self.em, "em_puño", 0) > 0:
                            weapon_damage = self.dice_ui.roll_damage(critical=False)
                            em_before = self.em.em_puño
                            em_part = self.em.golpear(critical=critico)
                            damage = weapon_damage + em_part + getattr(self.player, "fuerza_mod", 0)
                        else:
                            damage = self.dice_ui.roll_damage(critical=critico) + getattr(self.player, "fuerza_mod", 0)
                    except Exception:
                        try:
                            damage = self.dice_ui.roll_damage(critical=critico) + getattr(self.player, "fuerza_mod", 0)
                        except Exception:
                            damage = 0

                    enemy.hp -= damage

                    try:
                        self.last_hit = int(damage)
                        self.last_hit_time = pygame.time.get_ticks()
                    except Exception:
                        self.last_hit = None
                        self.last_hit_time = 0

                    try:
                        tx = enemy.rect.centerx - int(self.camera.offset_x)
                        ty = enemy.rect.top - int(self.camera.offset_y) - 20
                        self.damage_texts.add(DamageText(tx, ty, str(int(damage)), (255,0,0)))
                    except Exception:
                        pass

                    try:
                        if getattr(self, "audio", None):
                            self.audio.play_sfx("hit", volume=0.8)
                            if critico:
                                self.audio.play_sfx("crit", volume=0.9)
                    except Exception:
                        pass
                    try:
                        if critico and getattr(self, "flash", None):
                            self.flash.trigger()
                    except Exception:
                        pass

                    try:
                        dx = enemy.rect.centerx - self.player.rect.centerx
                        dy = enemy.rect.centery - self.player.rect.centery
                        dist = math.hypot(dx, dy) or 1.0
                        nx, ny = dx / dist, dy / dist
                        kb_strength = min(8, 2 + int(damage) // 2)
                        frames = 6
                        self.enemy_knockbacks[enemy] = [nx * kb_strength, ny * kb_strength, frames]
                        self.enemy_shakes[enemy] = 220
                    except Exception:
                        pass

                    try:
                        self.last_checkpoint = (self.player.rect.x, self.player.rect.y)
                    except Exception:
                        pass
                else:
                    try:
                        tx = enemy.rect.centerx - int(self.camera.offset_x)
                        ty = enemy.rect.top - int(self.camera.offset_y) - 20
                        self.damage_texts.add(DamageText(tx, ty, "FALLO", (200,200,200)))
                    except Exception:
                        pass

    # pause modal (keeps previous robust behavior)
    def process_pause_menu(self):
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_game()
                    self.quit_and_cleanup()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
                    self.paused = False
                    return
                handled_by_pausa = False
                try:
                    if hasattr(self.pausa_menu, "handle_event"):
                        try:
                            res = self.pausa_menu.handle_event(event)
                            handled_by_pausa = bool(res) if res is not None else True
                        except TypeError:
                            self.pausa_menu.handle_event(event)
                            handled_by_pausa = True
                except Exception:
                    handled_by_pausa = False
                if not handled_by_pausa:
                    if event.type == pygame.KEYDOWN:
                        if hasattr(self.pausa_menu, "options") and hasattr(self.pausa_menu, "selected"):
                            if event.key in (pygame.K_UP, pygame.K_w):
                                try:
                                    self.pausa_menu.selected = (self.pausa_menu.selected - 1) % len(self.pausa_menu.options)
                                except Exception:
                                    pass
                            elif event.key in (pygame.K_DOWN, pygame.K_s):
                                try:
                                    self.pausa_menu.selected = (self.pausa_menu.selected + 1) % len(self.pausa_menu.options)
                                except Exception:
                                    pass
                            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                                try:
                                    sel = getattr(self.pausa_menu, "selected", 0)
                                    if hasattr(self.pausa_menu, "activate"):
                                        try:
                                            self.pausa_menu.activate(sel)
                                        except Exception:
                                            pass
                                    elif hasattr(self.pausa_menu, "select_option"):
                                        try:
                                            self.pausa_menu.select_option(sel)
                                        except Exception:
                                            pass
                                    else:
                                        try:
                                            opt = self.pausa_menu.options[sel].lower()
                                            if "continu" in opt or "reanudar" in opt or "resume" in opt:
                                                self.paused = False
                                                return
                                            if "menu" in opt or "salir" in opt or "volver" in opt:
                                                self.paused = False
                                                self.in_menu = True
                                                return
                                        except Exception:
                                            pass
                                except Exception:
                                    pass
            try:
                if hasattr(self.pausa_menu, "draw"):
                    try:
                        self.pausa_menu.draw(self.screen)
                    except Exception:
                        self.screen.fill((12, 12, 18))
                        font = pygame.font.SysFont("arial", 36)
                        text = font.render("PAUSA", True, (255,255,255))
                        self.screen.blit(text, (ANCHO//2 - text.get_width()//2, ALTURA//2 - text.get_height()//2))
                else:
                    s = pygame.Surface((ANCHO, ALTURA))
                    s.set_alpha(200)
                    s.fill((0,0,0))
                    self.screen.blit(s, (0,0))
                    font = pygame.font.SysFont("arial", 36)
                    text = font.render("PAUSA - P/Esc para continuar", True, (255,255,255))
                    self.screen.blit(text, (ANCHO//2 - text.get_width()//2, ALTURA//2 - text.get_height()//2))
            except Exception:
                pass
            pygame.display.flip()
            try:
                self.clock.tick(FPS)
            except Exception:
                time.sleep(0.016)

    def start_new_game(self):
        if self.require_character:
            print("Debes crear un personaje antes de jugar.")
            return False
        if self.character:
            try:
                self.player = Player.from_character(self.character, 200, 300)
            except Exception:
                try:
                    self.player = Player(200, 300)
                except Exception:
                    self.player = None
            if not self.player:
                return False

            try:
                self.player.velocidad = 7
            except Exception:
                pass
            try:
                self.player.actualizar_stats()
            except Exception:
                pass
            if not hasattr(self.player, "nivel"):
                self.player.nivel = 1
            if not hasattr(self.player, "exp"):
                self.player.exp = 0
            if not hasattr(self.player, "stat_points"):
                try:
                    self.player.stat_points = int(getattr(self.player, "stat_points", 0))
                except Exception:
                    try:
                        setattr(self.player, "stat_points", 0)
                    except Exception:
                        pass

            # apply per-level derived attributes via external module
            try:
                apply_level_progression_to_player(self.player, int(getattr(self.player, "nivel", 1)))
            except Exception:
                pass

            try:
                self._shrink_player(scale=0.92)
            except Exception:
                pass

            try:
                self.stats_ui = StatsUI(self.player)
            except Exception:
                self.stats_ui = None
            self.level_up_menu.player = self.player
            self.enemies = []
            spawn_random_enemies(self, 8)
            self.last_checkpoint = (200, 300)
            if hasattr(self.world, "set_spawn_protection"):
                self.world.set_spawn_protection(self.player.rect.centerx, self.player.rect.centery, radius_tiles=10)
            try:
                if hasattr(self.world, "request_chunks_around"):
                    self.world.request_chunks_around(self.player.rect.centerx, self.player.rect.centery)
            except Exception:
                pass
            try:
                self.em = EnergiaMaldita(self.player)
            except Exception:
                self.em = None
            try:
                self.ensure_player_not_in_solid()
            except Exception:
                pass
            try:
                cx, cy = self.player.rect.center
                self.camera.offset_x = float(max(0.0, cx - (ANCHO / 2.0) / self.zoom))
                self.camera.offset_y = float(max(0.0, cy - (ALTURA / 2.0) / self.zoom))
            except Exception:
                pass
            return True
        return False

    def _start_tutorial(self):
        self.tutorial_active = True
        try:
            self.tutorial_world = TutorialWorld(tile_size=self.tile_size)
        except Exception:
            self.tutorial_world = None
        try:
            self.player = Player.from_character(self.character or {}, 100, 100)
        except Exception:
            try:
                self.player = Player(100, 100)
            except Exception:
                self.player = None
        if not self.player:
            self.tutorial_active = False
            return False
        if not hasattr(self.player, "nivel"):
            self.player.nivel = 1
        if not hasattr(self.player, "exp"):
            self.player.exp = 0
        if not hasattr(self.player, "stat_points"):
            try:
                self.player.stat_points = 0
            except Exception:
                pass

        # apply per-level derived attributes for tutorial player
        try:
            apply_level_progression_to_player(self.player, int(getattr(self.player, "nivel", 1)))
        except Exception:
            pass

        try:
            self._shrink_player(scale=0.92)
        except Exception:
            pass
        self.player.velocidad = 7
        try:
            self.player.actualizar_stats()
        except Exception:
            pass
        try:
            self.stats_ui = StatsUI(self.player)
        except Exception:
            self.stats_ui = None
        self.level_up_menu.player = self.player
        self.tutorial_enemies = [Enemy(320, 160, size=48, color=(220,0,0))]
        if hasattr(self.world, "set_spawn_protection"):
            self.world.set_spawn_protection(self.player.rect.centerx, self.player.rect.centery, radius_tiles=10)
        try:
            self.em = EnergiaMaldita(self.player)
        except Exception:
            self.em = None
        try:
            self.ensure_player_not_in_solid()
        except Exception:
            pass
        try:
            cx, cy = self.player.rect.center
            self.camera.offset_x = float(max(0.0, cx - (ANCHO / 2.0) / self.zoom))
            self.camera.offset_y = float(max(0.0, cy - (ALTURA / 2.0) / self.zoom))
        except Exception:
            pass

    # main loop (event handling, update, draw)
    def run(self):
        frame_count = 0
        render_surface = pygame.Surface((ANCHO, ALTURA))
        while True:
            frame_count += 1

            if self.paused:
                self.process_pause_menu()
                continue

            # death modal
            if getattr(self, "is_dead", False):
                if getattr(self, "no_lives_left", False):
                    try:
                        self.death_screen.draw_final(self.screen)
                        pygame.display.flip()
                        pygame.time.delay(1600)
                    except Exception:
                        pass
                    self.is_dead = False
                    self.no_lives_left = False
                    self.in_menu = True
                    continue
                while getattr(self, "is_dead", False):
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            self.quit_and_cleanup()
                        if ev.type == pygame.KEYDOWN:
                            if ev.key in (pygame.K_UP, pygame.K_w):
                                self.death_screen.selected = (self.death_screen.selected - 1) % len(self.death_screen.options)
                            elif ev.key in (pygame.K_DOWN, pygame.K_s):
                                self.death_screen.selected = (self.death_screen.selected + 1) % len(self.death_screen.options)
                            elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                                sel = self.death_screen.selected
                                if sel == 0:
                                    try:
                                        if getattr(self, "pending_death_pos", None) and self.player:
                                            dx, dy = self.pending_death_pos
                                            self.player.rect.x, self.player.rect.y = dx, dy
                                            self.player.hp = self.player.max_hp
                                            self.pending_death_pos = None
                                        elif self.player:
                                            self.player.rect.x, self.player.rect.y = self.last_checkpoint
                                            self.player.hp = self.player.max_hp
                                    except Exception:
                                        pass
                                    self.is_dead = False
                                    break
                                else:
                                    try:
                                        self.save_game()
                                    except Exception:
                                        pass
                                    self.in_menu = True
                                    self.is_dead = False
                                    break
                    try:
                        self.death_screen.draw(self.screen)
                        pygame.display.flip()
                    except Exception:
                        pass
                    try:
                        self.clock.tick(FPS)
                    except Exception:
                        time.sleep(0.016)
                continue

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_game()
                    self.quit_and_cleanup()

                # Chat toggle: T toggles open/close; ESC also closes while open.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    # toggle chat state
                    self.fairy_chat_active = not self.fairy_chat_active
                    if self.fairy_chat_active:
                        self.fairy_chat_input = ""
                    else:
                        self.fairy_chat_input = ""
                    # consume event
                    continue

                # If chat active, capture typing (Enter/Backspace/ESC/unicode)
                if self.fairy_chat_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            text = self.fairy_chat_input.strip()
                            if text != "":
                                self.fairy_chat_history.append(("user", text))
                                try:
                                    self.start_fairy_request(text)
                                except Exception:
                                    pass
                            self.fairy_chat_input = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.fairy_chat_input = self.fairy_chat_input[:-1]
                        elif event.key == pygame.K_ESCAPE:
                            # close chat with ESC
                            self.fairy_chat_active = False
                            self.fairy_chat_input = ""
                        else:
                            if hasattr(event, "unicode") and event.unicode and ord(event.unicode) >= 32:
                                self.fairy_chat_input += event.unicode
                    # consume event (don't forward to other systems)
                    continue

                # Stats UI handling: allow stats_ui to consume keys, then auto-close if puntos == 0
                if self.stats_open and getattr(self, "stats_ui", None) and event.type == pygame.KEYDOWN:
                    # Prevent ANY decrement key from being forwarded (LEFT/A)
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        # ignore decrement attempts entirely in gameplay
                        continue
                    try:
                        self.stats_ui.handle_key(event.key)
                        # sync remaining points
                        try:
                            remaining = getattr(self.stats_ui, "puntos", getattr(self.stats_ui, "points", None))
                            if remaining is not None:
                                try:
                                    self.player.stat_points = int(remaining)
                                except Exception:
                                    try:
                                        setattr(self.player, "stat_points", int(remaining))
                                    except Exception:
                                        pass
                                # auto-close if no points left
                                try:
                                    if int(remaining) <= 0:
                                        self.stats_open = False
                                except Exception:
                                    pass
                        except Exception:
                            pass
                        # consume event
                        continue
                    except Exception:
                        pass

                # otherwise pass to menu or in-game handlers
                if self.in_menu:
                    self._handle_menu_event(event)
                else:
                    try:
                        self._handle_in_game_event(event)
                    except Exception:
                        pass

            # Updates (AI, NPCs, enemies, knockbacks, camera)
            ui_open = self.in_menu or self.paused or self.fairy_chat_active or self.fairy_chat_waiting or self.stats_open or self.char_creator or self.is_dead or self.tutorial_active or self.dialogue.is_active()
            if not ui_open and self.player:
                try:
                    self.player.handle_input(self.world)
                except Exception:
                    pass

                for npc in self.npcs:
                    try:
                        npc.update(None)
                    except Exception:
                        pass

                for enemy in list(self.enemies):
                    if enemy.hp > 0:
                        kb = self.enemy_knockbacks.get(enemy)
                        if kb:
                            try:
                                vx, vy, frames = kb
                                enemy.rect.x += int(round(vx))
                                enemy.rect.y += int(round(vy))
                                frames -= 1
                                if frames <= 0:
                                    try:
                                        del self.enemy_knockbacks[enemy]
                                    except KeyError:
                                        pass
                                else:
                                    self.enemy_knockbacks[enemy][2] = frames
                            except Exception:
                                try:
                                    del self.enemy_knockbacks[enemy]
                                except Exception:
                                    pass
                        try:
                            enemy.seguir_jugador(self.player, self.world)
                        except Exception:
                            pass

                        # --- Collision handling: separate entities to avoid overlapping ---
                        try:
                            if self.player and enemy.rect.colliderect(self.player.rect):
                                # vector from player to enemy
                                dx = enemy.rect.centerx - self.player.rect.centerx
                                dy = enemy.rect.centery - self.player.rect.centery
                                if dx == 0 and dy == 0:
                                    dx = 0.01
                                dist = math.hypot(dx, dy) or 1.0
                                nx = dx / dist
                                ny = dy / dist

                                # compute overlaps on each axis
                                overlap_x = (enemy.rect.width / 2.0) + (self.player.rect.width / 2.0) - abs(dx)
                                overlap_y = (enemy.rect.height / 2.0) + (self.player.rect.height / 2.0) - abs(dy)

                                if overlap_x > 0 and overlap_y > 0:
                                    push = int(max(overlap_x, overlap_y) + 1)
                                    old_x, old_y = enemy.rect.x, enemy.rect.y
                                    enemy.rect.x += int(round(nx * push))
                                    enemy.rect.y += int(round(ny * push))
                                    # if enemy got pushed into solid, revert and try pushing player instead
                                    try:
                                        if hasattr(self.world, "is_pixel_solid") and self.world.is_pixel_solid(enemy.rect.centerx, enemy.rect.centery):
                                            enemy.rect.x, enemy.rect.y = old_x, old_y
                                            try:
                                                self.player.rect.x -= int(round(nx * push))
                                                self.player.rect.y -= int(round(ny * push))
                                                if hasattr(self.world, "is_pixel_solid") and self.world.is_pixel_solid(self.player.rect.centerx, self.player.rect.centery):
                                                    self.player.rect.x += int(round(nx * push))
                                                    self.player.rect.y += int(round(ny * push))
                                            except Exception:
                                                try:
                                                    self.player.rect.x += int(round(nx * push))
                                                    self.player.rect.y += int(round(ny * push))
                                                except Exception:
                                                    pass
                                    except Exception:
                                        # if world check fails, keep enemy in pushed position
                                        pass
                        except Exception:
                            pass

                        # After separation attempt, handle contact (damage/knockback) if still colliding
                        try:
                            if enemy.rect.colliderect(self.player.rect):
                                try:
                                    damage = enemy.ataque(self.player)
                                except Exception:
                                    damage = 0
                                if damage and damage > 0:
                                    try:
                                        tx = self.player.rect.centerx - int(self.camera.offset_x)
                                        ty = self.player.rect.top - int(self.camera.offset_y) - 30
                                        self.damage_texts.add(DamageText(tx, ty, str(int(damage)), (255, 0, 0)))
                                    except Exception:
                                        pass
                                    try:
                                        dx = self.player.rect.centerx - enemy.rect.centerx
                                        dy = self.player.rect.centery - enemy.rect.centery
                                        dist = math.hypot(dx, dy) or 1.0
                                        nx, ny = dx / dist, dy / dist
                                        kb_strength = min(6, 2 + int(damage) // 2)
                                        self.player.rect.x += int(round(nx * kb_strength))
                                        self.player.rect.y += int(round(ny * kb_strength))
                                        if hasattr(self.world, "is_pixel_solid"):
                                            if self.world.is_pixel_solid(self.player.rect.centerx, self.player.rect.centery):
                                                self.player.rect.x -= int(round(nx * kb_strength))
                                                self.player.rect.y -= int(round(ny * kb_strength))
                                    except Exception:
                                        pass
                                    if self.player.hp <= 0:
                                        if self.player.lives > 1:
                                            self.player.lives -= 1
                                            self.player.hp = self.player.max_hp
                                            self.player.rect.x, self.player.rect.y = self.last_checkpoint
                                        else:
                                            self.player.lives = 0
                                            self.is_dead = True
                                            self.no_lives_left = True
                        except Exception:
                            pass

                    else:
                        try:
                            xp_amount = getattr(enemy, "xp", None)
                            if xp_amount is None:
                                xp_amount = max(1, enemy.rect.width // 8)
                            try:
                                self.award_xp(xp_amount, show_text=True, src_pos=enemy.rect.center)
                            except Exception:
                                pass
                        except Exception:
                            pass
                        try:
                            self.enemies.remove(enemy)
                        except ValueError:
                            pass
                        try:
                            spawn_random_enemies(self, 1, near_player=True)
                        except Exception:
                            pass

                # rest of update loop continues unchanged...
                # clean up shakes
                remove_shakes = []
                for enemy, remaining in list(self.enemy_shakes.items()):
                    remaining -= self.clock.get_time()
                    if remaining <= 0:
                        remove_shakes.append(enemy)
                    else:
                        self.enemy_shakes[enemy] = remaining
                for e in remove_shakes:
                    try:
                        del self.enemy_shakes[e]
                    except KeyError:
                        pass

                # camera follow
                px, py = self.player.rect.center
                desired_cam_x = px - (ANCHO / 2.0) / self.zoom
                desired_cam_y = py - (ALTURA / 2.0) / self.zoom
                if self.camera.center_immediately:
                    self.camera.offset_x = float(max(0.0, desired_cam_x))
                    self.camera.offset_y = float(max(0.0, desired_cam_y))
                else:
                    smooth = getattr(self.camera, "smooth", 0.08)
                    self.camera.offset_x += (desired_cam_x - self.camera.offset_x) * smooth
                    self.camera.offset_y += (desired_cam_y - self.camera.offset_y) * smooth
                    if self.camera.offset_x < 0:
                        self.camera.offset_x = 0.0
                    if self.camera.offset_y < 0:
                        self.camera.offset_y = 0.0

            # DRAW
            render_surface.fill((0,0,0))
            if not self.in_menu:
                try:
                    self.world.draw(render_surface, (self.camera.offset_x, self.camera.offset_y))
                except Exception:
                    pass

                for npc in self.npcs:
                    try:
                        npc.draw(render_surface, (self.camera.offset_x, self.camera.offset_y))
                    except Exception:
                        pass

                if self.player:
                    try:
                        self.player.draw(render_surface, (self.camera.offset_x, self.camera.offset_y))
                    except Exception:
                        pass

                for enemy in self.enemies:
                    if enemy.hp > 0:
                        try:
                            if enemy in self.enemy_shakes and self.enemy_shakes.get(enemy, 0) > 0:
                                strength = 4
                                sx = random.randint(-strength, strength)
                                sy = random.randint(-strength, strength)
                                enemy.rect.x += sx
                                enemy.rect.y += sy
                                enemy.draw(render_surface, (self.camera.offset_x, self.camera.offset_y))
                                enemy.rect.x -= sx
                                enemy.rect.y -= sy
                            else:
                                enemy.draw(render_surface, (self.camera.offset_x, self.camera.offset_y))
                        except Exception:
                            ex = enemy.rect.x - int(self.camera.offset_x)
                            ey = enemy.rect.y - int(self.camera.offset_y)
                            pygame.draw.rect(render_surface, (200,50,50), (ex, ey, enemy.rect.width, enemy.rect.height))

                try:
                    nowt = pygame.time.get_ticks()
                    for arm in list(self.arms):
                        if hasattr(arm, "alive") and callable(getattr(arm, "alive")):
                            try:
                                if arm.alive(nowt):
                                    arm.draw(render_surface, (self.camera.offset_x, self.camera.offset_y))
                                else:
                                    try:
                                        self.arms.remove(arm)
                                    except ValueError:
                                        pass
                            except Exception:
                                try:
                                    self.arms.remove(arm)
                                except Exception:
                                    pass
                        else:
                            try:
                                start, end, created = arm
                                duration = 220
                                elapsed = nowt - created
                                if elapsed < duration:
                                    t = max(0.0, min(1.0, elapsed / float(duration)))
                                    width = max(2, int(8 * (1 - t)))
                                    sx = int(start[0] - self.camera.offset_x)
                                    sy = int(start[1] - self.camera.offset_y)
                                    ex = int(end[0] - self.camera.offset_x)
                                    ey = int(end[1] - self.camera.offset_y)
                                    pygame.draw.line(render_surface, (255,200,60), (sx, sy), (ex, ey), width)
                                    pygame.draw.circle(render_surface, (255,200,60), (ex, ey), max(3, int(6 * (1 - t/1.2))))
                                else:
                                    try:
                                        self.arms.remove(arm)
                                    except ValueError:
                                        pass
                            except Exception:
                                try:
                                    self.arms.remove(arm)
                                except Exception:
                                    pass
                except Exception:
                    pass

                try:
                    self.dice_ui.draw(render_surface)
                except Exception:
                    pass
                try:
                    self.flash.draw(render_surface)
                except Exception:
                    pass

                self.damage_texts.update()
                self.damage_texts.draw(render_surface)

                # --- NEW: show quick info for the nearest enemy (uses new Enemy fields we added) ---
                try:
                    # find nearest visible enemy to player
                    nearest = None
                    min_d = float("inf")
                    for e in self.enemies:
                        if getattr(e, "hp", 0) > 0:
                            dx = e.rect.centerx - self.player.rect.centerx
                            dy = e.rect.centery - self.player.rect.centery
                            d = math.hypot(dx, dy)
                            if d < min_d:
                                min_d = d
                                nearest = e
                    if nearest is not None and min_d < 300:
                        # draw a compact info panel on the top-right
                        panel_w = 220
                        panel_h = 110
                        px = ANCHO - panel_w - 10
                        py = 10
                        info_surf = pygame.Surface((panel_w, panel_h))
                        info_surf.set_alpha(210)
                        info_surf.fill((18,18,28))
                        pygame.draw.rect(info_surf, (200,200,200), (0,0,panel_w,panel_h), 2)
                        try:
                            title = self.font_small.render("Enemy info", True, (230,230,230))
                            info_surf.blit(title, (8, 6))
                            # fields: Size, HP, AC, Damage dice, XP, Speed, Range
                            size_txt = self.font_small.render(f"Size: {getattr(nearest, 'size', nearest.rect.width)}", True, (220,220,220))
                            info_surf.blit(size_txt, (8, 28))
                            try:
                                hp_txt = self.font_small.render(f"HP: {int(getattr(nearest,'hp',0))}/{int(getattr(nearest,'max_hp',0))}", True, (220,180,180))
                                info_surf.blit(hp_txt, (8, 46))
                            except Exception:
                                pass
                            ac_txt = self.font_small.render(f"AC: {getattr(nearest, 'ACD', getattr(nearest, 'AC', 'N/A'))}", True, (200,220,200))
                            info_surf.blit(ac_txt, (8, 64))
                            # damage dice
                            try:
                                dd = getattr(nearest, "damage_dice", None)
                                if dd:
                                    dmg_txt = self.font_small.render(f"Damage: {dd[0]}d{dd[1]}", True, (220,220,150))
                                    info_surf.blit(dmg_txt, (110, 28))
                                xp_txt = self.font_small.render(f"XP: {getattr(nearest, 'xp', getattr(nearest, 'experience', 0))}", True, (180,220,180))
                                info_surf.blit(xp_txt, (110, 46))
                            except Exception:
                                pass
                            try:
                                vel_txt = self.font_small.render(f"Speed: {getattr(nearest,'velocidad',0)}", True, (200,200,255))
                                info_surf.blit(vel_txt, (110, 64))
                            except Exception:
                                pass
                            try:
                                ar_txt = self.font_small.render(f"Range: {getattr(nearest,'attack_range',0)}", True, (190,190,190))
                                info_surf.blit(ar_txt, (8, 82))
                                scale_txt = self.font_small.render(f"Scale: {round(getattr(nearest,'scale',1.0),2)}", True, (190,190,255))
                                info_surf.blit(scale_txt, (110, 82))
                            except Exception:
                                pass
                        except Exception:
                            pass
                        render_surface.blit(info_surf, (px, py))
                except Exception:
                    pass
                # --- end of NEW info panel ---

                if self.dialogue.is_active():
                    try:
                        self.dialogue_ui.draw(render_surface)
                    except Exception:
                        pass

                try:
                    if self.player:
                        curxp = int(getattr(self.player, "exp", 0))
                        lvl = int(getattr(self.player, "nivel", 1))
                        needed = self.default_xp_formula(lvl)
                        draw_xp_bar(render_surface, (ANCHO-420)//2, 8, 420, 18, curxp, needed, lvl, self.font_small)
                except Exception:
                    pass

                if self.fairy_chat_active or self.fairy_chat_history:
                    try:
                        self._draw_chat_overlay(render_surface)
                    except Exception:
                        pass

                if self.stats_open and getattr(self, "stats_ui", None):
                    try:
                        try:
                            self.stats_ui.draw(render_surface)
                        except TypeError:
                            self.stats_ui.draw(render_surface, x=60, y=80)
                    except Exception:
                        pass

            else:
                self.screen.fill((0,0,0))
                try:
                    self.menu.draw(self.screen)
                except Exception:
                    pass
                pygame.display.flip()
                self.clock.tick(FPS)
                continue

            try:
                self.screen.blit(render_surface, (0,0))
            except Exception:
                pass

            # HUD draw
            try:
                if self.player:
                    try:
                        draw_health_bar(self.screen, 10, 10, self.player.hp, self.player.max_hp, width=160, height=16)
                        hp_text = self.font_small.render(f"HP: {int(self.player.hp)}/{int(self.player.max_hp)}  Vidas: {getattr(self.player,'lives',0)}", True, (255,255,255))
                        self.screen.blit(hp_text, (12, 12))
                    except Exception:
                        pass
            except Exception:
                pass

            try:
                draw_em_bar(self.screen, 12, 34, getattr(self, "em", None), width=160, height=10, font=self.font_small)
            except Exception:
                pass

            try:
                if getattr(self, "last_hit", None) is not None and getattr(self, "last_hit_time", 0) > 0:
                    elapsed = pygame.time.get_ticks() - self.last_hit_time
                    if elapsed < self.last_hit_duration:
                        pct = 1.0 - (elapsed / float(self.last_hit_duration))
                        alpha = int(40 + 215 * max(0.0, min(pct, 1.0)))
                        s = pygame.Surface((220, 28), pygame.SRCALPHA)
                        s.fill((10, 10, 10, int(alpha * 0.6)))
                        self.screen.blit(s, (10, 54))
                        hit_txt = self.font_small.render(f"Último golpe: {self.last_hit}", True, (255, 220, 80))
                        self.screen.blit(hit_txt, (14, 58))
                    else:
                        self.last_hit = None
                        self.last_hit_time = 0
            except Exception:
                pass

            pygame.display.flip()
            self.clock.tick(FPS)


# Main entry
if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except SystemExit:
        pass
    except Exception as e:
        print("Unhandled exception:", e)
        try:
            game.quit_and_cleanup(save=False)
        except Exception:
            pass
        raise