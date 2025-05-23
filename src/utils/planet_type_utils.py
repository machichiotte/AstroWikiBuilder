# src/utils/planet_type_utils.py
from typing import Optional
from src.models.exoplanet import Exoplanet

class PlanetTypeUtils:
    """
    Utilitaire pour classifier les exoplanètes selon les définitions Wikipédia (en français).
    """
    # Seuils de masse (en masses terrestres)
    SUB_EARTH_MAX = 0.5
    EARTH_MAX = 2.0
    SUPER_EARTH_MAX = 10.0
    ICE_GIANT_MAX = 30.0
    GAS_GIANT_MIN = 10.0
    JUPITER_MASS = 317.8  # 1 M_J

    # Seuils de rayon (en rayons terrestres)
    SUB_EARTH_RADIUS_MAX = 0.8
    EARTH_RADIUS_MAX = 1.25
    SUPER_PUFF_RADIUS_MIN = 4.0

    # Seuils de température (en K)
    ULTRA_HOT_MIN = 2200
    HOT_MIN = 1000
    WARM_MIN = 500

    def get_planet_type(self, p: Exoplanet) -> str:
        """Renvoie le type de planète en français."""
        m = self._mass_in_earth(p)
        r = self._radius_in_earth(p)
        a = p.semi_major_axis.value if p.semi_major_axis and p.semi_major_axis.value else None
        t = p.temperature.value if p.temperature and p.temperature.value else None

        # Planète super-enflée
        if r and m and r >= self.SUPER_PUFF_RADIUS_MIN and m <= self.SUPER_EARTH_MAX:
            return "Super-enflée"

        # Géantes (Jupiter, Neptune, Saturne)
        if m and m >= self.GAS_GIANT_MIN:
            return self._classify_giant(m, t, a)

        # Telluriques (Sous-Terre, Terre, Super-Terre, Méga-Terre)
        return self._classify_terrestrial(m, r)

    def _classify_giant(self, m: float, t: Optional[float], a: Optional[float]) -> str:
        # Jupiter et plus
        if m >= self.JUPITER_MASS:
            if t:
                if t >= self.ULTRA_HOT_MIN:
                    return "Jupiter ultra-chaud"
                if t >= self.HOT_MIN:
                    return "Jupiter chaud"
                if t >= self.WARM_MIN:
                    return "Jupiter tiède"
            # froid si éloigné ou sans température
            if a and a >= 1.0:
                return "Jupiter froid"
            return "Jupiter"

        # Géantes de glaces (type Neptune)
        if m <= self.ICE_GIANT_MAX:
            if a is not None:
                if a < 1.0:
                    return "Neptune chaude"
                if a >= 1.0:
                    return "Neptune froide"
            if t:
                if t >= self.HOT_MIN:
                    return "Neptune chaude"
                if t >= self.WARM_MIN:
                    return "Neptune tiède"
            return "Neptune"

        # Pour les masses intermédiaires entre Neptune et Jupiter
        if t:
            if t >= self.HOT_MIN:
                return "Jupiter chaud"
            if t >= self.WARM_MIN:
                return "Jupiter tiède"
        if a and a >= 1.0:
            return "Jupiter froid"
        return "Jupiter"

    def _classify_terrestrial(self, m: Optional[float], r: Optional[float]) -> str:
        if m and m <= self.SUB_EARTH_MAX or r and r <= self.SUB_EARTH_RADIUS_MAX:
            return "Sous-Terre"
        if m and m <= self.EARTH_MAX and r and r <= self.EARTH_RADIUS_MAX:
            return "Planète de dimensions terrestres"
        if m and m <= self.SUPER_EARTH_MAX:
            return "Super-Terre"
        return "Méga-Terre"

    def _mass_in_earth(self, p: Exoplanet) -> Optional[float]:
        if not p.mass or not p.mass.value:
            return None
        m = p.mass.value
        if p.mass.unit == "M_J":
            m *= self.JUPITER_MASS
        return m

    def _radius_in_earth(self, p: Exoplanet) -> Optional[float]:
        if not p.radius or not p.radius.value:
            return None
        r = p.radius.value
        if p.radius.unit == "R_J":
            r *= 11.2
        return r