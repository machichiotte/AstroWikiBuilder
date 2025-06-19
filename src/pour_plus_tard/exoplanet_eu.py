# src/data_collectors/exoplanet_eu.py
import pandas as pd
from typing import List, Optional, Dict, Any
import logging
from src.collectors.base_collector import BaseCollector
from src.models.references.reference import Reference, SourceType
from src.models.entities.exoplanet import ValueWithUncertainty
from src.models.entities.exoplanet import Exoplanet

logger: logging.Logger = logging.getLogger(__name__)


class ExoplanetEUCollector(BaseCollector):
    def __init__(
        self, cache_dir: str = "data/cache/exoplanet_eu", use_mock_data: bool = False
    ):
        super().__init__(cache_dir, use_mock_data)

    def _get_default_cache_filename(self) -> str:
        return "exoplanet.eu_catalog.csv"

    def _get_download_url(self) -> str:
        return "http://exoplanet.eu/catalog/exoplanet.eu_catalog.csv"

    def _get_source_type(self) -> SourceType:
        return SourceType.EPE

    def _get_source_reference_url(self) -> str:
        return "https://exoplanet.eu/"

    def _get_required_columns(self) -> List[str]:
        return ["name", "star_name", "discovery_method", "discovery_year"]

    def _get_csv_reader_kwargs(self) -> Dict[str, Any]:
        return {"comment": "#"}

    def _convert_row_to_exoplanet(
        self, row: pd.Series, ref: Reference
    ) -> Optional[Exoplanet]:
        try:
            if pd.isna(row["name"]) or pd.isna(row["star_name"]):
                logger.warning(
                    f"Données de base manquantes pour l'exoplanète : {row.get('name', 'Unknown')} (Source: Exoplanet.eu)"
                )
                return None

            exoplanet = Exoplanet(
                pl_name=str(row["name"]).strip(),
                st_name=str(row["star_name"]).strip(),
                reference=ref,
            )

            # Caractéristiques orbitales
            for field, csv_field in [
                ("semi_major_axis", "semi_major_axis"),
                ("eccentricity", "eccentricity"),
                ("orbital_period", "orbital_period"),
                ("inclination", "inclination"),
                ("argument_of_periastron", "argument_of_periastron"),
                ("periastron_time", "periastron_time"),
            ]:
                value: float | None = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, ValueWithUncertainty(value=value))

            # Caractéristiques physiques
            for field, csv_field in [
                ("mass", "mass"),
                ("radius", "radius"),
                ("temperature", "temperature"),
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, ValueWithUncertainty(value=value))

            # Informations sur l'étoile
            for field, csv_field in [
                ("spectral_type", "spectral_type"),
                ("star_temperature", "star_temperature"),
                ("star_radius", "star_radius"),
                ("star_mass", "star_mass"),
                ("distance", "distance"),
                ("apparent_magnitude", "apparent_magnitude"),
            ]:
                value = row.get(csv_field)
                if pd.notna(value):
                    processed_value: float | None | str = (
                        self._safe_float_conversion(value)
                        if isinstance(value, (int, float, str))
                        and str(value).replace(".", "", 1).isdigit()
                        else str(value).strip()
                    )
                    if processed_value is not None:
                        if isinstance(processed_value, (int, float)):
                            setattr(
                                exoplanet,
                                field,
                                processed_value,
                            )
                        else:
                            setattr(exoplanet, field, processed_value)

            if pd.notna(row.get("alt_names")):
                names: List[str] = str(row["alt_names"]).split(",")
                for name in names:
                    name: str = name.strip()
                    if name and name != exoplanet.pl_name:
                        exoplanet.pl_altname.append(name)

            return exoplanet

        except Exception as e:
            logger.error(
                f"Erreur Exoplanet.eu lors de la conversion de la ligne : {row.get('name', 'Unknown')}. Erreur: {e}",
                exc_info=True,
            )
            return None
