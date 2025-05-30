# src/utils/star_utils.py
from src.constants.field_mappings import CONSTELLATION_FR
from src.utils.formatting.format_utils import FormatUtils

from astropy.coordinates import SkyCoord
import astropy.units as u


class StarUtils:
    """
    Classe utilitaire pour décrire et caractériser les étoiles hôtes des exoplanètes,
    avec descriptions et liens Wikipedia en français vers le type d'astre correspondant.
    """

    def __init__(self, format_utils: FormatUtils):
        self.format_utils = format_utils

    def get_constellation_name(self, right_ascension, declination) -> str:
        """Trouve la constellation"""
        right_ascension = right_ascension.replace("/", " ")
        declination = declination.replace("/", " ")

        coord = SkyCoord(
            ra=right_ascension, dec=declination, unit=(u.hourangle, u.deg), frame="icrs"
        )
        constellation_en = coord.get_constellation()

        return CONSTELLATION_FR.get(constellation_en, constellation_en)

    def get_constellation_UAI(self, right_ascension, declination) -> str:
        """
        Génère le lien formaté pour la constellation de l'étoile hôte.
        Ex: [[Cygne (constellation)|Cygne]]
        """
        constellation_name = self.get_constellation_name(right_ascension, declination)

        if constellation_name and constellation_name != "son étoile hôte":
            return f"[[{constellation_name} (constellation)|{constellation_name}]]"
        return ""
