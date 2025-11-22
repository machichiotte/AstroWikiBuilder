# src/generators/articles/exoplanet/sections/system_architecture_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class SystemArchitectureSection:
    """Génère la section architecture du système pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur l'architecture du système planétaire."""
        if not exoplanet.sy_planet_count:
            return ""
        try:
            if hasattr(exoplanet.sy_planet_count, "value"):
                planet_count = int(exoplanet.sy_planet_count.value)
            else:
                planet_count = int(exoplanet.sy_planet_count)
        except (ValueError, TypeError, AttributeError):
            return ""
        if planet_count <= 1:
            return ""
        section = "== Architecture du système ==\n"
        if planet_count == 2:
            section += f"Cette planète fait partie d'un système binaire planétaire orbitant autour de [[{exoplanet.st_name}]]. L'existence de multiples planètes dans un même système permet d'étudier la formation et l'évolution planétaire de manière comparative.\n"
        elif planet_count >= 3 and planet_count <= 5:
            section += f"Cette planète fait partie d'un système de {planet_count} planètes connues orbitant autour de [[{exoplanet.st_name}]]. L'étude de systèmes multi-planétaires fournit des informations précieuses sur les mécanismes de formation et de migration planétaire.\n"
        else:
            section += f"Cette planète fait partie d'un système planétaire remarquable contenant {planet_count} planètes connues autour de [[{exoplanet.st_name}]]. Un tel système dense offre une opportunité unique d'étudier les interactions gravitationnelles entre planètes et la stabilité dynamique à long terme.\n"
        return section
