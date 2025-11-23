# src/generators/articles/exoplanet/sections/orbit_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class OrbitSection:
    """Génère la section orbite pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur l'orbite."""
        if not any(
            [
                exoplanet.pl_semi_major_axis,
                exoplanet.pl_eccentricity,
                exoplanet.pl_orbital_period,
                exoplanet.pl_inclination,
            ]
        ):
            return ""

        content: list[str] = ["== Orbite ==\n"]

        if exoplanet.pl_semi_major_axis:
            semi_major_axis_str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_semi_major_axis
            )
            if semi_major_axis_str:
                content.append(
                    f"L'exoplanète orbite à une distance de {semi_major_axis_str} [[unité astronomique|UA]] de son étoile."
                )

        if exoplanet.pl_eccentricity:
            eccentricity_str: str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_eccentricity
            )
            if eccentricity_str:
                content.append(f"L'orbite a une excentricité de {eccentricity_str}.")

        if exoplanet.pl_orbital_period:
            period_str: str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_orbital_period
            )
            if period_str:
                content.append(f"La période orbitale est de {period_str} [[jour|jours]].")

        if exoplanet.pl_inclination:
            inclination_str: str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_inclination
            )
            if inclination_str:
                content.append(
                    f"L'inclinaison de l'orbite est de {inclination_str} [[degré (angle)|degrés]]."
                )

        return "\n".join(content)
