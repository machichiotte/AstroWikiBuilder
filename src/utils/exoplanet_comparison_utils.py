from src.models.exoplanet import Exoplanet
from .format_utils import FormatUtils


class ExoplanetComparisonUtils:
    """
    Classe utilitaire pour les comparaisons physiques des exoplanètes
    """

    R_JUPITER_IN_EARTH_RADII = 11.209  # Rayon de Jupiter en rayons terrestres
    M_JUPITER_IN_EARTH_MASSES = 317.8  # Masse de Jupiter en masses terrestres
    SIMILARITY_MARGIN = 0.2  # Marge de 20%

    def __init__(self, format_utils: FormatUtils):
        self.format_utils = format_utils
        self.earth_orbit = 1.0  # 1 UA
        self.mercury_orbit = 0.387  # UA
        self.venus_orbit = 0.723  # UA
        self.mars_orbit = 1.524  # UA
        self.jupiter_orbit = 5.203  # UA

    def get_radius_comparison(self, exoplanet: Exoplanet) -> str:
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
                return f"d'un rayon environ {self.format_utils.format_numeric_value(radius_rj, 1)} fois celui de [[Jupiter (planète)|Jupiter]]"

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
            return f"d'un rayon environ {self.format_utils.format_numeric_value(radius_re, 1)} fois celui de la [[Terre]]"
        elif radius_re > 0:
            return f"d'un rayon environ {self.format_utils.format_numeric_value(1 / radius_re, 1)} fois plus petit que celui de la [[Terre]]"

        return ""

    def get_mass_comparison(self, exoplanet: Exoplanet) -> str:
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
                return f"environ {self.format_utils.format_numeric_value(mass_mj, 1)} fois plus massif que [[Jupiter (planète)|Jupiter]]"
        elif (
            mass_me >= EARTH_SIMILARITY_LOWER_ME
            and mass_me <= EARTH_SIMILARITY_UPPER_ME
        ):
            return "environ la même masse que la [[Terre]]"
        elif mass_me > EARTH_SIMILARITY_UPPER_ME:
            return f"environ {self.format_utils.format_numeric_value(mass_me, 1)} fois plus massif que la [[Terre]]"
        elif mass_me > 0:
            return f"environ {self.format_utils.format_numeric_value(1 / mass_me, 1)} fois moins massif que la [[Terre]]"

        return ""

    def get_orbital_comparison(self, exoplanet: Exoplanet) -> str:
        """
        Génère une comparaison orbitale avec le système solaire
        """
        sma = (
            exoplanet.semi_major_axis.value
            if exoplanet.semi_major_axis and exoplanet.semi_major_axis.value
            else None
        )
        if sma:
            if sma < 0.1:
                return ", une distance comparable à celle de [[Mercure (planète)|Mercure]] dans le [[système solaire]]"
            elif sma < 1:
                return ", une distance comparable à celle de [[Vénus (planète)|Vénus]] dans le [[système solaire]]"
            elif sma < 2:
                return ", une distance comparable à celle de [[Mars (planète)|Mars]] dans le [[système solaire]]"
            else:
                return ", une distance comparable à la [[ceinture d'astéroïdes]] (entre [[Mars (planète)|Mars]] et Jupiter) dans le [[système solaire]]"
        return ""

    def get_orbit_comparison(self, orbit_value: float) -> str:
        """Génère une comparaison orbitale pertinente."""
        if not orbit_value:
            return ""

        # Arrondir à 3 décimales pour éviter les comparaisons trop précises
        orbit_value = round(orbit_value, 3)

        if orbit_value < self.mercury_orbit:
            return "Son orbite est plus proche de son étoile que celle de [[Mercure (planète)|Mercure]] autour du [[Soleil]]."
        elif orbit_value < self.venus_orbit:
            return "Son orbite est similaire à celle de [[Mercure (planète)|Mercure]] autour du [[Soleil]]."
        elif orbit_value < self.earth_orbit:
            return "Son orbite est similaire à celle de [[Vénus (planète)|Vénus]] autour du [[Soleil]]."
        elif orbit_value < self.mars_orbit:
            return (
                "Son orbite est similaire à celle de la [[Terre]] autour du [[Soleil]]."
            )
        elif orbit_value < self.jupiter_orbit:
            return "Son orbite est similaire à celle de [[Mars (planète)|Mars]] autour du [[Soleil]]."
        else:
            return "Son orbite est plus éloignée de son étoile que celle de [[Jupiter (planète)|Jupiter]] autour du [[Soleil]]."
