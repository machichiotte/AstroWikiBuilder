# src/generators/articles/star/sections/rotation_activity_section.py

from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter


class RotationActivitySection:
    """Génère la section rotation et activité pour les articles d'étoiles."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, star: Star) -> str:
        """Génère la section sur la rotation et l'activité stellaire."""
        if not any([star.st_rotation, star.st_vsin, star.st_radial_velocity]):
            return ""

        content: list[str] = ["== Rotation et activité ==\n"]

        if star.st_rotation and star.st_rotation.value:
            period: str = self.article_util.format_number_as_french_string(star.st_rotation.value)
            content.append(f"L'étoile a une période de rotation d'environ {period} jours.")

        if star.st_vsin and star.st_vsin.value:
            vsin: str = self.article_util.format_number_as_french_string(star.st_vsin.value)
            content.append(f"Sa vitesse de rotation projetée (v sin i) est d'environ {vsin} km/s.")

        if star.st_radial_velocity and star.st_radial_velocity.value:
            radv: str = self.article_util.format_number_as_french_string(
                star.st_radial_velocity.value
            )
            content.append(f"La vitesse radiale systémique de l'étoile est d'environ {radv} km/s.")

        return "\n".join(content)
