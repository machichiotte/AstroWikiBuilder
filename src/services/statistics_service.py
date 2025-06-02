# src/services/statistics_service.py
import logging
from typing import List, Dict, Any
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint

logger = logging.getLogger(__name__)


class StatisticsService:
    def __init__(self):
        logger.info("StatisticsService initialized.")

    def generate_statistics(self, exoplanets: List[Exoplanet]) -> Dict[str, Any]:
        """
        Retourne des statistiques sur les données collectées.
        """
        if not exoplanets:
            logger.warning("No exoplanets provided for statistics generation.")
            return {
                "total_exoplanets": 0,
                "data_points_by_source": {},
                "discovery_methods": {},
                "discovery_years": {},
            }

        stats = {
            "total_exoplanets": len(exoplanets),
            "data_points_by_source": {},  # Counts how many data points come from each SourceType
            "discovery_methods": {},
            "discovery_years": {},
        }

        logger.info(f"Generating statistics for {len(exoplanets)} exoplanets.")

        for exoplanet in exoplanets:
            # Statistiques par source de données (pour chaque DataPoint)
            for field_name in exoplanet.__dataclass_fields__:
                if field_name in [
                    "name",
                    "other_names",
                ]:  # name is str, other_names is List[str]
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

            # Statistiques pour other_names - EPE specific in original code, now more generic
            # The original logic for 'EPE' for other_names seemed arbitrary without more context.
            # If 'other_names' are always considered from a specific source, that logic should be explicit.
            # For now, this specific stat is removed unless clarified.
            # if exoplanet.other_names:
            #     # Assuming 'EPE' was a placeholder for a default source for other_names
            #     # This needs clarification if 'other_names' should contribute to 'data_points_by_source'
            #     stats['data_points_by_source']['EPE_other_names'] = stats['data_points_by_source'].get('EPE_other_names', 0) + len(exoplanet.other_names)

            # Statistiques par méthode de découverte
            if exoplanet.discovery_method and exoplanet.discovery_method.value:
                method = str(exoplanet.discovery_method.value)  # Ensure it's a string
                stats["discovery_methods"][method] = (
                    stats["discovery_methods"].get(method, 0) + 1
                )

            # Statistiques par année de découverte
            if exoplanet.discovery_date and exoplanet.discovery_date.value:
                try:
                    # Assuming discovery_date.value could be a datetime object or a string representing a year or date
                    year_val = exoplanet.discovery_date.value
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
                            f"Could not parse year from discovery_date.value: {year_val}"
                        )
                        continue
                    stats["discovery_years"][year] = (
                        stats["discovery_years"].get(year, 0) + 1
                    )
                except ValueError:
                    logger.warning(
                        f"Could not parse year from discovery_date.value: {exoplanet.discovery_date.value} for exoplanet {exoplanet.name}"
                    )

        logger.info("Statistics generation complete.")
        return stats
