# src/data_collectors/nasa_exoplanet_archive_collector.py
import pandas as pd
from typing import List, Optional, Dict, Any
import logging
from src.models.data_source_star import DataSourceStar
from src.mappers.nasa_exoplanet_archive_mapper import NasaExoplanetArchiveMapper
from src.collectors.base_collector import BaseCollector
from src.models.data_source_exoplanet import DataSourceExoplanet

from src.models.reference import Reference, SourceType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NASAExoplanetArchiveCollector(BaseCollector):
    def __init__(
        self,
        cache_dir: str = "data/cache/nasa_exoplanet_archive",
        use_mock_data: bool = False,
    ):
        super().__init__(cache_dir, use_mock_data)
        self.mapper = NasaExoplanetArchiveMapper()

    def _get_default_cache_filename(self) -> str:
        # return "nea_mock_data_complete.csv"
        return "nea_mock_data.csv"

    def _get_download_url(self) -> str:
        return "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+PSCompPars&format=csv"

    def _get_source_type(self) -> SourceType:
        return SourceType.NEA

    def _get_source_reference_url(self) -> str:
        return "https://exoplanetarchive.ipac.caltech.edu/"

    def _get_required_columns(self) -> List[str]:
        return ["pl_name", "hostname", "discoverymethod", "disc_year"]

    def _get_csv_reader_kwargs(self) -> Dict[str, Any]:
        # Le fichier téléchargé de NEA n'a pas de lignes de commentaire typiques à ignorer avec '#' au début.
        # Si le fichier que vous sauvegardez/mockez en a, ajustez ici.
        return {}

    def _convert_row_to_exoplanet(
        self, row: pd.Series, ref: Reference
    ) -> Optional[DataSourceExoplanet]:
        """
        Converts a pandas Series (row from a CSV/DataFrame) to a Star object,
        populating it with data based on predefined mappings.
        """
        try:
            nea_data_dict = row.to_dict()
            # S'assurer que les données essentielles sont présentes avant d'appeler le mapper.
            if not nea_data_dict.get("pl_name"):
                logger.warning(
                    f"Exoplanet name (pl_name) is missing or empty for a row. Skipping exoplanet creation. Row data: {nea_data_dict}"
                )
                return None

            # Déléguer toute la logique de mappage et de création de l'objet au mapper.
            exoplanet = self.mapper.map_nea_data_to_exoplanet(nea_data_dict)
            return exoplanet
        except Exception as e:
            logger.error(
                f"Unexpected error converting row to Exoplanet using mapper for {row.get('pl_name', 'Unknown')}: {e}",
                exc_info=True,
            )
            return None

    def _convert_row_to_star(
        self, row: pd.Series, ref: Reference
    ) -> Optional[DataSourceStar]:
        """
        Converts a pandas Series (row from a CSV/DataFrame) to a Star object,
        populating it with data based on predefined mappings.
        """
        try:
            nea_data_dict = row.to_dict()
            # S'assurer que les données essentielles sont présentes avant d'appeler le mapper.
            if not nea_data_dict.get("hostname"):
                logger.warning(
                    f"Star name (hostname) is missing or empty for a row. Skipping star creation. Row data: {nea_data_dict}"
                )
                return None

            # Déléguer toute la logique de mappage et de création de l'objet au mapper.
            star = self.mapper.map_nea_data_to_star(nea_data_dict)
            return star
        except Exception as e:
            logger.error(
                f"Unexpected error converting row to Star using mapper for {row.get('hostname', 'Unknown')}: {e}",
                exc_info=True,
            )
            return None
