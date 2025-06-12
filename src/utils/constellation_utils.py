# src/utils/constellation_utils.py
from src.constants.field_mappings import CONSTELLATION_FR
from src.utils.formatters.article_formatters import ArticleUtils

from astropy.coordinates import SkyCoord
import astropy.units as u


class ConstellationUtils:
    """
    Classe utilitaire pour décrire et caractériser les étoiles hôtes des exoplanètes,
    avec descriptions et liens Wikipedia en français vers le type d'astre correspondant.
    """

    def __init__(self):
        self.article_utils = ArticleUtils()

    def get_constellation_name(self, right_ascension, declination) -> str:
        """Trouve la constellation"""
        right_ascension = right_ascension.replace("/", " ")
        declination = declination.replace("/", " ")

        coord = SkyCoord(
            ra=right_ascension, dec=declination, unit=(u.hourangle, u.deg), frame="icrs"
        )
        constellation_en = coord.get_constellation()

        return CONSTELLATION_FR.get(constellation_en, constellation_en)

    def get_constellation_UAI(self, st_constallation) -> str:
        """
        Génère le lien formaté pour la constellation de l'étoile hôte.
        Ex: [[Cygne (constellation)|Cygne]]
        """

        if st_constallation and st_constallation != "son étoile hôte":
            return f"[[{st_constallation} (constellation)|{st_constallation}]]"
        return ""
