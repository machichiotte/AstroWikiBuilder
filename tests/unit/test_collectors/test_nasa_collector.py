# tests/unit/test_collectors/test_nasa_collector.py
"""
Tests pour NASAExoplanetArchiveCollector.
"""

from unittest.mock import patch
import pandas as pd

from src.collectors.implementations.nasa_exoplanet_archive_collector import (
    NasaExoplanetArchiveCollector,
)
from src.models.references.reference import SourceType


class TestNASAExoplanetArchiveCollector:
    """Tests du collecteur NASA."""

    def test_initialization_with_mock_data(self, mock_cache_dir):
        """Test d'initialisation avec données mockées."""
        collector = NasaExoplanetArchiveCollector(
            use_mock_data=True, custom_cache_filename="test_cache.csv"
        )

        assert collector.use_mock_data is True
        assert "test_cache.csv" in collector.cache_path

    def test_get_source_type(self):
        """Test du type de source."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        assert collector.get_source_type() == SourceType.NEA

    def test_get_data_download_url(self):
        """Test de l'URL de téléchargement."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        url = collector.get_data_download_url()
        assert "exoplanetarchive.ipac.caltech.edu" in url
        assert url.startswith("https://")

    def test_get_source_reference_url(self):
        """Test de l'URL de référence."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        url = collector.get_source_reference_url()
        assert "exoplanetarchive.ipac.caltech.edu" in url

    def test_get_required_csv_columns(self):
        """Test des colonnes requises."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        columns = collector.get_required_csv_columns()
        assert isinstance(columns, list)
        # Vérifier quelques colonnes essentielles
        assert "pl_name" in columns
        assert "hostname" in columns

    @patch("src.collectors.base_collector.pd.read_csv")
    def test_validate_required_columns_success(self, mock_read_csv):
        """Test de validation des colonnes réussie."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        # Mock DataFrame avec toutes les colonnes requises
        mock_df = pd.DataFrame(
            {
                "pl_name": ["Test b"],
                "hostname": ["Test"],
                "pl_bmasse": [1.0],
                "pl_rade": [1.0],
                "discoverymethod": ["Transit"],
                "disc_year": [2020],
            }
        )

        result = collector.validate_required_columns(mock_df)
        assert result is True

    def test_convert_to_float_if_possible(self):
        """Test de conversion en float."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        # Test conversion réussie
        assert collector.convert_to_float_if_possible("1.5") == 1.5
        assert collector.convert_to_float_if_possible(2.5) == 2.5

        # Test valeurs non convertibles
        assert collector.convert_to_float_if_possible(None) is None
        assert collector.convert_to_float_if_possible("invalid") is None
        assert collector.convert_to_float_if_possible(pd.NA) is None

    @patch("src.collectors.base_collector.os.path.exists")
    @patch("src.collectors.base_collector.pd.read_csv")
    def test_load_source_dataframe_with_mock(self, mock_read_csv, mock_exists):
        """Test de chargement avec données mockées."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        mock_exists.return_value = True
        mock_df = pd.DataFrame({"pl_name": ["Test b"], "hostname": ["Test"]})
        mock_read_csv.return_value = mock_df

        df = collector.load_source_dataframe()

        assert df is not None
        assert len(df) == 1
        mock_read_csv.assert_called_once()
