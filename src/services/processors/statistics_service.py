# src/services/processors/statistics_service.py
import logging
from typing import Any

from src.models.entities.exoplanet_entity import Exoplanet
from src.models.entities.star_entity import Star

logger: logging.Logger = logging.getLogger(__name__)


class StatisticsService:
    def __init__(self):
        logger.info("StatisticsService initialized.")

    def _update_discovery_methods_stats(self, exoplanet: Exoplanet, stats: dict[str, Any]) -> None:
        if exoplanet.disc_method:
            method: str = exoplanet.disc_method
            stats["discovery_methods"][method] = stats["discovery_methods"].get(method, 0) + 1

    def _update_discovery_years_stats(self, exoplanet: Exoplanet, stats: dict[str, Any]) -> None:
        if exoplanet.disc_year:
            year: int = int(exoplanet.disc_year)
            stats["discovery_years"][year] = stats["discovery_years"].get(year, 0) + 1

    def _update_range_stats(self, value: float, ranges_dict: dict[str, int]) -> None:
        if value <= 1:
            ranges_dict["0-1"] += 1
        elif value <= 2:
            ranges_dict["1-2"] += 1
        elif value <= 5:
            ranges_dict["2-5"] += 1
        elif value <= 10:
            ranges_dict["5-10"] += 1
        else:
            ranges_dict["10+"] += 1

    def generate_statistics_exoplanet(self, exoplanets: list[Exoplanet]) -> dict[str, Any]:
        """Génère les statistiques pour les exoplanètes"""
        logger.info(f"Generating statistics for {len(exoplanets)} exoplanets.")
        stats = {
            "total": len(exoplanets),
            "discovery_methods": {},
            "discovery_years": {},
            "mass_ranges": {
                "0-1": 0,
                "1-2": 0,
                "2-5": 0,
                "5-10": 0,
                "10+": 0,
            },
            "radius_ranges": {
                "0-1": 0,
                "1-2": 0,
                "2-5": 0,
                "5-10": 0,
                "10+": 0,
            },
        }

        for exoplanet in exoplanets:
            self._update_discovery_methods_stats(exoplanet, stats)
            self._update_discovery_years_stats(exoplanet, stats)

            # Plages de masse
            if exoplanet.pl_mass and exoplanet.pl_mass.value:
                self._update_range_stats(exoplanet.pl_mass.value, stats["mass_ranges"])

            # Plages de rayon
            if exoplanet.pl_radius and exoplanet.pl_radius.value:
                self._update_range_stats(exoplanet.pl_radius.value, stats["radius_ranges"])

        logger.info("Statistics generation for exoplanets complete.")
        return stats

    def generate_statistics_star(self, stars: list[Star]) -> dict[str, Any]:
        """
        Retourne des statistiques sur les données collectées pour les étoiles.
        """
        if not stars:
            logger.warning("No stars provided for statistics generation.")
            return {
                "total_stars": 0,
                "spectral_types": {},
                "discovery_years": {},
            }

        stats = {
            "total_stars": len(stars),
            "spectral_types": {},
            "discovery_years": {},
        }

        logger.info(f"Generating statistics for {len(stars)} stars.")

        for star in stars:
            # Statistiques par type spectral
            if star.st_spectral_type:
                spectral = str(star.st_spectral_type)
                stats["spectral_types"][spectral] = stats["spectral_types"].get(spectral, 0) + 1

            # Statistiques par année de découverte
            if hasattr(star, "disc_year") and star.disc_year and star.disc_year.value:
                try:
                    disc_year: int = int(star.disc_year.value)
                    stats["discovery_years"][disc_year] = (
                        stats["discovery_years"].get(disc_year, 0) + 1
                    )
                except ValueError:
                    logger.warning(
                        f"Could not parse year from disc_year.value: {star.disc_year.value} for star {star.st_name}"
                    )

        logger.info("Statistics generation for stars complete.")
        return stats
