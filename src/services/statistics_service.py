# src/services/statistics_service.py
import logging
from typing import List, Dict, Any
from src.models.data_source_star import DataSourceStar
from src.models.data_source_exoplanet import DataSourceExoplanet
from src.models.reference import DataPoint

logger = logging.getLogger(__name__)


class StatisticsService:
    def __init__(self):
        logger.info("StatisticsService initialized.")

    def generate_statistics_exoplanet(self, exoplanets: List[DataSourceExoplanet]) -> Dict[str, Any]:
        """
        Retourne des statistiques sur les données collectées.
        """
        if not exoplanets:
            logger.warning("No exoplanets provided for statistics generation.")
            return {
                "total_exoplanets": 0,
                "data_points_by_source": {},
                "disc_methods": {},
                "discovery_years": {},
            }

        stats = {
            "total_exoplanets": len(exoplanets),
            "data_points_by_source": {},  # Counts how many data points come from each SourceType
            "disc_methods": {},
            "discovery_years": {},
        }

        logger.info(f"Generating statistics for {len(exoplanets)} exoplanets.")

        for exoplanet in exoplanets:
            # Statistiques par source de données (pour chaque DataPoint)
            for field_name in exoplanet.__dataclass_fields__:
                if field_name in [
                    "name",
                    "pl_altname",
                ]:  # name is str, pl_altname is List[str]
                    continue

                value_attr = getattr(exoplanet, field_name)
                if (
                    isinstance(value_attr, DataPoint)
                    and value_attr.reference
                    and value_attr.reference.source
                ):
                    source_key = value_attr.reference.source.value  # e.g., "NEA"
                    stats["data_points_by_source"][source_key] = (
                        stats["data_points_by_source"].get(source_key, 0) + 1
                    )

            # Statistiques pour pl_altname - EPE specific in original code, now more generic
            # The original logic for 'EPE' for pl_altname seemed arbitrary without more context.
            # If 'pl_altname' are always considered from a specific source, that logic should be explicit.
            # For now, this specific stat is removed unless clarified.
            # if exoplanet.pl_altname:
            #     # Assuming 'EPE' was a placeholder for a default source for pl_altname
            #     # This needs clarification if 'pl_altname' should contribute to 'data_points_by_source'
            #     stats['data_points_by_source']['EPE_pl_altname'] = stats['data_points_by_source'].get('EPE_pl_altname', 0) + len(exoplanet.pl_altname)

            # Statistiques par méthode de découverte
            if exoplanet.disc_method and exoplanet.disc_method.value:
                method = str(exoplanet.disc_method.value)  # Ensure it's a string
                stats["disc_methods"][method] = (
                    stats["disc_methods"].get(method, 0) + 1
                )

            # Statistiques par année de découverte
            if exoplanet.disc_year and exoplanet.disc_year.value:
                try:
                    # Assuming disc_year.value could be a datetime object or a string representing a year or date
                    year_val = exoplanet.disc_year.value
                    if hasattr(year_val, "year"):  # if it's a datetime object
                        year = year_val.year
                    elif (
                        isinstance(year_val, str)
                        and len(year_val) >= 4
                        and year_val[:4].isdigit()
                    ):
                        year = int(year_val[:4])
                    elif isinstance(year_val, (int, float)):
                        year = int(year_val)
                    else:  # Skip if not easily parsable as a year
                        logger.debug(
                            f"Could not parse year from disc_year.value: {year_val}"
                        )
                        continue
                    stats["discovery_years"][year] = (
                        stats["discovery_years"].get(year, 0) + 1
                    )
                except ValueError:
                    logger.warning(
                        f"Could not parse year from disc_year.value: {exoplanet.disc_year.value} for exoplanet {exoplanet.pl_name}"
                    )

        logger.info("Statistics generation complete.")
        return stats

    def generate_statistics_star(self, stars: List[DataSourceStar]) -> Dict[str, Any]:
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
                    "name",
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
            if hasattr(star, "spectral_type") and star.spectral_type and getattr(star.spectral_type, "value", None):
                spectral = str(star.spectral_type.value)
                stats["spectral_types"][spectral] = (
                    stats["spectral_types"].get(spectral, 0) + 1
                )
    
            # Statistiques par année de découverte
            if hasattr(star, "disc_year") and star.disc_year and getattr(star.disc_year, "value", None):
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