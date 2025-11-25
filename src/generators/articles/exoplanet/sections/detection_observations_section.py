# src/generators/articles/exoplanet/sections/detection_observations_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class DetectionObservationsSection:
    """Génère la section détection et observations pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur les méthodes de détection et observations."""
        # Vérifier s'il y a des méthodes de détection multiples
        detection_methods = []

        if exoplanet.tran_flag and exoplanet.tran_flag == 1:
            detection_methods.append("transits")
        if exoplanet.rv_flag and exoplanet.rv_flag == 1:
            detection_methods.append("vitesses radiales")
        if exoplanet.ttv_flag and exoplanet.ttv_flag == 1:
            detection_methods.append("variations du temps de transit (TTV)")
        if exoplanet.ast_flag and exoplanet.ast_flag == 1:
            detection_methods.append("astrométrie")
        if exoplanet.micro_flag and exoplanet.micro_flag == 1:
            detection_methods.append("microlentille gravitationnelle")
        if exoplanet.pul_flag and exoplanet.pul_flag == 1:
            detection_methods.append("chronométrage de pulsar")

        # Ne générer la section que s'il y a au moins 2 méthodes ou une facilité
        if len(detection_methods) < 2 and not exoplanet.disc_facility:
            return ""

        content: list[str] = ["== Détection et observations ==\n"]

        if len(detection_methods) >= 2:
            methods_str = ", ".join(detection_methods[:-1]) + f" et {detection_methods[-1]}"
            content.append(f"L'exoplanète a été détectée par plusieurs méthodes : {methods_str}.")

        if exoplanet.disc_facility:
            content.append(f"Les observations ont été réalisées avec {exoplanet.disc_facility}.")

        return "\n".join(content)
