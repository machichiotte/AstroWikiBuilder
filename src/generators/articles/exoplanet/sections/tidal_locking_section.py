# src/generators/articles/exoplanet/sections/tidal_locking_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class TidalLockingSection:
    """Génère la section verrouillage gravitationnel pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur le verrouil lage gravitationnel potentiel."""
        if not exoplanet.pl_orbital_period or not exoplanet.pl_orbital_period.value:
            return ""
        try:
            period_value = float(exoplanet.pl_orbital_period.value)
        except (ValueError, TypeError):
            return ""
        eccentricity_value = 0.0
        if exoplanet.pl_eccentricity and exoplanet.pl_eccentricity.value:
            try:
                eccentricity_value = float(exoplanet.pl_eccentricity.value)
            except (ValueError, TypeError):
                pass
        is_likely_locked = period_value < 15 and eccentricity_value < 0.1
        if not is_likely_locked:
            return ""
        section = "== Rotation et verrouillage gravitationnel ==\n"
        section += "En raison de sa proximité avec son étoile hôte, il est très probable que cette exoplanète subisse un [[verrouillage gravitationnel|verrouillage par effet de marée]].\n"
        return section
