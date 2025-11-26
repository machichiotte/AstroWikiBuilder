# src/generators/articles/star/sections/astrometry_section.py

from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter


class AstrometrySection:
    """Génère la section astrométrie pour les articles d'étoiles."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, star: Star) -> str:
        """Génère la section astrométrie."""
        if not self._has_astrometry_data(star):
            return ""

        section = "== Astrométrie ==\n\n"
        section += self._generate_proper_motion(star)
        section += self._generate_total_proper_motion(star)
        section += self._generate_parallax_distance(star)
        section += self._generate_galactic_coordinates(star)
        section += self._generate_ecliptic_coordinates(star)

        return section

    def _has_astrometry_data(self, star: Star) -> bool:
        """Vérifie si des données astrométriques sont disponibles."""
        return any(
            [
                star.st_proper_motion_ra,
                star.st_proper_motion_dec,
                star.st_parallax,
                star.st_distance,
                star.glon,
                star.glat,
                star.sy_pm,
                star.elon,
                star.elat,
            ]
        )

    def _generate_proper_motion(self, star: Star) -> str:
        """Génère les informations sur le mouvement propre."""
        content = ""

        if star.st_proper_motion_ra and star.st_proper_motion_ra.value is not None:
            pm_ra_str = self.article_util.format_number_as_french_string(
                star.st_proper_motion_ra.value
            )
            content += f"Le mouvement propre en ascension droite est de {pm_ra_str} [[Seconde d'arc|mas]]/an.\n"

        if star.st_proper_motion_dec and star.st_proper_motion_dec.value is not None:
            pm_dec_str = self.article_util.format_number_as_french_string(
                star.st_proper_motion_dec.value
            )
            content += f"Le mouvement propre en déclinaison est de {pm_dec_str} mas/an.\n"

        return content

    def _generate_parallax_distance(self, star: Star) -> str:
        """Génère les informations sur la parallaxe et la distance."""
        content = ""

        if star.st_parallax and star.st_parallax.value is not None:
            parallax_str = self.article_util.format_number_as_french_string(star.st_parallax.value)
            content += f"\nLa [[parallaxe]] de l'étoile est de {parallax_str} mas.\n"

        if star.st_distance and star.st_distance.value is not None:
            distance_str = self.article_util.format_number_as_french_string(star.st_distance.value)
            content += f"La distance à l'étoile est d'environ {distance_str} [[parsec|pc]].\n"

        return content

    def _generate_galactic_coordinates(self, star: Star) -> str:
        """Génère les informations sur les coordonnées galactiques."""
        content = ""

        if star.glon and star.glon.value is not None:
            glon_str = self.article_util.format_number_as_french_string(star.glon.value)
            content += f"\nLa longitude galactique est de {glon_str}°.\n"

        if star.glat and star.glat.value is not None:
            glat_str = self.article_util.format_number_as_french_string(star.glat.value)
            content += f"La latitude galactique est de {glat_str}°.\n"

        return content

    def _generate_total_proper_motion(self, star: Star) -> str:
        """Génère les informations sur le mouvement propre total."""
        content = ""

        if star.sy_pm and star.sy_pm.value is not None:
            pm_str = self.article_util.format_number_as_french_string(star.sy_pm.value)
            content += f"\nLe mouvement propre total est de {pm_str} mas/an.\n"

        return content

    def _generate_ecliptic_coordinates(self, star: Star) -> str:
        """Génère les informations sur les coordonnées écliptiques."""
        content = ""

        if star.elon and star.elon.value is not None:
            elon_str = self.article_util.format_number_as_french_string(star.elon.value)
            content += f"\nLa longitude écliptique est de {elon_str}°.\n"

        if star.elat and star.elat.value is not None:
            elat_str = self.article_util.format_number_as_french_string(star.elat.value)
            content += f"La latitude écliptique est de {elat_str}°.\n"

        return content
