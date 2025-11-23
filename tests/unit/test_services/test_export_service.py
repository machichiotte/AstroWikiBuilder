"""
Tests unitaires pour ExportService.

Ce module teste l'export de données vers CSV et JSON.
"""

import os
from unittest.mock import mock_open, patch

import pytest

from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.references.reference import Reference, SourceType
from src.services.external.export_service import ExportService


class TestExportService:
    """Tests pour ExportService."""

    @pytest.fixture
    def export_service(self):
        """Fixture pour créer un service d'export."""
        return ExportService()

    @pytest.fixture
    def sample_exoplanet(self):
        """Fixture pour créer une exoplanète de test."""
        from datetime import datetime

        ref = Reference(
            source=SourceType.NEA,
            star_id="Kepler-186",
            planet_id="Kepler-186 f",
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )
        return Exoplanet(
            pl_name="Kepler-186 f",
            st_name="Kepler-186",
            pl_mass=ValueWithUncertainty(value=1.71, error_positive=0.15),
            pl_radius=ValueWithUncertainty(value=1.17),
            pl_orbital_period=ValueWithUncertainty(value=129.9441),
            disc_method="Transit",
            disc_year=2014,
            reference=ref,
        )

    @pytest.fixture
    def sample_exoplanets(self, sample_exoplanet):
        """Fixture pour créer une liste d'exoplanètes."""
        from datetime import datetime

        ref2 = Reference(
            source=SourceType.NEA,
            star_id="Kepler-22",
            planet_id="Kepler-22 b",
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )
        exo2 = Exoplanet(
            pl_name="Kepler-22 b",
            st_name="Kepler-22",
            pl_mass=ValueWithUncertainty(value=36.0),
            pl_radius=ValueWithUncertainty(value=2.4),
            disc_method="Transit",
            disc_year=2011,
            reference=ref2,
        )
        return [sample_exoplanet, exo2]

    def test_init(self, export_service):
        """Test d'initialisation du service."""
        assert export_service is not None

    def test_exoplanet_to_dict_flat(self, export_service, sample_exoplanet):
        """Test de conversion d'exoplanète en dictionnaire."""
        result = export_service._exoplanet_to_dict_flat(sample_exoplanet)

        assert isinstance(result, dict)
        assert result["pl_name"] == "Kepler-186 f"
        assert result["st_name"] == "Kepler-186"
        assert result["disc_method"] == "Transit"
        assert result["disc_year"] == 2014

    def test_exoplanet_to_dict_flat_with_altnames(self, export_service):
        """Test de conversion avec noms alternatifs."""
        from datetime import datetime

        ref = Reference(
            source=SourceType.NEA,
            star_id="Test",
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )
        exo = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            pl_altname=["Alt1", "Alt2"],
            reference=ref,
        )

        result = export_service._exoplanet_to_dict_flat(exo)
        assert result["pl_altname"] == "Alt1, Alt2"

    def test_exoplanet_to_dict_flat_without_altnames(self, export_service, sample_exoplanet):
        """Test de conversion sans noms alternatifs."""
        result = export_service._exoplanet_to_dict_flat(sample_exoplanet)
        assert result["pl_altname"] is None

    @patch("builtins.open", new_callable=mock_open)
    def test_export_exoplanets_to_csv(self, mock_file, export_service, sample_exoplanets, tmp_path):
        """Test d'export vers CSV."""
        filename = str(tmp_path / "test_export.csv")
        export_service.export_exoplanets_to_csv(filename, sample_exoplanets)

        # Vérifier que le fichier a été ouvert en écriture
        mock_file.assert_called_once_with(filename, "w", newline="", encoding="utf-8")

    def test_export_exoplanets_to_csv_empty_list(self, export_service, tmp_path):
        """Test d'export CSV avec liste vide."""
        filename = str(tmp_path / "test_empty.csv")
        export_service.export_exoplanets_to_csv(filename, [])

        # Vérifier que le fichier n'a pas été créé
        assert not os.path.exists(filename)

    @patch("builtins.open", new_callable=mock_open)
    def test_export_exoplanets_to_json(
        self, mock_file, export_service, sample_exoplanets, tmp_path
    ):
        """Test d'export vers JSON."""
        filename = str(tmp_path / "test_export.json")
        export_service.export_exoplanets_to_json(filename, sample_exoplanets)

        # Vérifier que le fichier a été ouvert en écriture
        mock_file.assert_called_once_with(filename, "w", encoding="utf-8")

    def test_export_exoplanets_to_json_empty_list(self, export_service, tmp_path):
        """Test d'export JSON avec liste vide."""
        filename = str(tmp_path / "test_empty.json")
        export_service.export_exoplanets_to_json(filename, [])

        # Vérifier que le fichier n'a pas été créé
        assert not os.path.exists(filename)

    @patch("builtins.open", new_callable=mock_open)
    def test_export_generic_list_of_dicts_to_csv(self, mock_file, export_service, tmp_path):
        """Test d'export générique vers CSV."""
        filename = str(tmp_path / "test_generic.csv")
        data = [
            {"name": "Item1", "value": 10},
            {"name": "Item2", "value": 20},
        ]

        export_service.export_generic_list_of_dicts_to_csv(filename, data)

        # Vérifier que le fichier a été ouvert en écriture
        mock_file.assert_called_once_with(filename, "w", newline="", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open)
    def test_export_generic_list_of_dicts_to_csv_with_headers(
        self, mock_file, export_service, tmp_path
    ):
        """Test d'export générique vers CSV avec headers personnalisés."""
        filename = str(tmp_path / "test_generic_headers.csv")
        data = [
            {"name": "Item1", "value": 10, "extra": "ignored"},
            {"name": "Item2", "value": 20, "extra": "ignored"},
        ]
        headers = ["name", "value"]

        export_service.export_generic_list_of_dicts_to_csv(filename, data, headers)

        # Vérifier que le fichier a été ouvert en écriture
        mock_file.assert_called_once_with(filename, "w", newline="", encoding="utf-8")

    def test_export_generic_list_of_dicts_to_csv_empty_list(self, export_service, tmp_path):
        """Test d'export générique CSV avec liste vide."""
        filename = str(tmp_path / "test_generic_empty.csv")
        export_service.export_generic_list_of_dicts_to_csv(filename, [])

        # Vérifier que le fichier n'a pas été créé
        assert not os.path.exists(filename)

    @patch("builtins.open", new_callable=mock_open)
    def test_export_generic_list_of_dicts_to_json(self, mock_file, export_service, tmp_path):
        """Test d'export générique vers JSON."""
        filename = str(tmp_path / "test_generic.json")
        data = [
            {"name": "Item1", "value": 10},
            {"name": "Item2", "value": 20},
        ]

        export_service.export_generic_list_of_dicts_to_json(filename, data)

        # Vérifier que le fichier a été ouvert en écriture
        mock_file.assert_called_once_with(filename, "w", encoding="utf-8")

    def test_export_generic_list_of_dicts_to_json_empty_list(self, export_service, tmp_path):
        """Test d'export générique JSON avec liste vide."""
        filename = str(tmp_path / "test_generic_empty.json")
        export_service.export_generic_list_of_dicts_to_json(filename, [])

        # Vérifier que le fichier n'a pas été créé
        assert not os.path.exists(filename)

    @patch("builtins.open", side_effect=OSError("Permission denied"))
    def test_export_exoplanets_to_csv_error(
        self, mock_file, export_service, sample_exoplanets, tmp_path
    ):
        """Test de gestion d'erreur lors de l'export CSV."""
        filename = str(tmp_path / "test_error.csv")

        # Ne doit pas lever d'exception, juste logger l'erreur
        export_service.export_exoplanets_to_csv(filename, sample_exoplanets)

    @patch("builtins.open", side_effect=OSError("Permission denied"))
    def test_export_exoplanets_to_json_error(
        self, mock_file, export_service, sample_exoplanets, tmp_path
    ):
        """Test de gestion d'erreur lors de l'export JSON."""
        filename = str(tmp_path / "test_error.json")

        # Ne doit pas lever d'exception, juste logger l'erreur
        export_service.export_exoplanets_to_json(filename, sample_exoplanets)
