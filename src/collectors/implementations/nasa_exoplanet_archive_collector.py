# src/collectors/implementations/nasa_exoplanet_archive_collector.py
import pandas as pd
from typing import List, Optional, Dict, Any
import logging
from src.core.config import CACHE_PATHS
from src.models.entities.star import Star
from src.mappers.nasa_exoplanet_archive_mapper import NasaExoplanetArchiveMapper
from src.collectors.base_collector import BaseCollector
from src.models.entities.exoplanet import Exoplanet

from src.models.references.reference import SourceType

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class NasaExoplanetArchiveCollector(BaseCollector):
    BASE_NEARCHIVE_URL = "https://exoplanetarchive.ipac.caltech.edu"
    NEARCHIVE_CSV_ENDPOINT = (
        f"{BASE_NEARCHIVE_URL}/TAP/sync?query=select+*+from+PSCompPars&format=csv"
    )

    def __init__(
        self,
        cache_dir: str = "data",
        use_mock_data: bool = False,
        custom_cache_filename: Optional[str] = None,
    ):
        self._custom_cache_filename = custom_cache_filename

        super().__init__(cache_dir, use_mock_data)
        self.mapper = NasaExoplanetArchiveMapper()

    def _get_default_cache_filename(self) -> str:
        if self._custom_cache_filename:
            return self._custom_cache_filename
        mode = "mock" if self.use_mock_data else "real"
        return CACHE_PATHS["nasa_exoplanet_archive"][mode]

    def _get_download_url(self) -> str:
        return self.NEARCHIVE_CSV_ENDPOINT

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

    def _map_row_to_exoplanet(self, row: pd.Series) -> Optional[Exoplanet]:
        """
        Converts a pandas Series (row from a CSV/DataFrame) to an Exoplanet object,
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
            exoplanet: Exoplanet = self.mapper.map_exoplanet_from_nea_record(
                nea_data_dict
            )
            return exoplanet
        except Exception as e:
            logger.error(
                f"Unexpected error converting row to Exoplanet using mapper for {row.get('pl_name', 'Unknown')}: {e}",
                exc_info=True,
            )
            return None

    def _map_row_to_star(self, row: pd.Series) -> Optional[Star]:
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
            star: Star = self.mapper.map_star_from_nea_record(nea_data_dict)
            return star
        except Exception as e:
            logger.error(
                f"Unexpected error converting row to Star using mapper for {row.get('hostname', 'Unknown')}: {e}",
                exc_info=True,
            )
            return None
