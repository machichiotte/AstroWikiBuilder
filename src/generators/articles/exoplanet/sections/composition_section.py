# src/generators/articles/exoplanet/sections/composition_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class CompositionSection:
    """Génère la section composition pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur la composition basée sur la densité."""
        if not exoplanet.pl_density or not exoplanet.pl_density.value:
            return ""
        try:
            density_value = float(exoplanet.pl_density.value)
        except (ValueError, TypeError):
            return ""
        section = "== Composition ==\n"
        density_str = self.article_util.format_uncertain_value_for_article(exoplanet.pl_density)
        if density_value > 5.0:
            section += f"Avec une densité de {density_str} g/cm³, cette exoplanète présente une composition probablement [[Planète tellurique|tellurique]].\n"
        elif density_value > 3.0:
            section += f"Avec une densité de {density_str} g/cm³, cette exoplanète pourrait avoir une composition [[Planète tellurique|tellurique]].\n"
        elif density_value > 2.0:
            section += f"Avec une densité de {density_str} g/cm³, cette exoplanète pourrait être une [[mini-Neptune]].\n"
        else:
            section += f"Avec une faible densité de {density_str} g/cm³, cette exoplanète est probablement une [[géante gazeuse]].\n"
        return section
