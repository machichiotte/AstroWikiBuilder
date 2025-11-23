# tests/unit/test_collectors/test_exoplanet_eu_collector.py
"""
Tests pour ExoplanetEUCollector.
"""

from unittest.mock import patch

import pandas as pd

from src.collectors.implementations.exoplanet_eu_collector import ExoplanetEUCollector
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

    @patch(
        "src.services.processors.reference_manager.ReferenceManager.create_reference"
    )
    def test_transform_row_to_exoplanet_with_complete_data(self, mock_create_ref):
        """Test de transformation avec données complètes."""
        from unittest.mock import Mock

        # Mock de la référence
        mock_ref = Mock()
        mock_create_ref.return_value = mock_ref

        collector = ExoplanetEUCollector(use_mock_data=True)

        mock_row = pd.Series(
            {
                "name": "51 Peg b",
                "star_name": "51 Peg",
                "semi_major_axis": 0.0527,
                "eccentricity": 0.013,
                "orbital_period": 4.230785,
                "inclination": 79.0,
                "argument_of_periastron": 58.0,
                "periastron_time": 2450001.5,
                "mass": 0.468,
                "radius": 1.9,
                "temperature": 1284,
                "spectral_type": "G5V",
                "star_temperature": 5793,
                "star_radius": 1.237,
                "star_mass": 1.11,
                "distance": 15.6,
                "apparent_magnitude": 5.49,
                "alt_names": "HD 217014 b, HIP 113357 b",
            }
        )

        exoplanet = collector.transform_row_to_exoplanet(mock_row)

        assert exoplanet is not None
        assert exoplanet.pl_name == "51 Peg b"
        assert exoplanet.st_name == "51 Peg"
        assert len(exoplanet.pl_altname) == 2

    @patch(
        "src.services.processors.reference_manager.ReferenceManager.create_reference"
    )
    def test_transform_row_to_exoplanet_with_partial_data(self, mock_create_ref):
        """Test de transformation avec données partielles."""
        from unittest.mock import Mock

        mock_create_ref.return_value = Mock()

        collector = ExoplanetEUCollector(use_mock_data=True)

        mock_row = pd.Series(
            {
                "name": "Test b",
                "star_name": "Test",
                "mass": 1.5,
                "radius": pd.NA,
                "temperature": None,
                "spectral_type": "G2V",
            }
        )

        exoplanet = collector.transform_row_to_exoplanet(mock_row)

        assert exoplanet is not None
        assert exoplanet.pl_name == "Test b"

    def test_transform_row_to_exoplanet_missing_required_data(self):
        """Test de transformation avec données requises manquantes."""
        collector = ExoplanetEUCollector(use_mock_data=True)

        # Nom manquant
        mock_row = pd.Series({"name": pd.NA, "star_name": "Test"})
        result = collector.transform_row_to_exoplanet(mock_row)
        assert result is None

        # Nom d'étoile manquant
        mock_row = pd.Series({"name": "Test b", "star_name": pd.NA})
        result = collector.transform_row_to_exoplanet(mock_row)
        assert result is None

    @patch(
        "src.services.processors.reference_manager.ReferenceManager.create_reference"
    )
    def test_transform_row_to_exoplanet_with_numeric_string_values(
        self, mock_create_ref
    ):
        """Test de transformation avec valeurs numériques en string."""
        from unittest.mock import Mock

        mock_create_ref.return_value = Mock()

        collector = ExoplanetEUCollector(use_mock_data=True)

        mock_row = pd.Series(
            {
                "name": "Test b",
                "star_name": "Test",
                "mass": "1.5",
                "radius": "2.0",
                "star_temperature": "5778",
                "distance": "10.5",
            }
        )

        exoplanet = collector.transform_row_to_exoplanet(mock_row)

        assert exoplanet is not None

    @patch(
        "src.services.processors.reference_manager.ReferenceManager.create_reference"
    )
    def test_transform_row_to_exoplanet_with_alt_names(self, mock_create_ref):
        """Test de transformation avec noms alternatifs."""
        from unittest.mock import Mock

        mock_create_ref.return_value = Mock()

        collector = ExoplanetEUCollector(use_mock_data=True)

        mock_row = pd.Series(
            {
                "name": "Test b",
                "star_name": "Test",
                "alt_names": "HD 123 b, HIP 456 b, Test b",  # Test b doit être filtré
            }
        )

        exoplanet = collector.transform_row_to_exoplanet(mock_row)

        assert exoplanet is not None
        assert len(exoplanet.pl_altname) == 2  # Test b est filtré
        assert "HD 123 b" in exoplanet.pl_altname
        assert "HIP 456 b" in exoplanet.pl_altname
        assert "Test b" not in exoplanet.pl_altname

    def test_transform_row_to_exoplanet_with_exception(self):
        """Test de gestion d'exception lors de la transformation."""
        collector = ExoplanetEUCollector(use_mock_data=True)

        # Créer une row qui va causer une exception
        mock_row = pd.Series({"name": "Test b", "star_name": "Test"})

        # Simuler une exception dans reference_manager
        with patch.object(
            collector.reference_manager,
            "create_reference",
            side_effect=Exception("Test error"),
        ):
            result = collector.transform_row_to_exoplanet(mock_row)
            assert result is None
