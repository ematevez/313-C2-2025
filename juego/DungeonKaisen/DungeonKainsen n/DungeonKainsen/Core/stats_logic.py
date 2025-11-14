# core/stats_logic.py
# Centraliza la lógica para bonificadores y reglas relacionadas con stats.
# Permite ajustar el "peso" de los modificadores desde settings si lo deseas.

try:
    from settings import STAT_MODIFIER_SCALE
except Exception:
    # Si no existe STAT_MODIFIER_SCALE en settings, usamos un valor por defecto.
    STAT_MODIFIER_SCALE = 1.5

def bonus_constitucion(constitucion):
    """
    Calcula el bonus de constitución para HP.
    Acepta int o dict tipo {"value":n}.
    Devuelve un entero que se sumará (o multiplicará levemente) a la vida máxima.
    """
    if isinstance(constitucion, dict):
        try:
            c = int(constitucion.get("value", 10))
        except Exception:
            c = 10
    else:
        try:
            c = int(constitucion)
        except Exception:
            c = 10
    base = (c - 10) // 2
    # Escalar la contribución a HP para que constitución tenga más peso:
    return base * 2  # multiplicador simple para más impacto en HP

def stat_modifier(score):
    """
    Calcula el modificador de una stat (fuerza/destreza/etc) aplicando STAT_MODIFIER_SCALE.
    Antes: (score - 10)//2
    Ahora: redondeado( ((score - 10)/2) * STAT_MODIFIER_SCALE )
    """
    if isinstance(score, dict):
        try:
            s = int(score.get("value", 10))
        except Exception:
            s = 10
    else:
        try:
            s = int(score)
        except Exception:
            s = 10
    base = (s - 10) / 2.0
    scaled = round(base * STAT_MODIFIER_SCALE)
    return int(scaled)