# src/generators/articles/star/sections/astrometry_section.py

from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter


class AstrometrySection:
    """Génère la section astrométrie pour les articles d'étoiles."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, star: Star) -> str:
        """Génère la section astrométrie."""
        if not any(
            [
                star.st_proper_motion_ra,
                star.st_proper_motion_dec,
                star.st_parallax,
                star.st_distance,
                star.glon,
                star.glat,
            ]
        ):
            return ""

        section = "== Astrométrie ==\n\n"

        # Mouvement propre
        if star.st_proper_motion_ra and star.st_proper_motion_ra.value is not None:
            pm_ra_str = self.article_util.format_number_as_french_string(
                star.st_proper_motion_ra.value
            )
            section += f"Le mouvement propre en ascension droite est de {pm_ra_str} [[Seconde d'arc|mas]]/an.\n"

        if star.st_proper_motion_dec and star.st_proper_motion_dec.value is not None:
            pm_dec_str = self.article_util.format_number_as_french_string(
                star.st_proper_motion_dec.value
            )
            section += f"Le mouvement propre en déclinaison est de {pm_dec_str} mas/an.\n"

        # Parallaxe et distance
        if star.st_parallax and star.st_parallax.value is not None:
            parallax_str = self.article_util.format_number_as_french_string(star.st_parallax.value)
            section += f"\nLa [[parallaxe]] de l'étoile est de {parallax_str} mas.\n"

        if star.st_distance and star.st_distance.value is not None:
            distance_str = self.article_util.format_number_as_french_string(star.st_distance.value)
            section += f"La distance à l'étoile est d'environ {distance_str} [[parsec|pc]].\n"

        # Coordonnées galactiques
        if star.glon and star.glon.value is not None:
            glon_str = self.article_util.format_number_as_french_string(star.glon.value)
            section += f"\nLa longitude galactique est de {glon_str}°.\n"

        if star.glat and star.glat.value is not None:
            glat_str = self.article_util.format_number_as_french_string(star.glat.value)
            section += f"La latitude galactique est de {glat_str}°.\n"

        return section
