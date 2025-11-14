# core/energia_maldita.py
import random
import math

class EnergiaMaldita:
    def __init__(self, owner=None):
        """
        owner: objeto jugador que debe tener atributos `nivel` y `carisma`.
        """
        self.owner = None
        self.em_total_max = 0
        self.em_total = 0
        self.em_puño = 0
        self._per_punch_limit = 0
        if owner is not None:
            self.set_owner(owner)

    def set_owner(self, owner):
        """Asocia la EM a un jugador y recalcula máximos."""
        self.owner = owner
        nivel = getattr(owner, "nivel", 1)
        # corregido: obtener carisma por defecto 0 si no existe
        carisma = getattr(owner, "carisma", 0)
        try:
            nivel = int(nivel)
            carisma = int(carisma)
        except Exception:
            nivel = 1
            carisma = 0
        self.em_total_max = max(0, 2 * nivel + carisma)
        if self.em_total == 0:
            self.em_total = self.em_total_max
        else:
            self.em_total = min(self.em_total, self.em_total_max)
        self._per_punch_limit = max(0, carisma)

    def recompute_limits(self):
        if not self.owner:
            return
        self.set_owner(self.owner)

    def can_charge(self):
        if not self.owner:
            return False
        if self.em_total <= 0:
            return False
        if self.em_puño >= self._per_punch_limit:
            return False
        return True

    def cargar_punio(self):
        if not self.can_charge():
            return False
        self.em_puño += 1
        return True

    def reset_puño(self):
        self.em_puño = 0

    def available_total(self):
        return self.em_total

    def max_total(self):
        return self.em_total_max

    def golpear(self, critical=False):
        if self.em_puño <= 0:
            return 0

        em_damage = 0
        for _ in range(self.em_puño):
            em_damage += random.randint(1, 8)

        extra_blackflash = 0
        if critical and self.em_puño > 0:
            try:
                extra_blackflash = int(random.randint(1, 8) ** 2.5)
            except Exception:
                extra_blackflash = int(math.pow(random.randint(1, 8), 2.5))

        self.em_total = max(0, self.em_total - self.em_puño)
        self.em_puño = 0

        return em_damage + extra_blackflash

    def golpear_total(self, critical=False):
        base = random.randint(1, 6)
        if critical:
            base += random.randint(1, 6)
        em_part = self.golpear(critical=critical)
        return base + em_part

    def can_use_any(self):
        return self.em_total > 0 or self.em_puño > 0