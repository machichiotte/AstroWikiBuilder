# src/utils/exoplatnet_comparison_utils.py

from src.models.data_source_exoplanet import DataSourceExoplanet
from src.utils.formatters.article_utils import ArticleUtils


class ExoplanetComparisonUtils:
    """
    Classe utilitaire pour les comparaisons physiques des exoplanètes
    """

    R_JUPITER_IN_EARTH_RADII = 11.209
    M_JUPITER_IN_EARTH_MASSES = 317.8
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

    def get_radius_comparison(self, exoplanet: DataSourceExoplanet) -> str:
        """
        Génère une comparaison de rayon avec Jupiter ou la Terre.
        Le rayon de l'exoplanète est supposé être en rayons joviens (R_J).
        """
        if not exoplanet.radius or exoplanet.radius.value is None:
            return ""

        radius_rj = exoplanet.radius.value

        # Seuils pour Jupiter
        JUPITER_SIMILARITY_LOWER_RJ = 1.0 - self.SIMILARITY_MARGIN
        JUPITER_SIMILARITY_UPPER_RJ = 1.0 + self.SIMILARITY_MARGIN

        # Comparaison avec Jupiter
        if radius_rj >= JUPITER_SIMILARITY_LOWER_RJ:
            if radius_rj <= JUPITER_SIMILARITY_UPPER_RJ:
                return "d'un rayon environ similaire à celui de [[Jupiter (planète)|Jupiter]]"
            else:
                return f"d'un rayon environ {self.article_utils.format_numeric_value(radius_rj, 1)} fois celui de [[Jupiter (planète)|Jupiter]]"

        # Comparaison avec la Terre
        radius_re = radius_rj * self.R_JUPITER_IN_EARTH_RADII
        EARTH_SIMILARITY_LOWER_RE = 1.0 - self.SIMILARITY_MARGIN
        EARTH_SIMILARITY_UPPER_RE = 1.0 + self.SIMILARITY_MARGIN

        if (
            radius_re >= EARTH_SIMILARITY_LOWER_RE
            and radius_re <= EARTH_SIMILARITY_UPPER_RE
        ):
            return "d'un rayon environ similaire à celui de la [[Terre]]"
        elif radius_re > EARTH_SIMILARITY_UPPER_RE:
            return f"d'un rayon environ {self.article_utils.format_numeric_value(radius_re, 1)} fois celui de la [[Terre]]"
        elif radius_re > 0:
            return f"d'un rayon environ {self.article_utils.format_numeric_value(1 / radius_re, 1)} fois plus petit que celui de la [[Terre]]"

        return ""

    def get_mass_comparison(self, exoplanet: DataSourceExoplanet) -> str:
        """
        Génère une comparaison de masse avec Jupiter ou la Terre.
        La masse de l'exoplanète est supposée être en masses joviennes.
        """
        if not exoplanet.mass or exoplanet.mass.value is None:
            return ""

        mass_mj = exoplanet.mass.value

        # Seuils pour Jupiter
        JUPITER_SIMILARITY_LOWER_MJ = 1.0 - self.SIMILARITY_MARGIN
        JUPITER_SIMILARITY_UPPER_MJ = 1.0 + self.SIMILARITY_MARGIN

        # Comparaison avec la Terre
        mass_me = mass_mj * self.M_JUPITER_IN_EARTH_MASSES
        EARTH_SIMILARITY_LOWER_ME = 1.0 - self.SIMILARITY_MARGIN
        EARTH_SIMILARITY_UPPER_ME = 1.0 + self.SIMILARITY_MARGIN

        # Comparaison avec Jupiter
        if mass_mj >= JUPITER_SIMILARITY_LOWER_MJ:
            if mass_mj <= JUPITER_SIMILARITY_UPPER_MJ:
                return "environ la même masse que [[Jupiter (planète)|Jupiter]]"
            else:
                return f"environ {self.article_utils.format_numeric_value(mass_mj, 1)} fois plus massif que [[Jupiter (planète)|Jupiter]]"
        elif (
            mass_me >= EARTH_SIMILARITY_LOWER_ME
            and mass_me <= EARTH_SIMILARITY_UPPER_ME
        ):
            return "environ la même masse que la [[Terre]]"
        elif mass_me > EARTH_SIMILARITY_UPPER_ME:
            return f"environ {self.article_utils.format_numeric_value(mass_me, 1)} fois plus massif que la [[Terre]]"
        elif mass_me > 0:
            return f"environ {self.article_utils.format_numeric_value(1 / mass_me, 1)} fois moins massif que la [[Terre]]"

        return ""

    def get_orbital_comparison(self, exoplanet: DataSourceExoplanet) -> str:
        """
        Génère une comparaison de l'orbite de l'exoplanète avec les planètes du système solaire.
        La distance est supposée être en Unités Astronomiques (UA).
        """
        sma = (
            exoplanet.semi_major_axis.value
            if exoplanet.semi_major_axis and exoplanet.semi_major_axis.value is not None
            else None
        )

        if sma is None:
            return ""

        # Use a margin for "similar to" comparisons
        margin = self.SIMILARITY_MARGIN

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
