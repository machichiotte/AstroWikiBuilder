# tests/unit/test_collectors/test_nasa_exoplanet_archive_collector.py
"""
Tests pour NasaExoplanetArchiveCollector.
"""

from unittest.mock import patch

import pandas as pd

from src.collectors.implementations.nasa_exoplanet_archive_collector import (
    NasaExoplanetArchiveCollector,
)
from src.models.references.reference import SourceType


class TestNasaExoplanetArchiveCollector:
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

    def test_transform_row_to_exoplanet_success(self):
        """Test de transformation réussie d'une ligne en Exoplanet."""
        from src.models.entities.exoplanet_entity import Exoplanet

        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        # Créer une ligne de données valide
        row = pd.Series(
            {
                "pl_name": "Kepler-186 f",
                "hostname": "Kepler-186",
                "discoverymethod": "Transit",
                "disc_year": 2014,
                "pl_orbper": 129.9,
                "pl_rade": 1.17,
            }
        )

        # Mocker le mapper pour retourner un objet Exoplanet valide
        mock_exoplanet = Exoplanet(pl_name="Kepler-186 f", st_name="Kepler-186")
        with patch.object(
            collector.mapper,
            "map_exoplanet_from_nea_record",
            return_value=mock_exoplanet,
        ):
            result = collector.transform_row_to_exoplanet(row)

            assert result is not None
            assert result.pl_name == "Kepler-186 f"
            assert result.st_name == "Kepler-186"

    def test_transform_row_to_exoplanet_missing_name(self):
        """Test de transformation avec nom manquant."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        # Créer une ligne sans pl_name
        row = pd.Series(
            {
                "pl_name": None,
                "hostname": "Kepler-186",
                "discoverymethod": "Transit",
                "disc_year": 2014,
            }
        )

        result = collector.transform_row_to_exoplanet(row)

        assert result is None

    def test_transform_row_to_exoplanet_empty_name(self):
        """Test de transformation avec nom vide."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        # Créer une ligne avec pl_name vide
        row = pd.Series(
            {
                "pl_name": "",
                "hostname": "Kepler-186",
                "discoverymethod": "Transit",
                "disc_year": 2014,
            }
        )

        result = collector.transform_row_to_exoplanet(row)

        assert result is None

    def test_transform_row_to_exoplanet_mapper_exception(self):
        """Test de gestion d'exception du mapper."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        row = pd.Series(
            {
                "pl_name": "Test b",
                "hostname": "Test",
                "discoverymethod": "Transit",
                "disc_year": 2014,
            }
        )

        # Simuler une exception dans le mapper
        with patch.object(
            collector.mapper,
            "map_exoplanet_from_nea_record",
            side_effect=Exception("Mapper error"),
        ):
            result = collector.transform_row_to_exoplanet(row)
            assert result is None

    def test_transform_row_to_star_success(self):
        """Test de transformation réussie d'une ligne en Star."""
        from src.models.entities.star_entity import Star

        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        # Créer une ligne de données valide
        row = pd.Series(
            {
                "hostname": "Kepler-186",
                "st_teff": 3755,
                "st_rad": 0.47,
                "st_mass": 0.48,
            }
        )

        # Mocker le mapper pour retourner un objet Star valide
        mock_star = Star(st_name="Kepler-186")
        with patch.object(
            collector.mapper,
            "map_star_from_nea_record",
            return_value=mock_star,
        ):
            result = collector.transform_row_to_star(row)

            assert result is not None
            assert result.st_name == "Kepler-186"

    def test_transform_row_to_star_missing_hostname(self):
        """Test de transformation avec hostname manquant."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        # Créer une ligne sans hostname
        row = pd.Series(
            {
                "hostname": None,
                "st_teff": 3755,
                "st_rad": 0.47,
            }
        )

        result = collector.transform_row_to_star(row)

        assert result is None

    def test_transform_row_to_star_empty_hostname(self):
        """Test de transformation avec hostname vide."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        # Créer une ligne avec hostname vide
        row = pd.Series(
            {
                "hostname": "",
                "st_teff": 3755,
                "st_rad": 0.47,
            }
        )

        result = collector.transform_row_to_star(row)

        assert result is None

    def test_transform_row_to_star_mapper_exception(self):
        """Test de gestion d'exception du mapper pour Star."""
        collector = NasaExoplanetArchiveCollector(use_mock_data=True)

        row = pd.Series(
            {
                "hostname": "Test",
                "st_teff": 3755,
                "st_rad": 0.47,
            }
        )

        # Simuler une exception dans le mapper
        with patch.object(
            collector.mapper,
            "map_star_from_nea_record",
            side_effect=Exception("Mapper error"),
        ):
            result = collector.transform_row_to_star(row)
            assert result is None
