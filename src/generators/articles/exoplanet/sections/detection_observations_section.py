# src/generators/articles/exoplanet/sections/detection_observations_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class DetectionObservationsSection:
    """Génère la section détection et observations pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur les méthodes de détection et observations."""
        detection_methods = self._collect_detection_methods(exoplanet)

        # Ne générer la section que s'il y a au moins 2 méthodes ou une facilité
        if len(detection_methods) < 2 and not exoplanet.disc_facility:
            return ""

        content: list[str] = ["== Détection et observations ==\n"]

        if len(detection_methods) >= 2:
            methods_str = self._format_methods_list(detection_methods)
            content.append(f"L'exoplanète a été détectée par plusieurs méthodes : {methods_str}.")

        if exoplanet.disc_facility:
            content.append(f"Les observations ont été réalisées avec {exoplanet.disc_facility}.")

        return "\n".join(content)

    def _collect_detection_methods(self, exoplanet: Exoplanet) -> list[str]:
        """Collecte les méthodes de détection utilisées."""
        methods = []

        method_mapping = {
            "tran_flag": "transits",
            "rv_flag": "vitesses radiales",
            "ttv_flag": "variations du temps de transit (TTV)",
            "ast_flag": "astrométrie",
            "micro_flag": "microlentille gravitationnelle",
            "pul_flag": "chronométrage de pulsar",
        }

        for flag_name, method_name in method_mapping.items():
            flag_value = getattr(exoplanet, flag_name, None)
            if flag_value and flag_value == 1:
                methods.append(method_name)

        return methods

    def _format_methods_list(self, methods: list[str]) -> str:
        """Formate la liste des méthodes en français."""
        if len(methods) == 1:
            return methods[0]
        return ", ".join(methods[:-1]) + f" et {methods[-1]}"
