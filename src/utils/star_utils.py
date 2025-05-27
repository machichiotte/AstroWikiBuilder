# src/utils/star_utils.py
from src.constants.field_mappings import CONSTELLATION_FR, SPECTRAL_TYPE_DESCRIPTIONS
from src.models.exoplanet import Exoplanet
from .format_utils import FormatUtils

from astropy.coordinates import SkyCoord
import astropy.units as u


class StarUtils:
    """
    Classe utilitaire pour décrire et caractériser les étoiles hôtes des exoplanètes,
    avec descriptions et liens Wikipedia en français vers le type d'astre correspondant.
    """

    def __init__(self, format_utils: FormatUtils):
        self.format_utils = format_utils

    def get_exoplanet_spectral_type_formatted_description(
        self, spectral_type: str
    ) -> str:
        """Génère une description de l'étoile avec le type spectral."""
        if not spectral_type:
            return "son étoile hôte"

        spectral_class = spectral_type[0].upper()
        description = SPECTRAL_TYPE_DESCRIPTIONS.get(spectral_class, "son étoile hôte")

        return f"[[{description}]]"

    def get_exoplanet_constellation(self, exoplanet: Exoplanet) -> str:
        """Trouve la constellation"""
        right_ascension = exoplanet.right_ascension.value.replace("/", " ")
        declination = exoplanet.declination.value.replace("/", " ")

        coord = SkyCoord(
            ra=right_ascension, dec=declination, unit=(u.hourangle, u.deg), frame="icrs"
        )
        constellation_en = coord.get_constellation()

        return CONSTELLATION_FR.get(constellation_en, constellation_en)

    def get_exoplanet_constellation_formatted(self, exoplanet: Exoplanet) -> str:
        """
        Génère le lien formaté pour la constellation de l'étoile hôte.
        Ex: [[Cygne (constellation)|Cygne]]
        This method now internally calls get_constellation to determine the name.
        """
        # Use the astropy-based get_constellation to get the French constellation name
        constellation_name = self.get_exoplanet_constellation(
            exoplanet
        )  # This calls the user's new method

        if (
            constellation_name and constellation_name != "son étoile hôte"
        ):  # Check if a valid constellation was found
            # Assuming the French Wikipedia convention for constellations is "Name (constellation)"
            return f"[[{constellation_name} (constellation)|{constellation_name}]]"
        return ""  # Return empty string if no constellation or if it's the default "son étoile hôte"
