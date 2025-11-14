# settings.py
# Configuración global: ventana, escala y constantes del juego.
# Mantén este archivo sin importar módulos que a su vez importen settings (evita import circular).

# ---------------- Window / Engine ----------------
ANCHO = 1000
ALTURA = 1000
FPS = 120

# ---------------- Colors ----------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ---------------- Gameplay ----------------
RANGO_GOLPE = 80  # distancia máxima para golpear (pixels)

# ---------------- Scale (metros -> tiles -> pixels) ----------------
PIXELS_PER_METER = 35     # píxeles por metro
METERS_PER_TILE = 12       # metros que representa cada tile
TILE_SIZE = PIXELS_PER_METER * METERS_PER_TILE  # tile en píxeles

# ---------------- Save files ----------------
SAVE_FILE = "savegame.json"
CHAR_FILE = "character.json"

# ---------------- Stats scaling (tuneable) ----------------
# Valores >1 aumentan el peso de los bonificadores (impacto en daño/velocidad/etc).
# Puedes ajustar esto para poner más o menos peso a los modificadores.
STAT_MODIFIER_SCALE = 1.5

# ---------------- XP / leveling tuning ----------------
# Base XP per level used por default_xp_formula en game/core.py si lo deseas globalizar
XP_BASE_PER_LEVEL = 50