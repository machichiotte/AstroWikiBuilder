# src/services/processors/statistics_service.py
import logging
from typing import List, Dict, Any
from src.models.entities.exoplanet import Exoplanet
from src.models.entities.star import Star
from src.models.references.data_point import DataPoint

logger = logging.getLogger(__name__)


class StatisticsService:
    def __init__(self):
        logger.info("StatisticsService initialized.")

    def generate_statistics_exoplanet(
        self, exoplanets: List[Exoplanet]
    ) -> Dict[str, Any]:
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
            # Méthodes de découverte
            if exoplanet.disc_method and exoplanet.disc_method.value:
                method = exoplanet.disc_method.value
                stats["discovery_methods"][method] = (
                    stats["discovery_methods"].get(method, 0) + 1
                )

            # Années de découverte
            if exoplanet.disc_year and exoplanet.disc_year.value:
                year = exoplanet.disc_year.value
                stats["discovery_years"][year] = (
                    stats["discovery_years"].get(year, 0) + 1
                )

            # Plages de masse
            if exoplanet.pl_mass and exoplanet.pl_mass.value:
                mass = exoplanet.pl_mass.value
                if mass <= 1:
                    stats["mass_ranges"]["0-1"] += 1
                elif mass <= 2:
                    stats["mass_ranges"]["1-2"] += 1
                elif mass <= 5:
                    stats["mass_ranges"]["2-5"] += 1
                elif mass <= 10:
                    stats["mass_ranges"]["5-10"] += 1
                else:
                    stats["mass_ranges"]["10+"] += 1

            # Plages de rayon
            if exoplanet.pl_radius and exoplanet.pl_radius.value:
                radius = exoplanet.pl_radius.value
                if radius <= 1:
                    stats["radius_ranges"]["0-1"] += 1
                elif radius <= 2:
                    stats["radius_ranges"]["1-2"] += 1
                elif radius <= 5:
                    stats["radius_ranges"]["2-5"] += 1
                elif radius <= 10:
                    stats["radius_ranges"]["5-10"] += 1
                else:
                    stats["radius_ranges"]["10+"] += 1

        logger.info("Statistics generation for exoplanets complete.")
        return stats

    def generate_statistics_star(self, stars: List[Star]) -> Dict[str, Any]:
        """
        Retourne des statistiques sur les données collectées pour les étoiles.
        """
        if not stars:
            logger.warning("No stars provided for statistics generation.")
            return {
                "total_stars": 0,
                "data_points_by_source": {},
                "spectral_types": {},
                "discovery_years": {},
            }

        stats = {
            "total_stars": len(stars),
            "data_points_by_source": {},
            "spectral_types": {},
            "discovery_years": {},
        }

        logger.info(f"Generating statistics for {len(stars)} stars.")

        for star in stars:
            # Statistiques par source de données (pour chaque DataPoint)
            for field_name in star.__dataclass_fields__:
                if field_name in [
                    "st_name",
                    "pl_altname",
                ]:
                    continue

                value_attr = getattr(star, field_name)
                if (
                    isinstance(value_attr, DataPoint)
                    and value_attr.reference
                    and value_attr.reference.source
                ):
                    source_key = value_attr.reference.source.value
                    stats["data_points_by_source"][source_key] = (
                        stats["data_points_by_source"].get(source_key, 0) + 1
                    )

            # Statistiques par type spectral
            if (
                hasattr(star, "st_spectral_type")
                and star.st_spectral_type
                and star.st_spectral_type.value
            ):
                spectral = str(star.st_spectral_type.value)
                stats["spectral_types"][spectral] = (
                    stats["spectral_types"].get(spectral, 0) + 1
                )

            # Statistiques par année de découverte
            if hasattr(star, "disc_year") and star.disc_year and star.disc_year.value:
                try:
                    year_val = star.disc_year.value
                    if hasattr(year_val, "year"):
                        year = year_val.year
                    elif (
                        isinstance(year_val, str)
                        and len(year_val) >= 4
                        and year_val[:4].isdigit()
                    ):
                        year = int(year_val[:4])
                    elif isinstance(year_val, (int, float)):
                        year = int(year_val)
                    else:
                        logger.debug(
                            f"Could not parse year from disc_year.value: {year_val}"
                        )
                        continue
                    stats["discovery_years"][year] = (
                        stats["discovery_years"].get(year, 0) + 1
                    )
                except ValueError:
                    logger.warning(
                        f"Could not parse year from disc_year.value: {star.disc_year.value} for star {star.st_name}"
                    )

        logger.info("Statistics generation for stars complete.")
        return stats
