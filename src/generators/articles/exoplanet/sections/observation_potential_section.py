# src/generators/articles/exoplanet/sections/observation_potential_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class ObservationPotentialSection:
    """Génère la section potentiel d'observation pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur le potentiel d'observation pour la spectroscopie."""
        if not exoplanet.st_apparent_magnitude:
            return ""
        try:
            if hasattr(exoplanet.st_apparent_magnitude, "value"):
                mag_value = float(exoplanet.st_apparent_magnitude.value)
            else:
                mag_value = float(exoplanet.st_apparent_magnitude)
        except (ValueError, TypeError, AttributeError):
            return ""
        if mag_value > 12:
            return ""
        section = "== Potentiel d'observation ==\n"
        is_transiting = exoplanet.disc_method and "Transit" in str(exoplanet.disc_method)
        has_transit_depth = exoplanet.pl_transit_depth and exoplanet.pl_transit_depth.value
        if is_transiting and has_transit_depth and mag_value < 10:
            section += f"Grâce à la brillance de son étoile hôte (magnitude apparente de {mag_value:.1f}) et à sa méthode de détection par transit, cette exoplanète constitue une cible prometteuse pour la caractérisation atmosphérique par [[spectroscopie de transmission]]. De telles observations peuvent révéler la composition chimique de son atmosphère, notamment avec des instruments comme ceux du [[Télescope spatial James-Webb|JWST]].\n"
        elif mag_value < 10:
            section += f"Son étoile hôte possède une magnitude apparente de {mag_value:.1f}, ce qui en fait une cible relativement brillante accessible aux télescopes modernes pour des observations photométriques ou spectroscopiques.\n"
        elif mag_value < 12:
            section += f"Avec une magnitude apparente de {mag_value:.1f}, l'étoile hôte est observable avec des télescopes de taille moyenne, permettant des études de suivi.\n"
        return section
