# src/utils/astro/classification/exoplatnet_comparison_utils.py

from src.models.entities.exoplanet import ValueWithUncertainty
from src.models.entities.exoplanet import Exoplanet
from src.utils.formatters.article_formatters import ArticleUtils


class ExoplanetComparisonUtils:
    """
    Classe utilitaire pour les comparaisons physiques des exoplanètes
    """

    _R_JUPITER_IN_RE = 11.209
    _M_JUPITER_IN_ME = 317.8
    SIMILARITY_MARGIN = 0.2

    def __init__(self):
        self.article_utils = ArticleUtils()
        self.mercury_orbit_au = 0.387
        self.venus_orbit_au = 0.723
        self.earth_orbit_au = 1.0
        self.mars_orbit_au = 1.524
        self.jupiter_orbit_au = 5.203
        self.saturn_orbit_au = 9.582
        self.uranus_orbit_au = 19.229
        self.neptune_orbit_au = 30.103

    def describe_radius_vs_known_planets(self, exoplanet: Exoplanet) -> str:
        """
        Génère une comparaison de rayon avec Jupiter ou la Terre.
        Le rayon de l'exoplanète est supposé être en rayons joviens (R_J).
        """
        if not exoplanet.pl_radius or exoplanet.pl_radius.value is None:
            return ""

        radius_rj: float = exoplanet.pl_radius.value

        # Seuils pour Jupiter
        JUPITER_SIMILARITY_LOWER_RJ = 1.0 - self.SIMILARITY_MARGIN
        JUPITER_SIMILARITY_UPPER_RJ = 1.0 + self.SIMILARITY_MARGIN

        # Comparaison avec Jupiter
        if radius_rj >= JUPITER_SIMILARITY_LOWER_RJ:
            if radius_rj <= JUPITER_SIMILARITY_UPPER_RJ:
                return "d'un rayon environ similaire à celui de [[Jupiter (planète)|Jupiter]]"
            else:
                return f"d'un rayon environ {self.article_utils.format_number_as_french_string(radius_rj, 1)} fois celui de [[Jupiter (planète)|Jupiter]]"

        # Comparaison avec la Terre
        radius_re: float = radius_rj * self._R_JUPITER_IN_RE
        EARTH_SIMILARITY_LOWER_RE: float = 1.0 - self.SIMILARITY_MARGIN
        EARTH_SIMILARITY_UPPER_RE: float = 1.0 + self.SIMILARITY_MARGIN

        if (
            radius_re >= EARTH_SIMILARITY_LOWER_RE
            and radius_re <= EARTH_SIMILARITY_UPPER_RE
        ):
            return "d'un rayon environ similaire à celui de la [[Terre]]"
        elif radius_re > EARTH_SIMILARITY_UPPER_RE:
            return f"d'un rayon environ {self.article_utils.format_number_as_french_string(radius_re, 1)} fois celui de la [[Terre]]"
        elif radius_re > 0:
            return f"d'un rayon environ {self.article_utils.format_number_as_french_string(1 / radius_re, 1)} fois plus petit que celui de la [[Terre]]"

        return ""

    def describe_mass_vs_known_planets(self, exoplanet: Exoplanet) -> str:
        """
        Génère une comparaison de masse avec Jupiter ou la Terre.
        La masse de l'exoplanète est supposée être en masses joviennes.
        """
        if not exoplanet.pl_mass or exoplanet.pl_mass.value is None:
            return ""

        mass_mj: float = exoplanet.pl_mass.value

        # Seuils pour Jupiter
        JUPITER_SIMILARITY_LOWER_MJ: float = 1.0 - self.SIMILARITY_MARGIN
        JUPITER_SIMILARITY_UPPER_MJ: float = 1.0 + self.SIMILARITY_MARGIN

        # Comparaison avec la Terre
        mass_me: float = mass_mj * self._M_JUPITER_IN_ME
        EARTH_SIMILARITY_LOWER_ME: float = 1.0 - self.SIMILARITY_MARGIN
        EARTH_SIMILARITY_UPPER_ME: float = 1.0 + self.SIMILARITY_MARGIN

        # Comparaison avec Jupiter
        if mass_mj >= JUPITER_SIMILARITY_LOWER_MJ:
            if mass_mj <= JUPITER_SIMILARITY_UPPER_MJ:
                return "environ la même masse que [[Jupiter (planète)|Jupiter]]"
            else:
                return f"environ {self.article_utils.format_number_as_french_string(mass_mj, 1)} fois plus massif que [[Jupiter (planète)|Jupiter]]"
        elif (
            mass_me >= EARTH_SIMILARITY_LOWER_ME
            and mass_me <= EARTH_SIMILARITY_UPPER_ME
        ):
            return "environ la même masse que la [[Terre]]"
        elif mass_me > EARTH_SIMILARITY_UPPER_ME:
            return f"environ {self.article_utils.format_number_as_french_string(mass_me, 1)} fois plus massif que la [[Terre]]"
        elif mass_me > 0:
            return f"environ {self.article_utils.format_number_as_french_string(1 / mass_me, 1)} fois moins massif que la [[Terre]]"

        return ""

    def describe_orbit_vs_solar_system(self, exoplanet: Exoplanet) -> str:
        """
        Génère une comparaison de l'orbite de l'exoplanète avec les planètes du système solaire.
        La distance est supposée être en Unités Astronomiques (UA).
        """
        sma: ValueWithUncertainty | None = exoplanet.pl_semi_major_axis
        if hasattr(sma, "value"):
            sma = sma.value
        try:
            sma = float(sma)
        except (TypeError, ValueError):
            return ""  # ou une valeur par défaut

        # Maintenant, sma est bien un float pour la comparaison
        margin: float = self.SIMILARITY_MARGIN

        if sma < self.mercury_orbit_au * (1 - margin):
            return "Son orbite est significativement plus proche de son étoile que la distance orbitale de [[Mercure (planète)|Mercure]] dans notre [[système solaire]]."
        elif (
            self.mercury_orbit_au * (1 - margin)
            <= sma
            <= self.mercury_orbit_au * (1 + margin)
        ):
            return "Son orbite est comparable à celle de [[Mercure (planète)|Mercure]] dans notre [[système solaire]]."
        elif sma < self.venus_orbit_au * (1 - margin):
            return "Sa distance orbitale est comparable à la région entre [[Mercure (planète)|Mercure]] et [[Vénus (planète)|Vénus]] dans notre [[système solaire]]."
        elif (
            self.venus_orbit_au * (1 - margin)
            <= sma
            <= self.venus_orbit_au * (1 + margin)
        ):
            return "Son orbite est comparable à celle de [[Vénus (planète)|Vénus]] dans notre [[système solaire]]."
        elif sma < self.earth_orbit_au * (1 - margin):
            return "Sa distance orbitale est comparable à la région entre [[Vénus (planète)|Vénus]] et la [[Terre]] dans notre [[système solaire]]."
        elif (
            self.earth_orbit_au * (1 - margin)
            <= sma
            <= self.earth_orbit_au * (1 + margin)
        ):
            return "Son orbite est comparable à celle de la [[Terre]] dans notre [[système solaire]]."
        elif sma < self.mars_orbit_au * (1 - margin):
            return "Sa distance orbitale est comparable à la région entre la [[Terre]] et [[Mars (planète)|Mars]] dans notre [[système solaire]]."
        elif (
            self.mars_orbit_au * (1 - margin)
            <= sma
            <= self.mars_orbit_au * (1 + margin)
        ):
            return "Son orbite est comparable à celle de [[Mars (planète)|Mars]] dans notre [[système solaire]]."
        elif sma < self.jupiter_orbit_au * (1 - margin):
            # This range is where the asteroid belt is located
            return "Sa distance orbitale est comparable à la région entre [[Mars (planète)|Mars]] et [[Jupiter (planète)|Jupiter]], similaire à la [[ceinture d'astéroïdes]] dans notre [[système solaire]]."
        elif (
            self.jupiter_orbit_au * (1 - margin)
            <= sma
            <= self.jupiter_orbit_au * (1 + margin)
        ):
            return "Son orbite est comparable à celle de [[Jupiter (planète)|Jupiter]] dans notre [[système solaire]]."
        elif sma < self.saturn_orbit_au * (1 - margin):
            return "Sa distance orbitale est comparable à la région entre [[Jupiter (planète)|Jupiter]] et [[Saturne (planète)|Saturne]] dans notre [[système solaire]]."
        elif (
            self.saturn_orbit_au * (1 - margin)
            <= sma
            <= self.saturn_orbit_au * (1 + margin)
        ):
            return "Son orbite est comparable à celle de [[Saturne (planète)|Saturne]] dans notre [[système solaire]]."
        elif sma < self.uranus_orbit_au * (1 - margin):
            return "Sa distance orbitale est comparable à la région entre [[Saturne (planète)|Saturne]] et d'[[Uranus (planète)|Uranus]] dans notre [[système solaire]]."
        elif (
            self.uranus_orbit_au * (1 - margin)
            <= sma
            <= self.uranus_orbit_au * (1 + margin)
        ):
            return "Son orbite est comparable à celle d'[[Uranus (planète)|Uranus]] dans notre [[système solaire]]."
        elif sma < self.neptune_orbit_au * (1 - margin):
            return "Sa distance orbitale est comparable à la région entre d'[[Uranus (planète)|Uranus]] et de [[Neptune (planète)|Neptune]] dans notre [[système solaire]]."
        elif (
            self.neptune_orbit_au * (1 - margin)
            <= sma
            <= self.neptune_orbit_au * (1 + margin)
        ):
            return "Son orbite est comparable à celle de [[Neptune (planète)|Neptune]] dans notre [[système solaire]]."
        else:
            return "Son orbite est significativement plus éloignée de son étoile que la distance orbitale de [[Neptune (planète)|Neptune]] dans notre [[système solaire]]."
