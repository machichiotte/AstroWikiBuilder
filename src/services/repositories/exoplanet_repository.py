# src/services/repositories/exoplanet_repository.py
import logging
from typing import List, Dict
from src.models.entities.exoplanet_model import Exoplanet

logger: logging.Logger = logging.getLogger(__name__)


class ExoplanetRepository:
    def __init__(self):
        self.exoplanets: Dict[str, Exoplanet] = {}
        logger.info("ExoplanetRepository initialized.")

    def add_exoplanets(self, exoplanets: List[Exoplanet], source_system: str) -> None:
        """
        Ajoute ou fusionne les exoplanètes dans le dictionnaire.
        Le paramètre 'source_system' indique le système ou le lot d'où proviennent ces données.
        """
        logger.info(
            f"Attempting to add {len(exoplanets)} exoplanets from source system: {source_system}..."
        )
        added_count = 0
        merged_count = 0
        for exoplanet in exoplanets:
            if not exoplanet.pl_name:
                logger.warning("Skipping exoplanet with no name.")
                continue
            if exoplanet.pl_name in self.exoplanets:
                logger.debug(
                    f"Merging data for existing exoplanet: {exoplanet.pl_name}"
                )
                merged_count += 1
            else:
                logger.debug(f"Adding new exoplanet: {exoplanet.pl_name}")
                self.exoplanets[exoplanet.pl_name] = exoplanet
                added_count += 1
        logger.info(
            f"Addition from {source_system} complete. Added: {added_count}, Merged: {merged_count}. Total exoplanets: {len(self.exoplanets)}"
        )

    def get_all_exoplanets(self) -> List[Exoplanet]:
        return list(self.exoplanets.values())
