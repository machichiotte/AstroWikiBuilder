# tests/unit/test_models/test_exoplanet_entity.py
"""
Tests pour le modèle Exoplanet.
"""

from datetime import datetime

import pytest

from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.references.reference import Reference, SourceType


class TestExoplanet:
    """Tests du modèle Exoplanet."""

    @pytest.fixture
    def sample_exoplanet(self):
        reference = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
            planet_id="HD 209458 b",
        )
        return Exoplanet(
            pl_name="HD 209458 b",
            pl_mass=ValueWithUncertainty(value=0.69, error_positive=0.05, error_negative=0.05),
            pl_radius=ValueWithUncertainty(value=1.35, error_positive=0.05, error_negative=0.05),
            pl_orbital_period=ValueWithUncertainty(value=3.5247),
            disc_method="Transit",
            disc_year=1999,
            st_name="HD 209458",
            reference=reference,
        )

    def test_create_exoplanet_with_all_fields(self, sample_exoplanet):
        """Test de création d'une exoplanète avec tous les champs."""
        exo = sample_exoplanet

        assert exo.pl_name == "HD 209458 b"
        assert exo.pl_mass.value == 0.69
        assert exo.pl_radius.value == 1.35
        assert exo.pl_orbital_period.value == 3.5247
        assert exo.disc_method == "Transit"
        assert exo.disc_year == 1999
        assert exo.st_name == "HD 209458"
        assert exo.reference.source == SourceType.NEA

    def test_exoplanet_initialization_with_host_star_info(self):
        """Test de l'initialisation avec les infos de l'étoile hôte."""
        exoplanet = Exoplanet(
            pl_name="Test Planet b",
            st_name="Test Star",
            pl_mass=ValueWithUncertainty(value=1.5),
            st_metallicity=ValueWithUncertainty(value=0.1),
            st_age=ValueWithUncertainty(value=4.5),
        )

        assert exoplanet.pl_name == "Test Planet b"
        assert exoplanet.st_name == "Test Star"
        assert exoplanet.pl_mass.value == 1.5
        assert exoplanet.st_metallicity.value == 0.1
        assert exoplanet.st_age.value == 4.5

    def test_exoplanet_with_minimal_fields(self):
        """Test avec champs minimaux."""
        reference = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
            planet_id="Test Planet b",
        )

        exo = Exoplanet(
            pl_name="Test Planet b",
            reference=reference,
        )

        assert exo.pl_name == "Test Planet b"
        assert exo.pl_mass is None
        assert exo.pl_radius is None
        assert exo.pl_orbital_period is None

    def test_exoplanet_value_with_uncertainty(self, sample_exoplanet):
        """Test des valeurs avec incertitudes."""
        exo = sample_exoplanet

        assert exo.pl_mass.error_positive == 0.05
        assert exo.pl_mass.error_negative == 0.05
        assert exo.pl_radius.error_positive == 0.05

    def test_exoplanet_str_representation(self, sample_exoplanet):
        """Test de la représentation string."""
        exo = sample_exoplanet
        str_repr = str(exo)

        assert "HD 209458 b" in str_repr


class TestValueWithUncertainty:
    """Tests de la classe ValueWithUncertainty."""

    def test_create_value_with_uncertainty(self):
        """Test de création d'une valeur avec incertitudes."""
        value = ValueWithUncertainty(value=1.5, error_positive=0.1, error_negative=0.1)

        assert value.value == 1.5
        assert value.error_positive == 0.1
        assert value.error_negative == 0.1

    def test_value_without_errors(self):
        """Test d'une valeur sans incertitudes."""
        value = ValueWithUncertainty(value=2.0)

        assert value.value == 2.0
        assert value.error_positive is None
        assert value.error_negative is None

    def test_asymmetric_errors(self):
        """Test d'erreurs asymétriques."""
        value = ValueWithUncertainty(value=3.0, error_positive=0.5, error_negative=0.3)

        assert value.error_positive == 0.5
        assert value.error_negative == 0.3
