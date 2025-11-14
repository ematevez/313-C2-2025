# core/audio.py
# Simple audio manager for SFX and music (pygame.mixer).
import os
import pygame
from typing import Dict, Optional

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
SFX_DIR = os.path.join(ASSETS_DIR, "sfx")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")

class AudioManager:
    def __init__(self):
        # intenta inicializar el mixer (si no lo hizo pygame)
        try:
            pygame.mixer.init()
        except Exception:
            # si falla, seguimos sin sonido
            pass
        self.sfx: Dict[str, pygame.mixer.Sound] = {}
        self.master_volume = 1.0
        self.music_path: Optional[str] = None

    def load_sfx(self, name: str, filename: str):
        """Carga un sfx desde assets/sfx/<filename> y lo guarda como 'name'."""
        path = os.path.join(SFX_DIR, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"SFX not found: {path}")
        try:
            snd = pygame.mixer.Sound(path)
            snd.set_volume(self.master_volume)
            self.sfx[name] = snd
        except Exception:
            # No queremos crash si el formato no es soportado
            raise

    def play_sfx(self, name: str, volume: float = 1.0):
        """Reproduce un efecto de sonido ya cargado."""
        snd = self.sfx.get(name)
        if not snd:
            return
        try:
            snd.set_volume(max(0.0, min(1.0, volume * self.master_volume)))
            snd.play()
        except Exception:
            pass

    def play_music(self, filename: str, loops: int = -1, volume: float = 0.6):
        """Reproduce música de fondo (ruta relativa en assets/music)."""
        path = os.path.join(MUSIC_DIR, filename)
        if not os.path.exists(path):
            return
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(max(0.0, min(1.0, volume * self.master_volume)))
            pygame.mixer.music.play(loops=loops)
            self.music_path = path
        except Exception:
            pass

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def set_master_volume(self, v: float):
        self.master_volume = max(0.0, min(1.0, v))
        # aplicar a música y sfx existentes
        try:
            pygame.mixer.music.set_volume(self.master_volume)
        except Exception:
            pass
        for snd in self.sfx.values():
            try:
                snd.set_volume(self.master_volume)
            except Exception:
                pass