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
            "insolation_ranges": {
                "0-0.5": 0,  # Très faible (au-delà de Mars)
                "0.5-1.5": 0,  # Zone habitable
                "1.5-10": 0,  # Modéré
                "10-100": 0,  # Élevé
                "100-1000": 0,  # Très élevé
                "1000+": 0,  # Extrême (Jupiters chauds)
            },
            "temperature_ranges": {
                "0-200": 0,  # Très froid
                "200-400": 0,  # Froid
                "400-600": 0,  # Tempéré
                "600-1000": 0,  # Chaud
                "1000-2000": 0,  # Très chaud
                "2000+": 0,  # Extrême
            },
            "density_categories": {
                "gazeuse": 0,  # < 2 g/cm³
                "neptunienne": 0,  # 2-4 g/cm³
                "tellurique": 0,  # > 4 g/cm³
            },
            "eccentricity_ranges": {
                "circulaire": 0,  # < 0.1
                "faible": 0,  # 0.1-0.3
                "modérée": 0,  # 0.3-0.5
                "élevée": 0,  # > 0.5
            },
            "planet_types": {},  # Types de planètes (Jupiter chaud, Neptune froid, etc.)
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

            # Plages d'insolation
            if exoplanet.pl_insolation_flux and exoplanet.pl_insolation_flux.value:
                self._update_insolation_stats(
                    exoplanet.pl_insolation_flux.value, stats["insolation_ranges"]
                )

            # Plages de température
            if exoplanet.pl_temperature and exoplanet.pl_temperature.value:
                self._update_temperature_stats(
                    exoplanet.pl_temperature.value, stats["temperature_ranges"]
                )

            # Catégories de densité
            if exoplanet.pl_density and exoplanet.pl_density.value:
                self._update_density_stats(exoplanet.pl_density.value, stats["density_categories"])

            # Plages d'excentricité
            if exoplanet.pl_eccentricity and exoplanet.pl_eccentricity.value:
                self._update_eccentricity_stats(
                    exoplanet.pl_eccentricity.value, stats["eccentricity_ranges"]
                )

            # Type de planète
            self._update_planet_type_stats(exoplanet, stats["planet_types"])

        logger.info("Statistics generation for exoplanets complete.")
        return stats

    def _update_insolation_stats(self, value: float, ranges_dict: dict[str, int]) -> None:
        """Catégorise l'insolation (flux stellaire relatif à la Terre)"""
        if value < 0.5:
            ranges_dict["0-0.5"] += 1
        elif value < 1.5:
            ranges_dict["0.5-1.5"] += 1
        elif value < 10:
            ranges_dict["1.5-10"] += 1
        elif value < 100:
            ranges_dict["10-100"] += 1
        elif value < 1000:
            ranges_dict["100-1000"] += 1
        else:
            ranges_dict["1000+"] += 1

    def _update_temperature_stats(self, value: float, ranges_dict: dict[str, int]) -> None:
        """Catégorise la température d'équilibre (en Kelvin)"""
        if value < 200:
            ranges_dict["0-200"] += 1
        elif value < 400:
            ranges_dict["200-400"] += 1
        elif value < 600:
            ranges_dict["400-600"] += 1
        elif value < 1000:
            ranges_dict["600-1000"] += 1
        elif value < 2000:
            ranges_dict["1000-2000"] += 1
        else:
            ranges_dict["2000+"] += 1

    def _update_density_stats(self, value: float, categories_dict: dict[str, int]) -> None:
        """Catégorise la densité (en g/cm³)"""
        if value < 2:
            categories_dict["gazeuse"] += 1
        elif value < 4:
            categories_dict["neptunienne"] += 1
        else:
            categories_dict["tellurique"] += 1

    def _update_eccentricity_stats(self, value: float, ranges_dict: dict[str, int]) -> None:
        """Catégorise l'excentricité orbitale"""
        if value < 0.1:
            ranges_dict["circulaire"] += 1
        elif value < 0.3:
            ranges_dict["faible"] += 1
        elif value < 0.5:
            ranges_dict["modérée"] += 1
        else:
            ranges_dict["élevée"] += 1

    def _update_planet_type_stats(self, exoplanet: Exoplanet, types_dict: dict[str, int]) -> None:
        """Catégorise les exoplanètes par type (Jupiter chaud, Neptune froid, etc.)"""
        from src.utils.astro.classification.exoplanet_type_util import ExoplanetTypeUtil

        classifier = ExoplanetTypeUtil()
        planet_type = classifier.determine_exoplanet_classification(exoplanet)
        types_dict[planet_type] = types_dict.get(planet_type, 0) + 1

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
