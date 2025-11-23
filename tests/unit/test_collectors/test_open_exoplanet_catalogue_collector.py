# tests/unit/test_collectors/test_open_exoplanet_catalogue_collector.py
"""
Tests pour OpenExoplanetCatalogueCollector.
"""

from unittest.mock import patch

import pandas as pd

from src.collectors.implementations.open_exoplanet_catalogue_collector import (
    OpenExoplanetCatalogueCollector,
)
from src.models.references.reference import SourceType


class TestOpenExoplanetCatalogueCollector:
    """Tests du collecteur Open Exoplanet Catalogue."""

    def test_initialization_with_mock_data(self):
        """Test d'initialisation avec données mockées."""
        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        assert collector.use_mock_data is True

    def test_get_source_type(self):
        """Test du type de source."""
        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        assert collector.get_source_type() == SourceType.OEC

    def test_get_data_download_url(self):
        """Test de l'URL de téléchargement."""
        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        url = collector.get_data_download_url()
        assert "githubusercontent.com" in url
        assert "OpenExoplanetCatalogue" in url

    def test_get_source_reference_url(self):
        """Test de l'URL de référence."""
        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        url = collector.get_source_reference_url()
        assert "github.com" in url

    def test_get_required_csv_columns(self):
        """Test des colonnes requises."""
        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        columns = collector.get_required_csv_columns()
        assert isinstance(columns, list)
        # Vérifier quelques colonnes essentielles
        assert "name" in columns
        assert "star_name" in columns

    @patch("src.collectors.base_collector.pd.read_csv")
    def test_validate_required_columns_success(self, mock_read_csv):
        """Test de validation des colonnes réussie."""
        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

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
        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        # Test conversion réussie
        assert collector.convert_to_float_if_possible("1.5") == 1.5
        assert collector.convert_to_float_if_possible(2.5) == 2.5

        # Test valeurs non convertibles
        assert collector.convert_to_float_if_possible(None) is None
        assert collector.convert_to_float_if_possible("invalid") is None
        assert collector.convert_to_float_if_possible(pd.NA) is None

    def test_transform_row_to_star_returns_none(self):
        """Test que transform_row_to_star retourne None."""
        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        mock_row = pd.Series({"name": "Test b", "star_name": "Test"})
        result = collector.transform_row_to_star(mock_row)

        assert result is None

    def test_set_orbital_characteristics(self):
        """Test de _set_orbital_characteristics."""
        from src.models.entities.exoplanet_entity import Exoplanet

        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        exoplanet = Exoplanet(pl_name="Test b", st_name="Test")
        row = pd.Series(
            {
                "semimajoraxis": 0.5,
                "eccentricity": 0.1,
                "period": 10.5,
                "inclination": 89.0,
                "longitudeofperiastron": 45.0,
                "periastrontime": 2450000.0,
            }
        )

        collector._set_orbital_characteristics(exoplanet, row)

        assert exoplanet.pl_semi_major_axis is not None
        assert exoplanet.pl_semi_major_axis.value == 0.5
        assert exoplanet.pl_eccentricity is not None
        assert exoplanet.pl_eccentricity.value == 0.1
        assert exoplanet.pl_orbital_period is not None
        assert exoplanet.pl_orbital_period.value == 10.5

    def test_set_orbital_characteristics_with_none_values(self):
        """Test de _set_orbital_characteristics avec valeurs None."""
        from src.models.entities.exoplanet_entity import Exoplanet

        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        exoplanet = Exoplanet(pl_name="Test b", st_name="Test")
        row = pd.Series(
            {
                "semimajoraxis": None,
                "eccentricity": pd.NA,
                "period": "invalid",
            }
        )

        collector._set_orbital_characteristics(exoplanet, row)

        # Les valeurs None/invalides ne doivent pas être définies
        assert exoplanet.pl_semi_major_axis is None
        assert exoplanet.pl_eccentricity is None
        assert exoplanet.pl_orbital_period is None

    def test_set_physical_characteristics(self):
        """Test de _set_physical_characteristics."""
        from src.models.entities.exoplanet_entity import Exoplanet

        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        exoplanet = Exoplanet(pl_name="Test b", st_name="Test")
        row = pd.Series(
            {
                "mass": 1.5,
                "radius": 1.2,
                "temperature": 300.0,
            }
        )

        collector._set_physical_characteristics(exoplanet, row)

        assert exoplanet.pl_mass is not None
        assert exoplanet.pl_mass.value == 1.5
        assert exoplanet.pl_radius is not None
        assert exoplanet.pl_radius.value == 1.2
        assert exoplanet.pl_temperature is not None
        assert exoplanet.pl_temperature.value == 300.0

    def test_set_physical_characteristics_with_none_values(self):
        """Test de _set_physical_characteristics avec valeurs None."""
        from src.models.entities.exoplanet_entity import Exoplanet

        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        exoplanet = Exoplanet(pl_name="Test b", st_name="Test")
        row = pd.Series(
            {
                "mass": None,
                "radius": pd.NA,
                "temperature": "invalid",
            }
        )

        collector._set_physical_characteristics(exoplanet, row)

        assert exoplanet.pl_mass is None
        assert exoplanet.pl_radius is None
        assert exoplanet.pl_temperature is None

    def test_set_star_info_with_numeric_values(self):
        """Test de _set_star_info avec valeurs numériques."""
        from src.models.entities.exoplanet_entity import Exoplanet

        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        exoplanet = Exoplanet(pl_name="Test b", st_name="Test")
        row = pd.Series(
            {
                "star_temperature": 5778.0,
                "star_radius": 1.0,
                "star_mass": 1.0,
                "distance": 10.5,
                "apparentmagnitude": 4.5,
            }
        )

        collector._set_star_info(exoplanet, row)

        assert exoplanet.st_temperature is not None
        assert exoplanet.st_temperature.value == 5778.0
        assert exoplanet.st_radius is not None
        assert exoplanet.st_radius.value == 1.0

    def test_set_star_info_with_string_values(self):
        """Test de _set_star_info avec valeurs string."""
        from src.models.entities.exoplanet_entity import Exoplanet

        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        exoplanet = Exoplanet(pl_name="Test b", st_name="Test")
        row = pd.Series(
            {
                "spectraltype": "G2V",
                "star_temperature": "not_a_number",
            }
        )

        collector._set_star_info(exoplanet, row)

        assert exoplanet.st_spectral_type == "G2V"

    def test_set_star_info_with_none_values(self):
        """Test de _set_star_info avec valeurs None."""
        from src.models.entities.exoplanet_entity import Exoplanet

        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        exoplanet = Exoplanet(pl_name="Test b", st_name="Test")
        row = pd.Series(
            {
                "spectraltype": None,
                "star_temperature": pd.NA,
            }
        )

        collector._set_star_info(exoplanet, row)

        # Les valeurs None ne doivent pas être définies
        assert exoplanet.st_spectral_type is None

    def test_set_alt_names(self):
        """Test de _set_alt_names."""
        from src.models.entities.exoplanet_entity import Exoplanet

        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        exoplanet = Exoplanet(pl_name="Test b", st_name="Test")
        row = pd.Series(
            {
                "alt_names": "Alt1, Alt2, Test b, Alt3",
            }
        )

        collector._set_alt_names(exoplanet, row)

        # Test b ne doit pas être ajouté (c'est le nom principal)
        assert len(exoplanet.pl_altname) == 3
        assert "Alt1" in exoplanet.pl_altname
        assert "Alt2" in exoplanet.pl_altname
        assert "Alt3" in exoplanet.pl_altname
        assert "Test b" not in exoplanet.pl_altname

    def test_set_alt_names_with_none(self):
        """Test de _set_alt_names avec valeur None."""
        from src.models.entities.exoplanet_entity import Exoplanet

        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        exoplanet = Exoplanet(pl_name="Test b", st_name="Test")
        row = pd.Series(
            {
                "alt_names": None,
            }
        )

        collector._set_alt_names(exoplanet, row)

        assert len(exoplanet.pl_altname) == 0

    def test_transform_row_to_exoplanet_success(self):
        """Test de transformation réussie d'une ligne en Exoplanet."""
        from src.models.references.reference import Reference, SourceType

        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        row = pd.Series(
            {
                "name": "Kepler-1032 b",
                "star_name": "Kepler-1032",
                "semimajoraxis": 0.5,
                "mass": 1.5,
                "radius": 1.2,
                "spectraltype": "G2V",
                "alt_names": "Alt1, Alt2",
            }
        )

        # Mocker create_reference pour retourner une référence valide
        from datetime import datetime

        mock_reference = Reference(
            source=SourceType.OEC,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
            star_id="Kepler-1032",
            planet_id="Kepler-1032 b",
        )
        with patch.object(
            collector.reference_manager,
            "create_reference",
            return_value=mock_reference,
        ):
            result = collector.transform_row_to_exoplanet(row)

            assert result is not None
            assert result.pl_name == "Kepler-1032 b"
            assert result.st_name == "Kepler-1032"
            assert result.pl_semi_major_axis is not None
            assert result.pl_mass is not None

    def test_transform_row_to_exoplanet_missing_name(self):
        """Test de transformation avec nom manquant."""
        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        row = pd.Series(
            {
                "name": None,
                "star_name": "Kepler-1032",
            }
        )

        result = collector.transform_row_to_exoplanet(row)

        assert result is None

    def test_transform_row_to_exoplanet_missing_star_name(self):
        """Test de transformation avec star_name manquant."""
        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        row = pd.Series(
            {
                "name": "Kepler-1032 b",
                "star_name": None,
            }
        )

        result = collector.transform_row_to_exoplanet(row)

        assert result is None

    def test_transform_row_to_exoplanet_exception(self):
        """Test de gestion d'exception lors de la transformation."""
        collector = OpenExoplanetCatalogueCollector(use_mock_data=True)

        row = pd.Series(
            {
                "name": "Test b",
                "star_name": "Test",
            }
        )

        # Simuler une exception dans create_reference
        with patch.object(
            collector.reference_manager,
            "create_reference",
            side_effect=Exception("Reference error"),
        ):
            result = collector.transform_row_to_exoplanet(row)
            assert result is None
