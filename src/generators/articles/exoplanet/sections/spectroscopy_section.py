# src/generators/articles/exoplanet/sections/spectroscopy_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class SpectroscopySection:
    """Génère la section spectroscopie pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur la spectroscopie."""
        spectra_info = self._collect_spectra_info(exoplanet)

        if not spectra_info:
            return ""

        content: list[str] = ["== Spectroscopie ==\n"]
        content.extend(spectra_info)

        return "\n".join(content)

    def _collect_spectra_info(self, exoplanet: Exoplanet) -> list[str]:
        """Collecte les informations sur les spectres disponibles."""
        info = []

        if exoplanet.pl_ntranspec and exoplanet.pl_ntranspec > 0:
            info.append(self._format_transmission_spectra(exoplanet.pl_ntranspec))

        if exoplanet.pl_nespec and exoplanet.pl_nespec > 0:
            info.append(self._format_eclipse_spectra(exoplanet.pl_nespec))

        if exoplanet.pl_ndispec and exoplanet.pl_ndispec > 0:
            info.append(self._format_direct_imaging_spectra(exoplanet.pl_ndispec))

        return info

    def _format_transmission_spectra(self, count: int) -> str:
        """Formate l'information sur les spectres de transmission."""
        plural = "s" if count > 1 else ""
        return (
            f"L'atmosphère de l'exoplanète a été étudiée par spectroscopie de transmission, "
            f"avec {count} spectre{plural} disponible{plural}."
        )

    def _format_eclipse_spectra(self, count: int) -> str:
        """Formate l'information sur les spectres d'éclipse."""
        plural = "s" if count > 1 else ""
        return (
            f"Des observations en spectroscopie d'éclipse ont été réalisées, "
            f"avec {count} spectre{plural} disponible{plural}."
        )

    def _format_direct_imaging_spectra(self, count: int) -> str:
        """Formate l'information sur les spectres d'imagerie directe."""
        plural = "s" if count > 1 else ""
        return (
            f"L'exoplanète a également été observée par spectroscopie en imagerie directe, "
            f"avec {count} spectre{plural} disponible{plural}."
        )
