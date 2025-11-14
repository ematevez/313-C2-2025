# core/character_creator.py
# Interfaz de creación de personaje (point-buy). Adaptado para usar settings.CHAR_FILE si existe.
import pygame
import json
import os
import math
from settings import CHAR_FILE as SETTINGS_CHAR_FILE

STAT_NAMES = ["Fuerza", "Destreza", "Constitución", "Inteligencia", "Sabiduría", "Carisma"]
POINTS_AVAILABLE = 27
CHAR_FILE = SETTINGS_CHAR_FILE if SETTINGS_CHAR_FILE else "character.json"

def calculate_mod(score):
    return (score - 10) // 2

def cost_to_set_score(from_score, to_score):
    if to_score < from_score:
        return -cost_to_set_score(to_score, from_score)
    cost = 0
    x = from_score
    while x < to_score:
        nxt = x + 1
        if nxt <= 16:
            cost += 1
        else:
            cost += 2
        x = nxt
    return cost

class CharacterCreator:
    def __init__(self, screen, initial_scores=None):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 22)
        self.small = pygame.font.SysFont("arial", 18)
        self.selected = 0
        self.name = "Player"
        self.age = 18
        self.points = POINTS_AVAILABLE
        if initial_scores:
            self.scores = {s: max(10, int(initial_scores.get(s, 10))) for s in STAT_NAMES}
        else:
            self.scores = {s: 10 for s in STAT_NAMES}
        self._recompute_points()
        self.done = False
        self.cancelled = False
        self.input_mode = None

    def _recompute_points(self):
        spent = 0
        for s in STAT_NAMES:
            spent += cost_to_set_score(10, self.scores[s])
        self.points = POINTS_AVAILABLE - spent

    def increase(self):
        stat = STAT_NAMES[self.selected]
        cur = self.scores[stat]
        if cur >= 20:
            return
        new_score = cur + 1
        extra_cost = cost_to_set_score(cur, new_score)
        if self.points - extra_cost >= 0:
            self.scores[stat] = new_score
            self._recompute_points()

    def decrease(self):
        stat = STAT_NAMES[self.selected]
        cur = self.scores[stat]
        if cur <= 10:
            return
        new_score = cur - 1
        self.scores[stat] = new_score
        self._recompute_points()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.input_mode == "name":
                if event.key == pygame.K_RETURN:
                    self.input_mode = None
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    if event.unicode and ord(event.unicode) >= 32:
                        self.name += event.unicode
                return
            if self.input_mode == "age":
                if event.key == pygame.K_RETURN:
                    self.input_mode = None
                elif event.key == pygame.K_BACKSPACE:
                    s = str(self.age)
                    self.age = int(s[:-1]) if len(s) > 1 else 0
                else:
                    if event.unicode and event.unicode.isdigit():
                        self.age = int(str(self.age) + event.unicode)
                return

            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(STAT_NAMES)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(STAT_NAMES)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.increase()
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.decrease()
            elif event.key == pygame.K_n:
                self.input_mode = "name"
            elif event.key == pygame.K_g:
                self.input_mode = "age"
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._recompute_points()
                if self.points >= 0:
                    self.done = True
            elif event.key == pygame.K_ESCAPE:
                self.cancelled = True
                self.done = True

    def draw(self):
        w, h = self.screen.get_size()
        box_w, box_h = 560, 440
        x = w//2 - box_w//2
        y = h//2 - box_h//2
        pygame.draw.rect(self.screen, (18,18,28), (x,y,box_w,box_h))
        pygame.draw.rect(self.screen, (255,255,255), (x,y,box_w,box_h), 2)
        title = self.font.render("Crear personaje - Point buy (27 puntos)", True, (255,255,255))
        self.screen.blit(title, (x+20, y+12))

        for i, stat in enumerate(STAT_NAMES):
            color = (255,255,120) if i == self.selected else (200,200,200)
            val = self.scores[stat]
            mod = calculate_mod(val)
            next_cost = cost_to_set_score(val, val+1) if val < 20 else "-"
            line = f"{stat}: {val}  (mod {mod:+d})  next+1 cost: {next_cost}"
            text = self.font.render(line, True, color)
            self.screen.blit(text, (x+30, y+80 + i*40))

        info = self.small.render(f"Puntos restantes: {self.points}", True, (180, 220, 255))
        self.screen.blit(info, (x+30, y+80 + len(STAT_NAMES)*40 + 10))

        hint = self.small.render("Izq/Dcha +/-1 | N edita nombre | G edita edad | Enter confirma | Esc cancela", True, (180,180,180))
        self.screen.blit(hint, (x+30, y+80 + len(STAT_NAMES)*40 + 40))

        name_txt = self.small.render(f"Nombre: {self.name} (N)", True, (220,220,180))
        age_txt = self.small.render(f"Edad: {self.age} (G)", True, (220,220,180))
        self.screen.blit(name_txt, (x+30, y+80 + len(STAT_NAMES)*40 + 80))
        self.screen.blit(age_txt, (x+30, y+80 + len(STAT_NAMES)*40 + 110))

        if self.input_mode == "name":
            im = self.small.render("Editando nombre... Enter para terminar", True, (200,200,255))
            self.screen.blit(im, (x+30, y+box_h-40))
        if self.input_mode == "age":
            im = self.small.render("Editando edad... Enter para terminar", True, (200,200,255))
            self.screen.blit(im, (x+30, y+box_h-40))

    def save(self):
        data = {
            "name": self.name,
            "age": self.age,
            "scores": {}
        }
        for s in STAT_NAMES:
            val = int(self.scores[s])
            data["scores"][s] = {"value": val}
        try:
            with open(CHAR_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print("Error saving character:", e)
            return False

    @staticmethod
    def load_if_exists():
        if not os.path.exists(CHAR_FILE):
            return None
        try:
            with open(CHAR_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            scores = data.get("scores", {})
            normalized = {}
            for k in STAT_NAMES:
                v = scores.get(k)
                if isinstance(v, dict) and "value" in v:
                    normalized[k] = v
                elif isinstance(v, int):
                    normalized[k] = {"value": v, "mod": calculate_mod(v)}
                else:
                    normalized[k] = {"value": 10, "mod": 0}
            return {"name": data.get("name", "Player"), "age": data.get("age", 18), "scores": normalized}
        except Exception:
            return None