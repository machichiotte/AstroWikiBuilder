# src/generators/articles/star/sections/introduction_section.py

from src.models.entities.star_entity import Star
from src.utils.astro.classification.star_type_util import StarTypeUtil
from src.utils.formatters.article_formatter import ArticleFormatter
from src.utils.lang.phrase.constellation import phrase_situee_dans_constellation


class IntroductionSection:
    """Générateur de l’introduction encyclopédique pour les articles d’étoiles."""

    def __init__(self):
        self.star_type_util = StarTypeUtil()
        self.article_util = ArticleFormatter()

    def _compose_star_type_phrase(self, star: Star) -> str | None:
        """Renvoie une description textuelle du type spectral de l'étoile."""
        if not star.st_spectral_type:
            return None

        star_types = self.star_type_util.determine_star_types_from_properties(star)
        if not star_types:
            return None

        description = star_types[0].strip()
        description2 = description[0].lower() + description[1:]
        return f"une [[{description2}]]"

    def _compose_constellation_phrase(self, star: Star) -> str | None:
        """Renvoie une phrase indiquant la position dans la constellation."""
        if not star.sy_constellation:
            return None
        constellation = star.sy_constellation.strip()
        return phrase_situee_dans_constellation(constellation, with_bracket=True)

    def _compose_distance_phrase(self, star: Star) -> str | None:
        """Renvoie une phrase exprimant la distance à la Terre en parsecs."""
        if not star.st_distance or not star.st_distance.value:
            return None

        try:
            distance = float(star.st_distance.value)
            return f"à environ {{{{unité|{distance:.2f}|[[parsec]]s}}}} de la [[Terre]]"
        except (ValueError, TypeError):
            return None

    def compose_star_introduction(self, star: Star) -> str:
        """Génère l'introduction encyclopédique enrichie de l'article de l'étoile."""
        star_name: str = star.st_name if star.st_name else "Cette étoile"

        intro = f"'''{star_name}''' est"

        # Détermination de la nature du système (binaire, triple, etc.)
        is_multiple = False
        if star.sy_star_count and star.sy_star_count > 1:
            is_multiple = True
            if star.sy_star_count == 2:
                intro += " une [[étoile binaire]]"
            elif star.sy_star_count == 3:
                intro += " un [[système triple (astronomie)|système triple]]"
            else:
                intro += f" un [[système stellaire]] composé de {star.sy_star_count} étoiles"

        spectral_phrase = self._compose_star_type_phrase(star)

        if is_multiple:
            if spectral_phrase:
                intro += f" dont la composante principale est {spectral_phrase}"
        else:
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
