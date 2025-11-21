# src/utils/astro/constellation_util.py
import astropy.units as u
from astropy.coordinates import SkyCoord
from src.utils.formatters.article_formatter import ArticleFormatter

from src.constants.wikipedia_field_config import WIKIPEDIA_CONSTELLATION_ENG_TO_FR


class ConstellationUtil:
    """
    Classe utilitaire pour décrire et caractériser les étoiles hôtes des exoplanètes,
    avec descriptions et liens Wikipedia en français vers le type d'astre correspondant.
    """

    def __init__(self):
        self.article_util = ArticleFormatter()

    def get_constellation_name(self, right_ascension, declination) -> str:
        """Trouve la constellation"""
        right_ascension = right_ascension.replace("/", " ")
        declination = declination.replace("/", " ")

        coord = SkyCoord(
            ra=right_ascension, dec=declination, unit=(u.hourangle, u.deg), frame="icrs"
        )
        constellation_en = coord.get_constellation()

        return WIKIPEDIA_CONSTELLATION_ENG_TO_FR.get(constellation_en, constellation_en)
