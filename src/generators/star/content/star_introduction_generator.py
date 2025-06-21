# src/generators/star/star_introduction_generator.py

from typing import Optional
from src.models.entities.star import Star
from src.utils.astro.classification.star_type_utils import StarTypeUtils
from src.utils.lang.phrase.constellation import phrase_situee_dans_constellation
from src.utils.formatters.article_formatters import ArticleUtils


class StarIntroductionGenerator:
    """
    Générateur de l’introduction encyclopédique pour les articles d’étoiles.
    """

    def __init__(self):
        self.star_type_utils = StarTypeUtils()
        self.article_utils = ArticleUtils()

    # ============================================================================
    # COMPOSITION DES SEGMENTS DE PHRASE
    # ============================================================================
    def _compose_star_type_phrase(self, star: Star) -> Optional[str]:
        """
        Renvoie une description textuelle du type spectral de l'étoile.
        """
        if not star.st_spectral_type:
            return None

        star_types = self.star_type_utils.determine_star_types_from_properties(star)
        if not star_types:
            return None

        description = star_types[0].strip().lower()
        return f"une [[{description}]]"

    def _compose_constellation_phrase(self, star: Star) -> Optional[str]:
        """
        Renvoie une phrase indiquant la position dans la constellation.
        """
        if not star.sy_constellation:
            return None
        constellation = star.sy_constellation.strip()
        return phrase_situee_dans_constellation(constellation, with_bracket=True)

    def _compose_distance_phrase(self, star: Star) -> Optional[str]:
        """
        Renvoie une phrase exprimant la distance à la Terre en parsecs.
        """
        if not star.st_distance or not star.st_distance.value:
            return None

        try:
            distance = float(star.st_distance.value)
            return f"à environ {{{{unité|{distance:.2f}|[[parsec]]s}}}} de la [[Terre]]"
        except (ValueError, TypeError):
            return None

    # ============================================================================
    # GÉNÉRATION DE L'INTRODUCTION
    # ============================================================================
    def compose_star_introduction(self, star: Star) -> str:
        """
        Génère l'introduction encyclopédique enrichie de l'article de l'étoile.
        """
        star_name: str = star.st_name if star.st_name else "Cette étoile"

        intro = f"'''{star_name}''' est"

        spectral_phrase = self._compose_star_type_phrase(star)
        if spectral_phrase:
            intro += f" {spectral_phrase}"
        else:
            intro += " une étoile"

        constellation_phrase = self._compose_constellation_phrase(star)
        if constellation_phrase:
            intro += f" {constellation_phrase}"

        distance_phrase = self._compose_distance_phrase(star)
        if distance_phrase:
            intro += f", {distance_phrase}"

        return intro + "."
