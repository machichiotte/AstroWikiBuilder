# src/utils/astro/constellation_utils.py
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
