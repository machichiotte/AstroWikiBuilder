# src/data_collectors/exoplanet_eu.py
import pandas as pd
from typing import List, Optional, Dict, Any
import logging
from src.data_collectors.base_collector import BaseExoplanetCollector  # MODIFIÉ
from src.models.exoplanet import (
    Exoplanet,
)  # Assurez-vous que Exoplanet, DataPoint etc. sont accessibles
from src.models.reference import DataPoint, Reference, SourceType

logger = logging.getLogger(__name__)


class ExoplanetEUCollector(BaseExoplanetCollector):  # MODIFIÉ
    # DOWNLOAD_URL est maintenant géré par _get_download_url
    # self.cache_path est maintenant géré par la classe de base
    # self.reference_manager et self.last_update_date sont gérés par la classe de base

    def __init__(
        self, cache_dir: str = "data/cache/exoplanet_eu", use_mock_data: bool = False
    ):  # MODIFIÉ
        super().__init__(cache_dir, use_mock_data)
        # required_columns est maintenant géré par _get_required_columns

    def _get_default_cache_filename(self) -> str:
        return "exoplanet.eu_catalog.csv"

    def _get_download_url(self) -> str:
        return "http://exoplanet.eu/catalog/exoplanet.eu_catalog.csv"

    def _get_source_type(self) -> SourceType:
        return SourceType.EPE

    def _get_source_reference_url(self) -> str:
        return "https://exoplanet.eu/"

    def _get_required_columns(self) -> List[str]:
        return ["name", "star_name", "detection_type", "discovered"]

    def _get_csv_reader_kwargs(self) -> Dict[str, Any]:
        return {"comment": "#"}

    def _convert_row_to_exoplanet(
        self, row: pd.Series, ref: Reference
    ) -> Optional[Exoplanet]:
        try:
            # Validation des données de base
            if pd.isna(row["name"]) or pd.isna(row["star_name"]):
                logger.warning(
                    f"Données de base manquantes pour l'exoplanète : {row.get('name', 'Unknown')} (Source: EPE)"
                )
                return None

            exoplanet = Exoplanet(
                name=str(row["name"]).strip(),
                host_star=DataPoint(str(row["star_name"]).strip(), ref),
                discovery_method=DataPoint(str(row["detection_type"]).strip(), ref)
                if pd.notna(row["detection_type"])
                else None,
                discovery_date=DataPoint(str(row["discovered"]).strip(), ref)
                if pd.notna(row["discovered"])
                else None,
            )

            # Caractéristiques orbitales (utilisation de self._safe_float_conversion de la classe base)
            for field, csv_field in [
                ("semi_major_axis", "semi_major_axis"),
                ("eccentricity", "eccentricity"),
                ("orbital_period", "orbital_period"),
                ("inclination", "inclination"),
                ("argument_of_periastron", "omega"),
                ("periastron_time", "tperi"),
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref))

            # Caractéristiques physiques
            for field, csv_field in [
                ("mass", "mass"),
                ("radius", "radius"),
                ("temperature", "temp_calculated"),
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref))

            # Informations sur l'étoile
            for field, csv_field in [
                ("spectral_type", "star_sp_type"),
                ("star_temperature", "star_teff"),
                ("star_radius", "star_radius"),
                ("star_mass", "star_mass"),
                ("distance", "star_distance"),
                ("apparent_magnitude", "mag_v"),
            ]:
                value = row.get(csv_field)
                if pd.notna(value):
                    # La conversion float est déjà gérée si c'est un nombre, sinon on prend la chaîne
                    processed_value = (
                        self._safe_float_conversion(value)
                        if isinstance(value, (int, float, str))
                        and str(value).replace(".", "", 1).isdigit()
                        else str(value).strip()
                    )
                    if processed_value is not None:  # Peut être une chaîne ou un float
                        setattr(exoplanet, field, DataPoint(processed_value, ref))

            if pd.notna(row.get("planet_status")):
                exoplanet.status = DataPoint(str(row["planet_status"]).strip(), ref)

            if pd.notna(row.get("alternate_names")):
                names = str(row["alternate_names"]).split(",")
                for name in names:
                    name = name.strip()
                    if name and name != exoplanet.name:
                        exoplanet.other_names.append(name)

            return exoplanet

        except Exception as e:
            logger.error(
                f"Erreur EPE lors de la conversion de la ligne : {row.get('name', 'Unknown')}. Erreur: {e}",
                exc_info=True,
            )
            return None

    # fetch_data, _safe_float_conversion, _create_reference sont hérités
