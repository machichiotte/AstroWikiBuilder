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
        Exporte tous les champs de l'entité Exoplanet.
        """
        data = {
            # Identifiants
            "pl_name": exoplanet.pl_name,
            "pl_altname": (", ".join(exoplanet.pl_altname) if exoplanet.pl_altname else None),
            "hd_name": exoplanet.hd_name,
            "hip_name": exoplanet.hip_name,
            "tic_id": exoplanet.tic_id,
            "gaia_id": exoplanet.gaia_id,
            "image": exoplanet.image,
            "caption": exoplanet.caption,
            "sy_constellation": exoplanet.sy_constellation,
            "sy_planet_count": exoplanet.sy_planet_count,
            "sy_snum": exoplanet.sy_snum,
            "sy_mnum": exoplanet.sy_mnum,
            "cb_flag": exoplanet.cb_flag,
            # Étoile hôte
            "st_name": exoplanet.st_name,
            "st_epoch": exoplanet.st_epoch,
            "st_right_ascension": exoplanet.st_right_ascension,
            "st_declination": exoplanet.st_declination,
            "st_distance": exoplanet.st_distance,
            "st_spectral_type": exoplanet.st_spectral_type,
            "st_apparent_magnitude": exoplanet.st_apparent_magnitude,
            "st_luminosity": exoplanet.st_luminosity,
            "st_mass": exoplanet.st_mass,
            "st_radius": exoplanet.st_radius,
            "st_variability": exoplanet.st_variability,
            "st_metallicity": exoplanet.st_metallicity,
            "st_age": exoplanet.st_age,
            # Caractéristiques orbitales
            "pl_semi_major_axis": exoplanet.pl_semi_major_axis,
            "pl_periastron": exoplanet.pl_periastron,
            "pl_apoastron": exoplanet.pl_apoastron,
            "pl_eccentricity": exoplanet.pl_eccentricity,
            "pl_orbital_period": exoplanet.pl_orbital_period,
            "pl_angular_distance": exoplanet.pl_angular_distance,
            "pl_periastron_time": exoplanet.pl_periastron_time,
            "pl_inclination": exoplanet.pl_inclination,
            "pl_argument_of_periastron": exoplanet.pl_argument_of_periastron,
            "pl_epoch": exoplanet.pl_epoch,
            "pl_projobliq": exoplanet.pl_projobliq,
            "pl_trueobliq": exoplanet.pl_trueobliq,
            "pl_imppar": exoplanet.pl_imppar,
            "pl_ratdor": exoplanet.pl_ratdor,
            "pl_ratror": exoplanet.pl_ratror,
            # Caractéristiques physiques
            "pl_mass": exoplanet.pl_mass,
            "pl_mass_earth": exoplanet.pl_mass_earth,
            "pl_minimum_mass": exoplanet.pl_minimum_mass,
            "pl_radius": exoplanet.pl_radius,
            "pl_radius_earth": exoplanet.pl_radius_earth,
            "pl_density": exoplanet.pl_density,
            "pl_gravity": exoplanet.pl_gravity,
            "pl_rotation_period": exoplanet.pl_rotation_period,
            "pl_temperature": exoplanet.pl_temperature,
            "pl_insolation_flux": exoplanet.pl_insolation_flux,
            "pl_transit_depth": exoplanet.pl_transit_depth,
            "pl_occultation_depth": exoplanet.pl_occultation_depth,
            "pl_albedo_bond": exoplanet.pl_albedo_bond,
            # Atmosphère
            "pl_pressure": exoplanet.pl_pressure,
            "pl_composition": exoplanet.pl_composition,
            "pl_wind_speed": exoplanet.pl_wind_speed,
            "pl_ntranspec": exoplanet.pl_ntranspec,
            "pl_nespec": exoplanet.pl_nespec,
            "pl_ndispec": exoplanet.pl_ndispec,
            # Découverte
            "disc_by": exoplanet.disc_by,
            "disc_program": exoplanet.disc_program,
            "disc_method": exoplanet.disc_method,
            "disc_year": exoplanet.disc_year,
            "disc_facility": exoplanet.disc_facility,
            "disc_telescope": exoplanet.disc_telescope,
            "disc_instrument": exoplanet.disc_instrument,
            "disc_pubdate": exoplanet.disc_pubdate,
            "pl_controv_flag": exoplanet.pl_controv_flag,
            "tran_flag": exoplanet.tran_flag,
            "rv_flag": exoplanet.rv_flag,
            "ttv_flag": exoplanet.ttv_flag,
            "ast_flag": exoplanet.ast_flag,
            "micro_flag": exoplanet.micro_flag,
            "pul_flag": exoplanet.pul_flag,
            "pre_discovery": exoplanet.pre_discovery,
            "detection_type": exoplanet.detection_type,
            "status": exoplanet.status,
        }
        return data

    def export_exoplanets_to_csv(self, filename: str, exoplanets: list[Exoplanet]) -> None:
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

    def export_exoplanets_to_json(self, filename: str, exoplanets: list[Exoplanet]) -> None:
        """Exporte les exoplanètes vers un fichier JSON"""
        logger.info(f"Exporting {len(exoplanets)} exoplanets to JSON: {filename}")
        if not exoplanets:
            logger.warning("No exoplanets to export to JSON.")
            return

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    [self._exoplanet_to_dict_flat(exoplanet) for exoplanet in exoplanets],
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
