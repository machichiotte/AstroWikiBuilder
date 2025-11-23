# src/services/external/export_service.py
import csv
import json
import logging
from typing import Any

from src.models.entities.exoplanet_entity import Exoplanet

logger: logging.Logger = logging.getLogger(__name__)


class ExportService:
    def __init__(self):
        logger.info("ExportService initialized.")

    def _exoplanet_to_dict_flat(self, exoplanet: Exoplanet) -> dict[str, Any]:
        """
        Convertit un objet Exoplanet en dictionnaire avec des valeurs 'plates'.
        """
        data = {
            "pl_name": exoplanet.pl_name,
            "pl_altname": (
                ", ".join(exoplanet.pl_altname) if exoplanet.pl_altname else None
            ),
            "st_name": exoplanet.st_name,
            "st_spectral_type": exoplanet.st_spectral_type,
            "st_distance": exoplanet.st_distance,
            "st_apparent_magnitude": exoplanet.st_apparent_magnitude,
            "pl_semi_major_axis": exoplanet.pl_semi_major_axis,
            "pl_eccentricity": exoplanet.pl_eccentricity,
            "pl_orbital_period": exoplanet.pl_orbital_period,
            "pl_angular_distance": exoplanet.pl_angular_distance,
            "pl_periastron_time": exoplanet.pl_periastron_time,
            "pl_inclination": exoplanet.pl_inclination,
            "pl_argument_of_periastron": exoplanet.pl_argument_of_periastron,
            "pl_mass": exoplanet.pl_mass,
            "pl_minimum_mass": exoplanet.pl_minimum_mass,
            "pl_radius": exoplanet.pl_radius,
            "pl_density": exoplanet.pl_density,
            "pl_temperature": exoplanet.pl_temperature,
            "disc_method": exoplanet.disc_method,
            "disc_year": exoplanet.disc_year,
            "disc_facility": exoplanet.disc_facility,
        }
        return data

    def export_exoplanets_to_csv(
        self, filename: str, exoplanets: list[Exoplanet]
    ) -> None:
        """Exporte les exoplanètes vers un fichier CSV"""
        logger.info(f"Exporting {len(exoplanets)} exoplanets to CSV: {filename}")
        if not exoplanets:
            logger.warning("No exoplanets to export to CSV.")
            return

        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=self._exoplanet_to_dict_flat(exoplanets[0]).keys()
                )
                writer.writeheader()
                writer.writerows(
                    self._exoplanet_to_dict_flat(exoplanet) for exoplanet in exoplanets
                )
            logger.info(f"Successfully exported exoplanets to {filename}")
        except Exception as e:
            logger.error(f"Error exporting exoplanets to CSV {filename}: {e}")

    def export_exoplanets_to_json(
        self, filename: str, exoplanets: list[Exoplanet]
    ) -> None:
        """Exporte les exoplanètes vers un fichier JSON"""
        logger.info(f"Exporting {len(exoplanets)} exoplanets to JSON: {filename}")
        if not exoplanets:
            logger.warning("No exoplanets to export to JSON.")
            return

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    [
                        self._exoplanet_to_dict_flat(exoplanet)
                        for exoplanet in exoplanets
                    ],
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
            logger.info(f"Successfully exported exoplanets to {filename}")
        except Exception as e:
            logger.error(f"Error exporting exoplanets to JSON {filename}: {e}")

    def export_generic_list_of_dicts_to_csv(
        self, filename: str, data: list, headers: list = None
    ) -> None:
        """Exporte une liste de dictionnaires vers un fichier CSV générique."""
        logger.info(f"Exporting generic data to CSV: {filename}")
        if not data:
            logger.warning("No data to export to CSV.")
            return
        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                if not headers:
                    headers = list(data[0].keys())
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"Successfully exported generic data to {filename}")
        except Exception as e:
            logger.error(f"Error exporting generic data to CSV {filename}: {e}")

    def export_generic_list_of_dicts_to_json(self, filename: str, data: list) -> None:
        """Exporte une liste de dictionnaires vers un fichier JSON générique."""
        logger.info(f"Exporting generic data to JSON: {filename}")
        if not data:
            logger.warning("No data to export to JSON.")
            return
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Successfully exported generic data to {filename}")
        except Exception as e:
            logger.error(f"Error exporting generic data to JSON {filename}: {e}")
