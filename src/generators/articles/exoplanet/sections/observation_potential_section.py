# src/generators/articles/exoplanet/sections/observation_potential_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class ObservationPotentialSection:
    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        magnitude = self._extract_apparent_magnitude(exoplanet)

        # Seuil max de pertinence (ex: au-delà de 12, difficile pour les amateurs/moyens)
        if magnitude is None or magnitude > 12:
            return ""

        intro = "== Potentiel d'observation ==\n"
        scenario = self._determine_observation_scenario(exoplanet, magnitude)

        if scenario:
            return intro + scenario
        return ""

    def _extract_apparent_magnitude(self, exoplanet: Exoplanet) -> float | None:
        raw = exoplanet.st_apparent_magnitude
        if raw is None:
            return None
        try:
            # Gestion robuste des types (valeur simple ou objet Quantity)
            return float(raw.value) if hasattr(raw, "value") else float(raw)
        except (ValueError, TypeError, AttributeError):
            return None

    def _determine_observation_scenario(self, exoplanet: Exoplanet, magnitude: float) -> str | None:
        # Booléens d'aide à la décision
        is_bright = magnitude < 10
        is_transiting = exoplanet.disc_method and "Transit" in str(exoplanet.disc_method)
        has_depth_data = exoplanet.pl_transit_depth and exoplanet.pl_transit_depth.value

        # 1. Scénario "Atmosphère" (Le Graal : brillant + transit)
        if is_bright and is_transiting and has_depth_data:
            return (
                f"Grâce à la brillance de son étoile hôte (magnitude apparente "
                f"de {magnitude:.1f}) et à sa détection par transit, "
                "cette exoplanète constitue une cible de choix pour la "
                "[[spectroscopie de transmission]]. De telles observations "
                "permettent d'extraire la composition atmosphérique, notamment via "
                "des instruments comme ceux du [[Télescope spatial James-Webb|JWST]].\n"
            )

        # 2. Scénario "Étoile Brillante" (Bonne cible photométrique)
        if is_bright:
            return (
                f"Son étoile hôte présente une magnitude apparente de "
                f"{magnitude:.1f}, ce qui en fait une cible brillante pour des "
                "observations photométriques ou spectroscopiques avancées.\n"
            )

        # 3. Scénario "Étoile Moyenne" (Accessible pour suivi)
        # On sait déjà que magnitude <= 12 grâce au guard clause dans generate()
        return (
            f"Avec une magnitude apparente de {magnitude:.1f}, "
            "l'étoile hôte reste accessible aux télescopes de taille moyenne "
            "pour des études de suivi.\n"
        )
