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
            # Nouvelles statistiques orbitales
            "orbital_period_ranges": {
                "< 1 jour": 0,
                "1-10 jours": 0,
                "10-100 jours": 0,
                "100-365 jours": 0,
                "1-10 ans": 0,
                "> 10 ans": 0,
            },
            "semi_major_axis_ranges": {
                "< 0.1 UA": 0,
                "0.1-0.5 UA": 0,
                "0.5-1.5 UA": 0,
                "1.5-5 UA": 0,
                "> 5 UA": 0,
            },
            "inclination_ranges": {
                "< 10°": 0,
                "10-45°": 0,
                "45-90°": 0,
                "> 90°": 0,
            },
            # Statistiques de découverte
            "discovery_facilities": {},
            "discovery_telescopes": {},
            "discovery_programs": {},
            # Statistiques stellaires
            "star_distance_ranges": {
                "< 10 pc": 0,
                "10-50 pc": 0,
                "50-100 pc": 0,
                "100-500 pc": 0,
                "> 500 pc": 0,
            },
            "star_magnitude_ranges": {
                "< 5": 0,
                "5-10": 0,
                "10-15": 0,
                "> 15": 0,
            },
            "star_metallicity_ranges": {
                "< -0.5": 0,
                "-0.5 à 0": 0,
                "0 à +0.5": 0,
                "> +0.5": 0,
            },
            # Statistiques système
            "system_planet_count": {
                "1": 0,
                "2": 0,
                "3-5": 0,
                "> 5": 0,
            },
            "constellations": {},
            # Statistiques atmosphériques
            "atmospheric_observations": {
                "with_transmission_spectrum": 0,
                "with_emission_spectrum": 0,
                "with_direct_imaging": 0,
                "no_atmospheric_data": 0,
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

            # Nouvelles statistiques orbitales
            if exoplanet.pl_orbital_period and exoplanet.pl_orbital_period.value:
                self._update_orbital_period_stats(
                    exoplanet.pl_orbital_period.value, stats["orbital_period_ranges"]
                )

            if exoplanet.pl_semi_major_axis and exoplanet.pl_semi_major_axis.value:
                self._update_semi_major_axis_stats(
                    exoplanet.pl_semi_major_axis.value, stats["semi_major_axis_ranges"]
                )

            if exoplanet.pl_inclination and exoplanet.pl_inclination.value:
                self._update_inclination_stats(
                    exoplanet.pl_inclination.value, stats["inclination_ranges"]
                )

            # Statistiques de découverte
            if exoplanet.disc_facility:
                stats["discovery_facilities"][exoplanet.disc_facility] = (
                    stats["discovery_facilities"].get(exoplanet.disc_facility, 0) + 1
                )

            if exoplanet.disc_telescope:
                stats["discovery_telescopes"][exoplanet.disc_telescope] = (
                    stats["discovery_telescopes"].get(exoplanet.disc_telescope, 0) + 1
                )

            if exoplanet.disc_program:
                stats["discovery_programs"][exoplanet.disc_program] = (
                    stats["discovery_programs"].get(exoplanet.disc_program, 0) + 1
                )

            # Statistiques stellaires
            if exoplanet.st_distance and exoplanet.st_distance.value:
                self._update_star_distance_stats(
                    exoplanet.st_distance.value, stats["star_distance_ranges"]
                )

            if exoplanet.st_apparent_magnitude:
                # st_apparent_magnitude peut être float ou ValueWithUncertainty
                mag_value = (
                    exoplanet.st_apparent_magnitude.value
                    if hasattr(exoplanet.st_apparent_magnitude, "value")
                    else exoplanet.st_apparent_magnitude
                )
                if mag_value is not None:
                    self._update_star_magnitude_stats(mag_value, stats["star_magnitude_ranges"])

            if exoplanet.st_metallicity and exoplanet.st_metallicity.value:
                self._update_star_metallicity_stats(
                    exoplanet.st_metallicity.value, stats["star_metallicity_ranges"]
                )

            # Statistiques système
            if exoplanet.sy_planet_count:
                # sy_planet_count peut être int ou ValueWithUncertainty
                count_value = (
                    exoplanet.sy_planet_count.value
                    if hasattr(exoplanet.sy_planet_count, "value")
                    else exoplanet.sy_planet_count
                )
                if count_value is not None:
                    self._update_system_planet_count_stats(
                        int(count_value), stats["system_planet_count"]
                    )

            if exoplanet.sy_constellation:
                stats["constellations"][exoplanet.sy_constellation] = (
                    stats["constellations"].get(exoplanet.sy_constellation, 0) + 1
                )

            # Statistiques atmosphériques
            self._update_atmospheric_observations_stats(
                exoplanet, stats["atmospheric_observations"]
            )

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

    def _update_orbital_period_stats(self, value: float, ranges_dict: dict[str, int]) -> None:
        """Catégorise la période orbitale (en jours)"""
        if value < 1:
            ranges_dict["< 1 jour"] += 1
        elif value < 10:
            ranges_dict["1-10 jours"] += 1
        elif value < 100:
            ranges_dict["10-100 jours"] += 1
        elif value < 365:
            ranges_dict["100-365 jours"] += 1
        elif value < 3650:  # 10 ans
            ranges_dict["1-10 ans"] += 1
        else:
            ranges_dict["> 10 ans"] += 1

    def _update_semi_major_axis_stats(self, value: float, ranges_dict: dict[str, int]) -> None:
        """Catégorise le demi-grand axe (en UA)"""
        if value < 0.1:
            ranges_dict["< 0.1 UA"] += 1
        elif value < 0.5:
            ranges_dict["0.1-0.5 UA"] += 1
        elif value < 1.5:
            ranges_dict["0.5-1.5 UA"] += 1
        elif value < 5:
            ranges_dict["1.5-5 UA"] += 1
        else:
            ranges_dict["> 5 UA"] += 1

    def _update_inclination_stats(self, value: float, ranges_dict: dict[str, int]) -> None:
        """Catégorise l'inclinaison orbitale (en degrés)"""
        if value < 10:
            ranges_dict["< 10°"] += 1
        elif value < 45:
            ranges_dict["10-45°"] += 1
        elif value < 90:
            ranges_dict["45-90°"] += 1
        else:
            ranges_dict["> 90°"] += 1

    def _update_star_distance_stats(self, value: float, ranges_dict: dict[str, int]) -> None:
        """Catégorise la distance stellaire (en parsecs)"""
        if value < 10:
            ranges_dict["< 10 pc"] += 1
        elif value < 50:
            ranges_dict["10-50 pc"] += 1
        elif value < 100:
            ranges_dict["50-100 pc"] += 1
        elif value < 500:
            ranges_dict["100-500 pc"] += 1
        else:
            ranges_dict["> 500 pc"] += 1

    def _update_star_magnitude_stats(self, value: float, ranges_dict: dict[str, int]) -> None:
        """Catégorise la magnitude apparente"""
        if value < 5:
            ranges_dict["< 5"] += 1
        elif value < 10:
            ranges_dict["5-10"] += 1
        elif value < 15:
            ranges_dict["10-15"] += 1
        else:
            ranges_dict["> 15"] += 1

    def _update_star_metallicity_stats(self, value: float, ranges_dict: dict[str, int]) -> None:
        """Catégorise la métallicité stellaire [Fe/H]"""
        if value < -0.5:
            ranges_dict["< -0.5"] += 1
        elif value < 0:
            ranges_dict["-0.5 à 0"] += 1
        elif value < 0.5:
            ranges_dict["0 à +0.5"] += 1
        else:
            ranges_dict["> +0.5"] += 1

    def _update_system_planet_count_stats(self, value: int, ranges_dict: dict[str, int]) -> None:
        """Catégorise le nombre de planètes par système"""
        if value == 1:
            ranges_dict["1"] += 1
        elif value == 2:
            ranges_dict["2"] += 1
        elif value <= 5:
            ranges_dict["3-5"] += 1
        else:
            ranges_dict["> 5"] += 1

    def _update_atmospheric_observations_stats(
        self, exoplanet: Exoplanet, stats_dict: dict[str, int]
    ) -> None:
        """Catégorise les observations atmosphériques"""
        has_data = False

        if exoplanet.pl_ntranspec and exoplanet.pl_ntranspec > 0:
            stats_dict["with_transmission_spectrum"] += 1
            has_data = True

        if exoplanet.pl_nespec and exoplanet.pl_nespec > 0:
            stats_dict["with_emission_spectrum"] += 1
            has_data = True

        if exoplanet.pl_ndispec and exoplanet.pl_ndispec > 0:
            stats_dict["with_direct_imaging"] += 1
            has_data = True

        if not has_data:
            stats_dict["no_atmospheric_data"] += 1

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
