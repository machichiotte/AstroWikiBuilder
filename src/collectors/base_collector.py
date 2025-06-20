# src/data_collectors/base_collector.py
import pandas as pd
import requests
import os
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import logging
from abc import ABC, abstractmethod

from src.models.entities.star import Star
from src.models.entities.exoplanet import Exoplanet
from src.models.references.reference import SourceType
from src.services.processors.reference_manager import ReferenceManager

logger = logging.getLogger(__name__)


class BaseCollector(ABC):
    def __init__(self, cache_dir: str, use_mock_data: bool = False):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.use_mock_data = use_mock_data
        self.reference_manager = ReferenceManager()
        self.last_update_date = datetime.now()
        self.cache_path = os.path.join(
            self.cache_dir, self._get_default_cache_filename()
        )

    @abstractmethod
    def _get_default_cache_filename(self) -> str:
        """Nom de fichier par défaut pour le cache de cette source."""
        pass

    @abstractmethod
    def _get_download_url(self) -> str:
        """URL de téléchargement des données pour cette source."""
        pass

    @abstractmethod
    def _get_source_type(self) -> SourceType:
        """Type de source (Enum) pour la référence."""
        pass

    @abstractmethod
    def _get_source_reference_url(self) -> str:
        """URL de référence principale de la source."""
        pass

    @abstractmethod
    def _get_required_columns(self) -> List[str]:
        """Liste des colonnes CSV requises pour cette source."""
        return []  # Optionnel, retournera une liste vide si non surchargé

    @abstractmethod
    def _convert_row_to_exoplanet(self, row: pd.Series) -> Optional[Exoplanet]:
        """Convertit une ligne du DataFrame en objet Exoplanet."""
        pass

    @abstractmethod
    def _convert_row_to_star(self, row: pd.Series) -> Optional[Star]:
        """Convertit une ligne du DataFrame en objet Star."""
        pass

    def _read_csv_from_path(self, file_path: str) -> Optional[pd.DataFrame]:
        try:
            return pd.read_csv(file_path, **self._get_csv_reader_kwargs())
        except FileNotFoundError:
            logger.warning(f"Fichier non trouvé : {file_path}")
        except pd.errors.EmptyDataError:
            logger.error(f"Fichier vide : {file_path}")
        except Exception as e:
            logger.error(f"Erreur lecture CSV {file_path}: {e}")
        return None

    def _download_data_to_cache_and_parse_csv(self) -> Optional[pd.DataFrame]:
        url = self._get_download_url()
        logger.info(f"Téléchargement depuis {url}")

        try:
            response: requests.Response = requests.get(url, timeout=10)
            response.raise_for_status()

            with open(self.cache_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            return self._read_csv_from_path(self.cache_path)
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur HTTP depuis {url}: {e}")
        except Exception as e:
            logger.error(f"Erreur d'écriture du cache {self.cache_path}: {e}")

        return None

    def collect_exoplanets_and_stars_from_source(
        self,
    ) -> Tuple[List[Exoplanet], List[Star]]:
        df: Optional[pd.DataFrame] = self._load_data()
        if df is None:
            logger.error("Chargement des données impossible.")
            return [], []

        if not self._validate_columns(df):
            return [], []

        return self._parse_entities_from_dataframe(df)

    def _get_csv_reader_kwargs(self) -> Dict[str, Any]:
        """Arguments optionnels pour pd.read_csv (ex: comment char)."""
        return {}  # Par défaut, aucun argument spécial

    def _safe_float_conversion(self, value: any) -> Optional[float]:
        if pd.isna(value):
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def _load_data(self) -> Optional[pd.DataFrame]:
        if self.use_mock_data:
            logger.info("Chargement depuis les données mockées.")
            if os.path.exists(self.cache_path):
                df = self._read_csv_from_path(self.cache_path)
                if df is not None:
                    logger.info(
                        f"Fichier mock chargé: {self.cache_path} ({len(df)} lignes)"
                    )
                else:
                    logger.warning(
                        f"Fichier mock vide ou non lisible: {self.cache_path}"
                    )
                return df
            else:
                logger.error(f"Fichier mock introuvable: {self.cache_path}")
                return None

        if os.path.exists(self.cache_path):
            df: Optional[pd.DataFrame] = self._read_csv_from_path(self.cache_path)
            if df is not None:
                return df
            logger.warning("Échec lecture cache, tentative de téléchargement.")

        df = self._download_data_to_cache_and_parse_csv()
        if df is None and os.path.exists(self.cache_path):
            logger.info("Relecture du cache après échec du téléchargement.")
            return self._read_csv_from_path(self.cache_path)

        return df

    def _validate_columns(self, df: pd.DataFrame) -> bool:
        required: List[str] = self._get_required_columns()
        missing: List[str] = [col for col in required if col not in df.columns]
        if missing:
            logger.error(f"Colonnes manquantes : {missing} (dans {self.cache_path})")
            return False
        return True

    def _parse_entities_from_dataframe(
        self, df: pd.DataFrame
    ) -> Tuple[List[Exoplanet], List[Star]]:
        exoplanets: List[Exoplanet] = []
        stars: List[Star] = []

        for idx, row in df.iterrows():
            try:
                exo: Optional[Exoplanet] = self._convert_row_to_exoplanet(row)
                if exo:
                    exoplanets.append(exo)

                star: Optional[Star] = self._convert_row_to_star(row)
                if star:
                    stars.append(star)
            except Exception as e:
                logger.exception(
                    f"Erreur conversion ligne {idx} ({self._get_source_type().name}): {e}"
                )

        logger.info(f"{len(exoplanets)} exoplanètes et {len(stars)} étoiles extraites.")
        return exoplanets, stars
