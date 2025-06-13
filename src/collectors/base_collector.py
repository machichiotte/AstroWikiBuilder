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
from src.models.references.reference import Reference, SourceType
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
    def _convert_row_to_exoplanet(
        self, row: pd.Series, ref: Reference
    ) -> Optional[Exoplanet]:
        """Convertit une ligne du DataFrame en objet Exoplanet."""
        pass

    @abstractmethod
    def _convert_row_to_star(self, row: pd.Series, ref: Reference) -> Optional[Star]:
        """Convertit une ligne du DataFrame en objet Star."""
        pass

    def _read_csv_from_path(self, file_path: str) -> Optional[pd.DataFrame]:
        try:
            return pd.read_csv(file_path, **self._get_csv_reader_kwargs())
        except FileNotFoundError:
            logger.warning(f"Fichier non trouvé : {file_path}")
        except pd.errors.EmptyDataError:
            logger.error(
                f"Aucune donnée trouvée dans le fichier : {file_path}. Le fichier est vide."
            )
        except Exception as e:
            logger.error(
                f"Une erreur est survenue lors de la lecture du fichier {file_path}: {e}"
            )
        return None

    def _download_and_save_data(self) -> Optional[pd.DataFrame]:
        download_url = self._get_download_url()
        logger.info(f"Téléchargement des données depuis {download_url}")
        try:
            response = requests.get(download_url)
            response.raise_for_status()

            with open(self.cache_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            logger.info(
                f"Données téléchargées et sauvegardées avec succès dans {self.cache_path}"
            )
            return self._read_csv_from_path(self.cache_path)
        except requests.exceptions.RequestException as e:
            logger.error(
                f"Erreur lors du téléchargement des données depuis {download_url}: {e}"
            )
        except Exception as e:
            logger.error(
                f"Une erreur est survenue lors du traitement des données téléchargées depuis {self.cache_path}: {e}"
            )
        return None

    def fetch_data(self) -> Tuple[List[Exoplanet], List[Star]]:
        exoplanets: List[Exoplanet] = []
        stars: List[Star] = []
        df = None

        if self.use_mock_data:
            logger.info(
                f"Utilisation des données mockées/cache depuis {self.cache_path}"
            )
            if not os.path.exists(self.cache_path):
                logger.warning(f"Fichier mock/cache non trouvé : {self.cache_path}")
                return [], []
            df = self._read_csv_from_path(self.cache_path)
        else:
            logger.info(
                "Tentative de chargement des données depuis le cache ou téléchargement."
            )
            if os.path.exists(self.cache_path):
                logger.info("Fichier cache trouvé. Chargement des données.")
                df = self._read_csv_from_path(self.cache_path)
                if df is None:
                    logger.warning(
                        "Échec de la lecture du cache. Tentative de téléchargement."
                    )
            if df is None:
                df = self._download_and_save_data()
                if df is None and os.path.exists(self.cache_path):
                    logger.info(
                        "Échec du téléchargement. Rechargement du cache existant."
                    )
                    df = self._read_csv_from_path(self.cache_path)

        if df is not None:
            required_cols = self._get_required_columns()
            if required_cols:
                missing_columns = [
                    col for col in required_cols if col not in df.columns
                ]
                if missing_columns:
                    logger.error(
                        f"Colonnes manquantes : {missing_columns} (source: {self.cache_path})"
                    )
                    return [], []

            ref = self._create_reference()
            for _, row in df.iterrows():
                try:
                    exoplanet = self._convert_row_to_exoplanet(row, ref)
                    if exoplanet:
                        exoplanets.append(exoplanet)

                    star = self._convert_row_to_star(row, ref)
                    if star:
                        stars.append(star)

                except Exception as e:
                    logger.error(
                        f"Erreur de conversion pour {self._get_source_type().name}: {e}",
                        exc_info=True,
                    )

            logger.info(
                f"{len(exoplanets)} exoplanètes et {len(stars)} étoiles traitées avec succès."
            )
        else:
            logger.error("Impossible de charger ou télécharger les données.")

        return exoplanets, stars

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

    def _create_reference(self) -> Reference:
        return self.reference_manager.create_reference(
            source=self._get_source_type(),
            update_date=self.last_update_date,
        )
