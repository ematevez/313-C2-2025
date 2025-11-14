# game/lvl_up_player_logic.py
# Lógica centralizada de progresión por nivel.
# Provee:
#  - get_proficiency_bonus(level)
#  - get_level_point_bonus(level)
#  - cursed_energy_base_for(level)
#  - apply_level_progression_to_player(player, level)
#
# Reemplaza cualquier versión anterior; guarda este archivo en game/lvl_up_player_logic.py
# y reinicia el juego.

from typing import Optional

# Proficiency bonus por nivel (según la tabla que proporcionaste)
LEVEL_PROFICIENCY_BONUS = {
    1: 2, 2: 2, 3: 2, 4: 2,
    5: 3, 6: 3, 7: 3, 8: 3,
    9: 4, 10: 4, 11: 4, 12: 4,
    13: 5, 14: 5, 15: 5, 16: 5,
    17: 6, 18: 6, 19: 6, 20: 6,
}

# Puntos que se otorgan en hitos (no confundir con "proficiency")
LEVEL_POINT_BONUS_MILESTONES = {4, 8, 12, 16}
POINTS_PER_MILESTONE = 2

# Movimiento sin armadura por nivel (pies)
UNARMORED_MOVEMENT_BY_LEVEL = {
    1: 10, 2: 10, 3: 10,
    4: 15, 5: 15, 6: 15,
    7: 20, 8: 20, 9: 20,
    10: 25, 11: 25, 12: 25,
    13: 30, 14: 30, 15: 30,
    16: 35, 17: 35, 18: 35,
    19: 40, 20: 40,
}

# Dado de artes marciales por nivel (string)
MARTIAL_ARTS_BY_LEVEL = {
    1: None,
    2: "1d4", 3: "1d4",
    4: "1d6", 5: "1d6", 6: "1d6", 7: "1d6", 8: "1d6",
    9: "1d8", 10: "1d8", 11: "1d8", 12: "1d8",
    13: "1d10", 14: "1d10", 15: "1d10", 16: "1d10",
    17: "1d12", 18: "1d12", 19: "1d12", 20: "1d12",
}


def get_proficiency_bonus(level: int) -> int:
    """Devuelve el proficiency bonus para el nivel dado."""
    try:
        return int(LEVEL_PROFICIENCY_BONUS.get(int(level), 0))
    except Exception:
        return 0


def get_level_point_bonus(level: int) -> int:
    """
    Devuelve la cantidad de puntos de estadística que se otorgan al subir a `level`.
    Sólo devuelve POINTS_PER_MILESTONE en los hitos definidos.
    """
    try:
        lvl = int(level)
        return POINTS_PER_MILESTONE if lvl in LEVEL_POINT_BONUS_MILESTONES else 0
    except Exception:
        return 0


def cursed_energy_base_for(level: int) -> int:
    """
    Base de energía maldita por nivel. Según la tabla: base = level * 2.
    Retorna int >= 0.
    """
    try:
        lvl = int(level)
        return max(0, lvl * 2)
    except Exception:
        return 0


def _compute_charisma_mod_from_player(player) -> int:
    """
    Determina un modificador de Carisma que se pueda sumar a la energía maldita:
     - usa player.carisma_mod si existe y no es None
     - si sólo hay player.carisma (puntaje), calcula (carisma - 10)//2
     - si nada, retorna 0
    Función defensiva (no lanza).
    """
    try:
        if player is None:
            return 0
        if hasattr(player, "carisma_mod") and getattr(player, "carisma_mod") is not None:
            try:
                return int(getattr(player, "carisma_mod") or 0)
            except Exception:
                pass
        if hasattr(player, "carisma"):
            try:
                raw = int(getattr(player, "carisma") or 0)
                return (raw - 10) // 2
            except Exception:
                pass
    except Exception:
        pass
    return 0


def apply_level_progression_to_player(player, level: int) -> None:
    """
    Aplica al objeto `player` los atributos derivados del `level`:
      - player.proficiency_bonus (int)
      - player.cursed_energy_base (int)
      - player.cursed_energy_total (int) = base + charisma_mod
      - player.unarmored_movement_bonus (int, pies)
      - player.martial_arts_die (str o None)
    Este método es defensivo: intenta setear atributos, usando setattr si es necesario,
    y no lanza excepciones hacia el llamador.
    """
    if player is None:
        return
    try:
        lvl = int(level)
    except Exception:
        return

    try:
        prof = get_proficiency_bonus(lvl)
        try:
            player.proficiency_bonus = int(prof)
        except Exception:
            try:
                setattr(player, "proficiency_bonus", int(prof))
            except Exception:
                pass
    except Exception:
        pass

    try:
        base = cursed_energy_base_for(lvl)
        cha_mod = _compute_charisma_mod_from_player(player)
        total = int(base) + int(cha_mod)
        try:
            player.cursed_energy_base = int(base)
            player.cursed_energy_total = int(total)
        except Exception:
            try:
                setattr(player, "cursed_energy_base", int(base))
                setattr(player, "cursed_energy_total", int(total))
            except Exception:
                pass
    except Exception:
        pass

    try:
        um = UNARMORED_MOVEMENT_BY_LEVEL.get(lvl, 0)
        try:
            player.unarmored_movement_bonus = int(um)
        except Exception:
            try:
                setattr(player, "unarmored_movement_bonus", int(um))
            except Exception:
                pass
    except Exception:
        pass

    try:
        mad = MARTIAL_ARTS_BY_LEVEL.get(lvl, None)
        try:
            player.martial_arts_die = mad
        except Exception:
            try:
                setattr(player, "martial_arts_die", mad)
            except Exception:
                pass
    except Exception:
        pass


__all__ = [
    "get_proficiency_bonus",
    "get_level_point_bonus",
    "cursed_energy_base_for",
    "apply_level_progression_to_player",
    "UNARMORED_MOVEMENT_BY_LEVEL",
    "MARTIAL_ARTS_BY_LEVEL",
]