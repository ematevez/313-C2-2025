# game/save_load.py
# Guardado y carga funcional del estado principal (player + world seed + character)

import json
import os
from Core.texto import DamageText
from Core.energia_maldita import EnergiaMaldita
from Core.jugador import Player
from Core.world import World
from Core.stats import StatsUI
from game.spawn import spawn_random_enemies
from settings import *
SAVE_DEFAULT = "savegame.json"

def save_game_data(game):
    if not getattr(game, "player", None):
        return False
    data = {
        "player": {
            "x": int(game.player.rect.x),
            "y": int(game.player.rect.y),
            "hp": int(game.player.hp),
            "max_hp": int(game.player.max_hp),
            "nivel": int(game.player.nivel),
            "exp": int(game.player.exp),
            "lives": int(game.player.lives)
        },
        "world": {
            "seed": getattr(game.world, "seed", 12121)
        },
        "character": game.character
    }
    path = getattr(game, "SAVE_FILE", SAVE_DEFAULT)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print("Error saving:", e)
        return False

def load_game_data(game):
    path = getattr(game, "SAVE_FILE", SAVE_DEFAULT)
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("Error loading:", e)
        return False

    p = data.get("player", {})
    wc = data.get("world", {})
    chrdata = data.get("character", None)

    if not chrdata:
        return False

    try:
        game.player = Player.from_character(chrdata, p.get("x", 200), p.get("y", 300))
    except Exception:
        try:
            game.player = Player(p.get("x", 200), p.get("y", 300))
        except Exception:
            return False

    game.player.nivel = int(p.get("nivel", 1))
    game.player.exp = int(p.get("exp", 0))
    game.player.lives = int(p.get("lives", 3))
    game.player.max_hp = int(p.get("max_hp", getattr(game.player, "max_hp", 12)))
    game.player.hp = int(p.get("hp", game.player.max_hp))
    game.player.velocidad = 7
    try:
        game.player.actualizar_stats()
    except Exception:
        pass

    game.character = chrdata
    try:
        game.stats_ui = StatsUI(game.player)
    except Exception:
        game.stats_ui = None
    game.level_up_menu.player = game.player
    game.require_character = False

    seed = wc.get("seed", getattr(game.world, "seed", 12121))
    try:
        if getattr(game, "world", None):
            game.world.stop()
    except Exception:
        pass

    try:
        game.world = World(mapa=None, tile_size=game.tile_size, seed=seed)
    except Exception:
        game.world = World(mapa=None, tile_size=game.tile_size, seed=seed)

    if hasattr(game.world, "set_spawn_protection"):
        game.world.set_spawn_protection(game.player.rect.centerx, game.player.rect.centery, radius_tiles=10)
    try:
        game.world.request_chunks_around(game.player.rect.centerx, game.player.rect.centery)
    except Exception:
        pass

    game.enemies = []
    try:
        spawn_random_enemies(game, 8)
    except Exception:
        pass

    try:
        game.em = EnergiaMaldita(game.player)
    except Exception:
        game.em = None

    try:
        game.ensure_player_not_in_solid()
    except Exception:
        pass

    try:
        cx, cy = game.player.rect.center
        game.camera.offset_x = float(max(0.0, cx - (ANCHO / 2.0) / getattr(game, "zoom", 1.0)))
        game.camera.offset_y = float(max(0.0, cy - (ALTURA / 2.0) / getattr(game, "zoom", 1.0)))
    except Exception:
        pass

    return True