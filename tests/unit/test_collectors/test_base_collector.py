"""Tests pour BaseCollector."""

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest
import requests

from src.collectors.base_collector import BaseCollector
from src.models.entities.exoplanet_entity import Exoplanet
from src.models.entities.star_entity import Star
from src.models.references.reference import SourceType


class ConcreteCollector(BaseCollector):
    """Implémentation concrète pour les tests."""

    def get_default_cache_filename(self) -> str:
        return "test_cache.csv"

    def get_data_download_url(self) -> str:
        return "https://example.com/data.csv"

    def get_source_type(self) -> SourceType:
        return SourceType.NEA

    def get_source_reference_url(self) -> str:
        return "https://example.com"

    def get_required_csv_columns(self) -> list[str]:
        return ["name", "mass"]

    def transform_row_to_exoplanet(self, row: pd.Series) -> Exoplanet | None:
        name = row.get("name")
        if pd.isna(name):
            return None

        # Créer un objet Exoplanet avec les champs minimaux requis
        return Exoplanet(pl_name=str(name), st_name=str(row.get("hostname", "Unknown")))

    def transform_row_to_star(self, row: pd.Series) -> Star | None:
        hostname = row.get("hostname")
        if pd.isna(hostname):
            return None

        return Star(st_name=str(hostname))


class TestBaseCollector:
    """Tests pour BaseCollector."""

    @pytest.fixture
    def temp_cache_dir(self, tmp_path):
        """Fixture pour créer un répertoire de cache temporaire."""
        cache_dir = tmp_path / "cache"
        cache_dir.mkdir()
        return str(cache_dir)

    @pytest.fixture
    def collector(self, temp_cache_dir):
        """Fixture pour créer un collector."""
        return ConcreteCollector(cache_dir=temp_cache_dir, use_mock_data=False)

    def test_init_creates_cache_dir(self, tmp_path):
        """Test que l'initialisation crée le répertoire de cache."""
        cache_dir = str(tmp_path / "new_cache")
        collector = ConcreteCollector(cache_dir=cache_dir)

        assert os.path.exists(cache_dir)
        assert collector.cache_dir == cache_dir
        assert collector.use_mock_data is False

    def test_init_with_mock_data(self, temp_cache_dir):
        """Test de l'initialisation avec mock_data."""
        collector = ConcreteCollector(cache_dir=temp_cache_dir, use_mock_data=True)
        assert collector.use_mock_data is True

    def test_get_csv_reader_options_default(self, collector):
        """Test des options par défaut pour read_csv."""
        options = collector.get_csv_reader_options()
        assert options == {}

    def test_convert_to_float_if_possible_valid_float(self, collector):
        """Test de conversion d'un float valide."""
        assert collector.convert_to_float_if_possible(3.14) == 3.14

    def test_convert_to_float_if_possible_valid_string(self, collector):
        """Test de conversion d'une chaîne valide."""
        assert collector.convert_to_float_if_possible("42.5") == 42.5

    def test_convert_to_float_if_possible_nan(self, collector):
        """Test de conversion d'un NaN."""
        assert collector.convert_to_float_if_possible(pd.NA) is None

    def test_convert_to_float_if_possible_invalid(self, collector):
        """Test de conversion d'une valeur invalide."""
        assert collector.convert_to_float_if_possible("invalid") is None

    def test_validate_required_columns_success(self, collector):
        """Test de validation avec toutes les colonnes requises."""
        df = pd.DataFrame({"name": ["test"], "mass": [1.0]})
        assert collector.validate_required_columns(df) is True

    def test_validate_required_columns_missing(self, collector):
        """Test de validation avec des colonnes manquantes."""
        df = pd.DataFrame({"name": ["test"]})
        assert collector.validate_required_columns(df) is False

    def test_read_csv_file_success(self, collector, temp_cache_dir):
        """Test de lecture réussie d'un fichier CSV."""
        csv_path = os.path.join(temp_cache_dir, "test.csv")
        df = pd.DataFrame({"name": ["test"], "mass": [1.0]})
        df.to_csv(csv_path, index=False)

        result = collector.read_csv_file(csv_path)

        assert result is not None
        assert len(result) == 1
        assert "name" in result.columns

    def test_read_csv_file_not_found(self, collector):
        """Test de lecture d'un fichier inexistant."""
        result = collector.read_csv_file("nonexistent.csv")
        assert result is None

    def test_read_csv_file_empty(self, collector, temp_cache_dir):
        """Test de lecture d'un fichier vide."""
        csv_path = os.path.join(temp_cache_dir, "empty.csv")
        Path(csv_path).touch()

        result = collector.read_csv_file(csv_path)
        assert result is None

    @patch("requests.get")
    def test_fetch_and_cache_csv_data_success(self, mock_get, collector):
        """Test de téléchargement et mise en cache réussis."""
        mock_response = Mock()
        mock_response.text = "name,mass\ntest,1.0"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = collector.fetch_and_cache_csv_data()

        assert result is not None
        assert len(result) == 1
        assert os.path.exists(collector.cache_path)

    @patch("requests.get")
    def test_fetch_and_cache_csv_data_http_error(self, mock_get, collector):
        """Test de gestion d'erreur HTTP."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        result = collector.fetch_and_cache_csv_data()

        assert result is None

    def test_load_source_dataframe_with_mock_data(self, collector, temp_cache_dir):
        """Test de chargement avec mock_data."""
        collector.use_mock_data = True
        csv_path = collector.cache_path
        df = pd.DataFrame({"name": ["test"], "mass": [1.0]})
        df.to_csv(csv_path, index=False)

        result = collector.load_source_dataframe()

        assert result is not None
        assert len(result) == 1

    def test_load_source_dataframe_mock_file_not_found(self, collector):
        """Test de chargement avec mock_data mais fichier inexistant."""
        collector.use_mock_data = True

        result = collector.load_source_dataframe()

        assert result is None

    @patch("requests.get")
    def test_load_source_dataframe_download_on_cache_miss(self, mock_get, collector):
        """Test de téléchargement en cas de cache manquant."""
        mock_response = Mock()
        mock_response.text = "name,mass\ntest,1.0"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = collector.load_source_dataframe()

        assert result is not None
        assert len(result) == 1

    def test_load_source_dataframe_use_existing_cache(self, collector, temp_cache_dir):
        """Test d'utilisation du cache existant."""
        csv_path = collector.cache_path
        df = pd.DataFrame({"name": ["test"], "mass": [1.0]})
        df.to_csv(csv_path, index=False)

        result = collector.load_source_dataframe()

        assert result is not None
        assert len(result) == 1

    def test_extract_entities_from_dataframe_success(self, collector):
        """Test d'extraction d'entités réussie."""
        df = pd.DataFrame(
            {"name": ["Planet1", "Planet2"], "hostname": ["Star1", "Star2"], "mass": [1.0, 2.0]}
        )

        exoplanets, stars = collector.extract_entities_from_dataframe(df)

        assert len(exoplanets) == 2
        assert len(stars) == 2
        assert exoplanets[0].pl_name == "Planet1"
        assert stars[0].st_name == "Star1"

    def test_collect_entities_from_source_no_data(self, collector):
        """Test de collecte sans données disponibles."""
        exoplanets, stars = collector.collect_entities_from_source()

        assert exoplanets == []
        assert stars == []
