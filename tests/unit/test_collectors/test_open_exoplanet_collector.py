# tests/unit/test_collectors/test_open_exoplanet_collector.py
"""
Tests pour OpenExoplanetCollector.
"""

from unittest.mock import patch
import pandas as pd

from src.collectors.implementations.open_exoplanet_collection import (
    OpenExoplanetCollector,
)
from src.models.references.reference import SourceType


class TestOpenExoplanetCollector:
    """Tests du collecteur Open Exoplanet Catalogue."""

    def test_initialization_with_mock_data(self):
        """Test d'initialisation avec données mockées."""
        collector = OpenExoplanetCollector(use_mock_data=True)

        assert collector.use_mock_data is True

    def test_get_source_type(self):
        """Test du type de source."""
        collector = OpenExoplanetCollector(use_mock_data=True)

        assert collector.get_source_type() == SourceType.OEC

    def test_get_data_download_url(self):
        """Test de l'URL de téléchargement."""
        collector = OpenExoplanetCollector(use_mock_data=True)

        url = collector.get_data_download_url()
        assert "github.com" in url
        assert "OpenExoplanetCatalogue" in url

    def test_get_source_reference_url(self):
        """Test de l'URL de référence."""
        collector = OpenExoplanetCollector(use_mock_data=True)

        url = collector.get_source_reference_url()
        assert "github.com" in url

    def test_get_required_csv_columns(self):
        """Test des colonnes requises."""
        collector = OpenExoplanetCollector(use_mock_data=True)

        columns = collector.get_required_csv_columns()
        assert isinstance(columns, list)
        # Vérifier quelques colonnes essentielles
        assert "name" in columns
        assert "star_name" in columns

    @patch("src.collectors.base_collector.pd.read_csv")
    def test_validate_required_columns_success(self, mock_read_csv):
        """Test de validation des colonnes réussie."""
        collector = OpenExoplanetCollector(use_mock_data=True)

        # Mock DataFrame avec toutes les colonnes requises
        mock_df = pd.DataFrame(
            {
                "name": ["Kepler-1032 b"],
                "star_name": ["Kepler-1032"],
            }
        )

        result = collector.validate_required_columns(mock_df)
        assert result is True

    def test_convert_to_float_if_possible(self):
        """Test de conversion en float."""
        collector = OpenExoplanetCollector(use_mock_data=True)

        # Test conversion réussie
        assert collector.convert_to_float_if_possible("1.5") == 1.5
        assert collector.convert_to_float_if_possible(2.5) == 2.5

        # Test valeurs non convertibles
        assert collector.convert_to_float_if_possible(None) is None
        assert collector.convert_to_float_if_possible("invalid") is None
        assert collector.convert_to_float_if_possible(pd.NA) is None

    def test_transform_row_to_star_returns_none(self):
        """Test que transform_row_to_star retourne None."""
        collector = OpenExoplanetCollector(use_mock_data=True)

        mock_row = pd.Series({"name": "Test b", "star_name": "Test"})
        result = collector.transform_row_to_star(mock_row)

        assert result is None
