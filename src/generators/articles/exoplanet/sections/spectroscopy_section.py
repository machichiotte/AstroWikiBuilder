# src/generators/articles/exoplanet/sections/spectroscopy_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class SpectroscopySection:
    """Génère la section spectroscopie pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur la spectroscopie."""
        if not any(
            [
                exoplanet.pl_ntranspec,
                exoplanet.pl_nespec,
                exoplanet.pl_ndispec,
            ]
        ):
            return ""

        content: list[str] = ["== Spectroscopie ==\n"]

        has_spectra = False

        if exoplanet.pl_ntranspec and exoplanet.pl_ntranspec > 0:
            content.append(
                f"L'atmosphère de l'exoplanète a été étudiée par spectroscopie de transmission, "
                f"avec {exoplanet.pl_ntranspec} spectre{'s' if exoplanet.pl_ntranspec > 1 else ''} disponible{'s' if exoplanet.pl_ntranspec > 1 else ''}."
            )
            has_spectra = True

        if exoplanet.pl_nespec and exoplanet.pl_nespec > 0:
            content.append(
                f"Des observations en spectroscopie d'éclipse ont été réalisées, "
                f"avec {exoplanet.pl_nespec} spectre{'s' if exoplanet.pl_nespec > 1 else ''} disponible{'s' if exoplanet.pl_nespec > 1 else ''}."
            )
            has_spectra = True

        if exoplanet.pl_ndispec and exoplanet.pl_ndispec > 0:
            content.append(
                f"L'exoplanète a également été observée par spectroscopie en imagerie directe, "
                f"avec {exoplanet.pl_ndispec} spectre{'s' if exoplanet.pl_ndispec > 1 else ''} disponible{'s' if exoplanet.pl_ndispec > 1 else ''}."
            )
            has_spectra = True

        if not has_spectra:
            return ""

        return "\n".join(content)
