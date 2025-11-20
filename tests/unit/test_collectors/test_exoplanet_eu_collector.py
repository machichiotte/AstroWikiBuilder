# tests/unit/test_collectors/test_exoplanet_eu_collector.py
"""
Tests pour ExoplanetEUCollector.
"""

from unittest.mock import patch

import pandas as pd

from src.collectors.implementations.exoplanet_eu import ExoplanetEUCollector
from src.models.references.reference import SourceType


class TestExoplanetEUCollector:
    """Tests du collecteur Exoplanet.eu."""

    def test_initialization_with_mock_data(self):
        """Test d'initialisation avec données mockées."""
        collector = ExoplanetEUCollector(use_mock_data=True)

        assert collector.use_mock_data is True

    def test_get_source_type(self):
        """Test du type de source."""
        collector = ExoplanetEUCollector(use_mock_data=True)

        assert collector.get_source_type() == SourceType.EPE

    def test_get_data_download_url(self):
        """Test de l'URL de téléchargement."""
        collector = ExoplanetEUCollector(use_mock_data=True)

        url = collector.get_data_download_url()
        assert "exoplanet.eu" in url
        assert url.startswith("http://")

    def test_get_source_reference_url(self):
        """Test de l'URL de référence."""
        collector = ExoplanetEUCollector(use_mock_data=True)

        url = collector.get_source_reference_url()
        assert "exoplanet.eu" in url

    def test_get_required_csv_columns(self):
        """Test des colonnes requises."""
        collector = ExoplanetEUCollector(use_mock_data=True)

        columns = collector.get_required_csv_columns()
        assert isinstance(columns, list)
        # Vérifier quelques colonnes essentielles
        assert "name" in columns
        assert "star_name" in columns

    def test_get_csv_reader_options(self):
        """Test des options CSV."""
        collector = ExoplanetEUCollector(use_mock_data=True)

        options = collector.get_csv_reader_options()
        assert isinstance(options, dict)
        assert "comment" in options

    @patch("src.collectors.base_collector.pd.read_csv")
    def test_validate_required_columns_success(self, mock_read_csv):
        """Test de validation des colonnes réussie."""
        collector = ExoplanetEUCollector(use_mock_data=True)

        # Mock DataFrame avec toutes les colonnes requises
        mock_df = pd.DataFrame(
            {
                "name": ["109 Psc b"],
                "star_name": ["109 Psc"],
                "discovery_method": ["Radial Velocity"],
                "discovery_year": [2000],
            }
        )

        result = collector.validate_required_columns(mock_df)
        assert result is True

    def test_convert_to_float_if_possible(self):
        """Test de conversion en float."""
        collector = ExoplanetEUCollector(use_mock_data=True)

        # Test conversion réussie
        assert collector.convert_to_float_if_possible("1.5") == 1.5
        assert collector.convert_to_float_if_possible(2.5) == 2.5

        # Test valeurs non convertibles
        assert collector.convert_to_float_if_possible(None) is None
        assert collector.convert_to_float_if_possible("invalid") is None
        assert collector.convert_to_float_if_possible(pd.NA) is None

    def test_transform_row_to_star_returns_none(self):
        """Test que transform_row_to_star retourne None."""
        collector = ExoplanetEUCollector(use_mock_data=True)

        mock_row = pd.Series({"name": "Test b", "star_name": "Test"})
        result = collector.transform_row_to_star(mock_row)

        assert result is None
