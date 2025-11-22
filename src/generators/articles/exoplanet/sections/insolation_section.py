# src/generators/articles/exoplanet/sections/insolation_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class InsolationSection:
    """Génère la section flux d'insolation pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur le flux d'insolation reçu par rapport à la Terre."""
        if not exoplanet.pl_insolation_flux or not exoplanet.pl_insolation_flux.value:
            return ""
        try:
            flux_value = float(exoplanet.pl_insolation_flux.value)
        except (ValueError, TypeError):
            return ""
        section = "== Flux d'insolation ==\n"
        flux_str = self.article_util.format_uncertain_value_for_article(
            exoplanet.pl_insolation_flux
        )
        if flux_value < 0.1:
            section += f"La planète reçoit environ {flux_str} fois le flux lumineux que la [[Terre]] reçoit du [[Soleil]], ce qui la place dans une zone très froide et sombre, similaire aux planètes externes du système solaire comme [[Jupiter (planète)|Jupiter]] ou [[Saturne (planète)|Saturne]].\n"
        elif flux_value < 0.4:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil, soit un niveau d'insolation inférieur à celui de [[Mars (planète)|Mars]]. Elle se trouve dans la zone externe du système planétaire.\n"
        elif flux_value < 0.8:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil, la plaçant dans la limite externe de la [[zone habitable]], où l'eau liquide pourrait théoriquement exister avec une atmosphère à effet de serre appropriée.\n"
        elif flux_value < 1.3:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil, soit un niveau d'insolation relativement comparable. Ces conditions sont favorables au maintien d'eau liquide en surface.\n"
        elif flux_value < 1.9:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil, la plaçant dans la limite interne de la zone habitable, proche des conditions de [[Vénus (planète)|Vénus]]. Le risque d'un effet de serre incontrôlé est élevé.\n"
        elif flux_value < 4:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil. Ce flux élevé indique une proximité importante avec son étoile hôte, susceptible d'entraîner une température de surface très élevée et l'évaporation de toute eau liquide.\n"
        else:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil. Ce flux extrêmement élevé, supérieur à celui de [[Mercure (planète)|Mercure]], indique une très grande proximité avec son étoile hôte. De telles conditions entraînent des températures de surface extrêmes et peuvent provoquer l'évaporation massive de l'atmosphère.\n"
        return section
