# src/data_collectors/open_exoplanet_collection.py
import pandas as pd
from typing import List, Optional
import logging

from src.data_collectors.base_collector import BaseExoplanetCollector  # MODIFIÉ
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, Reference, SourceType

logger = logging.getLogger(__name__)


class OpenExoplanetCollector(BaseExoplanetCollector):  # MODIFIÉ
    def __init__(
        self, cache_dir: str = "data/cache/oec", use_mock_data: bool = False
    ):  # MODIFIÉ
        super().__init__(cache_dir, use_mock_data)

    def _get_default_cache_filename(self) -> str:
        return "open_exoplanet_catalogue.txt"

    def _get_download_url(self) -> str:
        return "https://raw.githubusercontent.com/OpenExoplanetCatalogue/oec_tables/master/comma_separated/open_exoplanet_catalogue.txt"

    def _get_source_type(self) -> SourceType:
        return SourceType.OEC

    def _get_source_reference_url(self) -> str:
        return "https://github.com/OpenExoplanetCatalogue/oec_tables"

    def _get_required_columns(self) -> List[str]:
        # Définissez ici les colonnes que vous considérez comme critiques pour OEC, par exemple:
        return ["name", "star_name"]  # À adapter selon les besoins réels

    # _get_csv_reader_kwargs n'a pas besoin d'être surchargé si le CSV OEC n'a pas de commentaires spéciaux

    def _convert_row_to_exoplanet(
        self, row: pd.Series, ref: Reference
    ) -> Optional[Exoplanet]:  # MODIFIÉ
        try:
            if pd.isna(row["name"]) or pd.isna(row["star_name"]):
                logger.warning(
                    f"Données de base manquantes pour l'exoplanète : {row.get('name', 'Unknown')} (Source: OEC)"
                )
                return None

            exoplanet = Exoplanet(
                name=str(row["name"]).strip(),
                host_star=DataPoint(str(row["star_name"]).strip(), ref),
                discovery_method=DataPoint(str(row["discovery_method"]).strip(), ref)
                if pd.notna(row["discovery_method"])
                else None,
                discovery_date=DataPoint(str(row["discovery_year"]).strip(), ref)
                if pd.notna(row["discovery_year"])
                else None,
            )

            # Caractéristiques orbitales
            for field, csv_field in [
                ("semi_major_axis", "semimajoraxis"),
                ("eccentricity", "eccentricity"),
                ("orbital_period", "period"),
                ("inclination", "inclination"),
                ("argument_of_periastron", "longitudeofperiastron"),
                ("periastron_time", "periastrontime"),
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref))

            # Caractéristiques physiques
            for field, csv_field in [
                ("mass", "mass"),
                ("radius", "radius"),
                (
                    "temperature",
                    "temperature",
                ),  # OEC a 'temperature', EPE a 'temp_calculated', NASA a 'pl_eqt'
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref))

            # Informations sur l'étoile
            for field, csv_field in [
                ("spectral_type", "spectraltype"),
                (
                    "star_temperature",
                    "star_temperature",
                ),  # OEC a 'star_temperature', EPE/NASA ont 'star_teff'
                ("star_radius", "star_radius"),
                ("star_mass", "star_mass"),
                ("distance", "distance"),
                (
                    "apparent_magnitude",
                    "apparentmagnitude",
                ),  # OEC a 'apparentmagnitude', EPE a 'mag_v', NASA a 'sy_vmag'
            ]:
                value = row.get(csv_field)
                if pd.notna(value):
                    processed_value = (
                        self._safe_float_conversion(value)
                        if isinstance(value, (int, float, str))
                        and str(value).replace(".", "", 1).isdigit()
                        else str(value).strip()
                    )
                    if processed_value is not None:
                        setattr(exoplanet, field, DataPoint(processed_value, ref))

            if pd.notna(row.get("alt_names")):  # OEC utilise 'alt_names'
                names = str(row["alt_names"]).split(",")
                for name in names:
                    name = name.strip()
                    if name and name != exoplanet.name:
                        exoplanet.other_names.append(name)

            return exoplanet

        except Exception as e:
            logger.error(
                f"Erreur OEC lors de la conversion de la ligne : {row.get('name', 'Unknown')}. Erreur: {e}",
                exc_info=True,
            )
            return None
