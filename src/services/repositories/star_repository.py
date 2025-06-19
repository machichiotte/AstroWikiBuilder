# src/services/repositories/star_repository.py
import logging
from typing import List, Dict
from src.models.entities.star import Star

logger: logging.Logger = logging.getLogger(__name__)


class StarRepository:
    def __init__(self):
        self.stars: Dict[str, Star] = {}
        logger.info("StarRepository initialized.")

    def add_stars(self, stars: List[Star], source_system: str) -> None:
        """
        Ajoute ou fusionne les exoplanètes dans le dictionnaire.
        Le paramètre 'source_system' indique le système ou le lot d'où proviennent ces données,
        pas nécessairement la 'SourceType' d'une donnée individuelle.
        """
        logger.info(
            f"Attempting to add {len(stars)} stars from source system: {source_system}..."
        )
        added_count = 0
        merged_count = 0
        for star in stars:
            if not star.st_name:
                logger.warning("Skipping star with no name.")
                continue
            if star.st_name in self.stars:
                logger.debug(f"Merging data for existing star: {star.st_name}")
                merged_count += 1
            else:
                logger.debug(f"Adding new star: {star.st_name}")
                self.stars[star.st_name] = star
                added_count += 1
        logger.info(
            f"Addition from {source_system} complete. Added: {added_count}, Merged: {merged_count}. Total stars: {len(self.stars)}"
        )

    def get_all_stars(self) -> List[Star]:
        return list(self.stars.values())
