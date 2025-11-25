# src/generators/articles/exoplanet/sections/orbit_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class OrbitSection:
    """Génère la section orbite pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur l'orbite."""
        if not self._has_orbital_data(exoplanet):
            return ""

        content: list[str] = ["== Orbite ==\n"]

        self._add_semi_major_axis(exoplanet, content)
        self._add_eccentricity(exoplanet, content)
        self._add_orbital_period(exoplanet, content)
        self._add_inclination(exoplanet, content)
        self._add_obliquity(exoplanet, content)
        self._add_impact_parameter(exoplanet, content)
        self._add_geometric_ratios(exoplanet, content)

        return "\n".join(content)

    def _has_orbital_data(self, exoplanet: Exoplanet) -> bool:
        """Vérifie si des données orbitales sont disponibles."""
        return any(
            [
                exoplanet.pl_semi_major_axis,
                exoplanet.pl_eccentricity,
                exoplanet.pl_orbital_period,
                exoplanet.pl_inclination,
                exoplanet.pl_projobliq,
                exoplanet.pl_trueobliq,
                exoplanet.pl_imppar,
                exoplanet.pl_ratdor,
                exoplanet.pl_ratror,
            ]
        )

    def _add_semi_major_axis(self, exoplanet: Exoplanet, content: list[str]) -> None:
        """Ajoute le demi-grand axe."""
        if exoplanet.pl_semi_major_axis:
            value_str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_semi_major_axis
            )
            if value_str:
                content.append(
                    f"L'exoplanète orbite à une distance de {value_str} [[unité astronomique|UA]] de son étoile."
                )

    def _add_eccentricity(self, exoplanet: Exoplanet, content: list[str]) -> None:
        """Ajoute l'excentricité."""
        if exoplanet.pl_eccentricity:
            value_str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_eccentricity
            )
            if value_str:
                content.append(f"L'orbite a une excentricité de {value_str}.")

    def _add_orbital_period(self, exoplanet: Exoplanet, content: list[str]) -> None:
        """Ajoute la période orbitale."""
        if exoplanet.pl_orbital_period:
            value_str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_orbital_period
            )
            if value_str:
                content.append(f"La période orbitale est de {value_str} [[jour|jours]].")

    def _add_inclination(self, exoplanet: Exoplanet, content: list[str]) -> None:
        """Ajoute l'inclinaison."""
        if exoplanet.pl_inclination:
            value_str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_inclination
            )
            if value_str:
                content.append(
                    f"L'inclinaison de l'orbite est de {value_str} [[degré (angle)|degrés]]."
                )

    def _add_obliquity(self, exoplanet: Exoplanet, content: list[str]) -> None:
        """Ajoute les obliquités."""
        if exoplanet.pl_projobliq:
            value_str = self.article_util.format_uncertain_value_for_article(exoplanet.pl_projobliq)
            if value_str:
                content.append(f"L'obliquité projetée est de {value_str} degrés.")

        if exoplanet.pl_trueobliq:
            value_str = self.article_util.format_uncertain_value_for_article(exoplanet.pl_trueobliq)
            if value_str:
                content.append(f"L'obliquité vraie est de {value_str} degrés.")

    def _add_impact_parameter(self, exoplanet: Exoplanet, content: list[str]) -> None:
        """Ajoute le paramètre d'impact."""
        if exoplanet.pl_imppar:
            value_str = self.article_util.format_uncertain_value_for_article(exoplanet.pl_imppar)
            if value_str:
                content.append(f"Le paramètre d'impact du transit est de {value_str}.")

    def _add_geometric_ratios(self, exoplanet: Exoplanet, content: list[str]) -> None:
        """Ajoute les rapports géométriques."""
        if exoplanet.pl_ratdor:
            value_str = self.article_util.format_uncertain_value_for_article(exoplanet.pl_ratdor)
            if value_str:
                content.append(
                    f"Le rapport entre la distance orbitale et le rayon stellaire (a/R*) est de {value_str}."
                )

        if exoplanet.pl_ratror:
            value_str = self.article_util.format_uncertain_value_for_article(exoplanet.pl_ratror)
            if value_str:
                content.append(
                    f"Le rapport entre le rayon planétaire et le rayon stellaire (Rp/R*) est de {value_str}."
                )
