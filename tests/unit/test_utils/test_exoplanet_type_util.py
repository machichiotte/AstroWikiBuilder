"""
Tests unitaires pour ExoplanetTypeUtil.
"""

import math

import pytest

from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.utils.astro.classification.exoplanet_type_util import ExoplanetTypeUtil


class TestExoplanetTypeUtil:
    """Tests pour les utilitaires de classification d'exoplanètes."""

    @pytest.fixture
    def util(self):
        """Fixture pour créer une instance des util."""
        return ExoplanetTypeUtil()

    # Tests pour convert_mass_to_earth_units
    def test_convert_mass_to_earth_units_valid(self, util):
        """Test de conversion de masse Jupiter vers Terre."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_mass=ValueWithUncertainty(value=1.0),  # 1 M_Jupiter
        )
        result = util.convert_mass_to_earth_units(exoplanet)

        assert result is not None
        assert result == pytest.approx(317.8, rel=0.01)

    def test_convert_mass_to_earth_units_none(self, util):
        """Test avec masse None."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = util.convert_mass_to_earth_units(exoplanet)

        assert result is None

    # Tests pour convert_radius_to_earth_units
    def test_convert_radius_to_earth_units_valid(self, util):
        """Test de conversion de rayon Jupiter vers Terre."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_radius=ValueWithUncertainty(value=1.0),  # 1 R_Jupiter
        )
        result = util.convert_radius_to_earth_units(exoplanet)

        assert result is not None
        assert result == pytest.approx(11.2, rel=0.01)

    def test_convert_radius_to_earth_units_none(self, util):
        """Test avec rayon None."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = util.convert_radius_to_earth_units(exoplanet)

        assert result is None

    # Tests pour calculate_density_from_mass_and_radius
    def test_calculate_density_valid(self, util):
        """Test de calcul de densité."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_mass=ValueWithUncertainty(value=1.0),
            pl_radius=ValueWithUncertainty(value=1.0),
        )
        result = util.calculate_density_from_mass_and_radius(exoplanet)

        assert result is not None
        assert result > 0

    def test_calculate_density_missing_data(self, util):
        """Test avec données manquantes."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_mass=ValueWithUncertainty(value=1.0),
        )
        result = util.calculate_density_from_mass_and_radius(exoplanet)

        assert result is None

    # Tests pour compute_stellar_insolation
    def test_compute_stellar_insolation_valid(self, util):
        """Test de calcul d'insolation."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_luminosity=ValueWithUncertainty(value=1.0),
            pl_semi_major_axis=ValueWithUncertainty(value=0.05),
        )
        result = util.compute_stellar_insolation(exoplanet)

        assert not math.isnan(result)
        assert result > 0

    def test_compute_stellar_insolation_missing_data(self, util):
        """Test avec données manquantes."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = util.compute_stellar_insolation(exoplanet)

        assert math.isnan(result)

    def test_compute_stellar_insolation_zero_distance(self, util):
        """Test avec distance nulle."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_luminosity=ValueWithUncertainty(value=1.0),
            pl_semi_major_axis=ValueWithUncertainty(value=0.0),
        )
        result = util.compute_stellar_insolation(exoplanet)

        assert math.isnan(result)

    # Tests pour classify_planet_type_by_mass_only
    def test_classify_by_mass_super_earth(self, util):
        """Test classification Super-Terre par masse."""
        result = util.classify_planet_type_by_mass_only(5.0)  # 5 M_Earth
        assert result == "Super-Terre"

    def test_classify_by_mass_earth_like(self, util):
        """Test classification terrestre par masse."""
        result = util.classify_planet_type_by_mass_only(1.0)  # 1 M_Earth
        assert result == "Planète de dimensions terrestres"

    def test_classify_by_mass_giant(self, util):
        """Test classification géante par masse."""
        result = util.classify_planet_type_by_mass_only(50.0)  # 50 M_Earth
        assert result == "Planète géante de masse élevée"

    # Tests pour classify_planet_type_by_radius_only
    def test_classify_by_radius_earth_like(self, util):
        """Test classification terrestre par rayon."""
        result = util.classify_planet_type_by_radius_only(1.0)  # 1 R_Earth
        assert result == "Planète de dimensions terrestres"

    def test_classify_by_radius_super_puff(self, util):
        """Test classification super-enflée par rayon."""
        result = util.classify_planet_type_by_radius_only(5.0)  # 5 R_Earth
        assert result == "Planète super-enflée"

    def test_classify_by_radius_moderate(self, util):
        """Test classification rayon modéré."""
        result = util.classify_planet_type_by_radius_only(2.5)  # 2.5 R_Earth
        assert result == "Planète géante de rayon modéré"

    # Tests pour classify_terrestrial_type_by_mass_and_radius
    def test_classify_terrestrial_sub_earth(self, util):
        """Test classification Sous-Terre."""
        result = util.classify_terrestrial_type_by_mass_and_radius(0.3, 0.7)
        assert result == "Sous-Terre"

    def test_classify_terrestrial_earth_like(self, util):
        """Test classification terrestre."""
        result = util.classify_terrestrial_type_by_mass_and_radius(1.0, 1.0)
        assert result == "Planète de dimensions terrestres"

    def test_classify_terrestrial_super_earth(self, util):
        """Test classification Super-Terre."""
        result = util.classify_terrestrial_type_by_mass_and_radius(5.0, 1.5)
        assert result == "Super-Terre"

    def test_classify_terrestrial_mega_earth(self, util):
        """Test classification Méga-Terre."""
        result = util.classify_terrestrial_type_by_mass_and_radius(15.0, 2.0)
        assert result == "Méga-Terre"

    # Tests pour determine_exoplanet_classification (intégration)
    def test_classification_hot_jupiter(self, util):
        """Test classification Jupiter chaud."""
        exoplanet = Exoplanet(
            pl_name="Hot Jupiter",
            pl_mass=ValueWithUncertainty(value=1.0),  # 1 M_Jupiter
            pl_radius=ValueWithUncertainty(value=1.3),
            pl_temperature=ValueWithUncertainty(value=1500),
        )
        result = util.determine_exoplanet_classification(exoplanet)

        assert "Jupiter" in result
        assert "chaud" in result

    def test_classification_super_earth(self, util):
        """Test classification Super-Terre."""
        exoplanet = Exoplanet(
            pl_name="Super Earth",
            pl_mass=ValueWithUncertainty(value=0.015),  # ~5 M_Earth
            pl_radius=ValueWithUncertainty(value=0.15),  # ~1.7 R_Earth
        )
        result = util.determine_exoplanet_classification(exoplanet)

        assert "Super-Terre" in result

    def test_classification_neptune_like(self, util):
        """Test classification Neptune."""
        exoplanet = Exoplanet(
            pl_name="Neptune-like",
            pl_mass=ValueWithUncertainty(value=0.05),  # ~16 M_Earth
            pl_radius=ValueWithUncertainty(value=0.35),  # ~4 R_Earth
            pl_semi_major_axis=ValueWithUncertainty(value=0.5),
        )
        result = util.determine_exoplanet_classification(exoplanet)

        assert "Neptune" in result or "géante" in result

    def test_classification_minimal_data(self, util):
        """Test avec données minimales."""
        exoplanet = Exoplanet(pl_name="Minimal")
        result = util.determine_exoplanet_classification(exoplanet)

        assert result == "Exoplanète"

    def test_classification_mass_only(self, util):
        """Test classification avec masse uniquement."""
        exoplanet = Exoplanet(
            pl_name="Mass Only",
            pl_mass=ValueWithUncertainty(value=0.01),  # ~3 M_Earth
        )
        result = util.determine_exoplanet_classification(exoplanet)

        assert result != "Exoplanète"

    def test_classification_radius_only(self, util):
        """Test classification avec rayon uniquement."""
        exoplanet = Exoplanet(
            pl_name="Radius Only",
            pl_radius=ValueWithUncertainty(value=0.1),  # ~1.1 R_Earth
        )
        result = util.determine_exoplanet_classification(exoplanet)

        assert result != "Exoplanète"
