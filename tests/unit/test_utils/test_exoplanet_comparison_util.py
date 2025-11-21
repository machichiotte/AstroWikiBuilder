"""
Tests unitaires pour ExoplanetComparisonUtil.

Ce module teste les comparaisons physiques des exoplanètes avec les planètes connues.
"""

from datetime import datetime

import pytest

from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.references.reference import Reference, SourceType
from src.utils.astro.classification.exoplanet_comparison_util import (
    ExoplanetComparisonUtil,
)


class TestExoplanetComparisonUtil:
    """Tests pour ExoplanetComparisonUtil."""

    @pytest.fixture
    def comparison_util(self):
        """Fixture pour créer un ExoplanetComparisonUtil."""
        return ExoplanetComparisonUtil()

    @pytest.fixture
    def create_exoplanet(self):
        """Fixture factory pour créer des exoplanètes de test."""

        def _create(pl_name="Test b", pl_radius=None, pl_mass=None, pl_semi_major_axis=None):
            ref = Reference(
                source=SourceType.NEA,
                star_id="Test",
                planet_id=pl_name,
                update_date=datetime.now(),
                consultation_date=datetime.now(),
            )
            return Exoplanet(
                pl_name=pl_name,
                st_name="Test",
                pl_radius=pl_radius,
                pl_mass=pl_mass,
                pl_semi_major_axis=pl_semi_major_axis,
                reference=ref,
            )

        return _create

    # Tests pour describe_radius_vs_known_planets

    def test_describe_radius_no_radius(self, comparison_util, create_exoplanet):
        """Test avec aucun rayon."""
        exo = create_exoplanet()
        result = comparison_util.describe_radius_vs_known_planets(exo)
        assert result == ""

    def test_describe_radius_similar_to_jupiter(self, comparison_util, create_exoplanet):
        """Test rayon similaire à Jupiter."""
        exo = create_exoplanet(pl_radius=ValueWithUncertainty(value=1.0))
        result = comparison_util.describe_radius_vs_known_planets(exo)
        assert "similaire à celui de [[Jupiter" in result

    def test_describe_radius_larger_than_jupiter(self, comparison_util, create_exoplanet):
        """Test rayon plus grand que Jupiter."""
        exo = create_exoplanet(pl_radius=ValueWithUncertainty(value=2.0))
        result = comparison_util.describe_radius_vs_known_planets(exo)
        assert "fois celui de [[Jupiter" in result
        assert "2" in result or "deux" in result

    def test_describe_radius_similar_to_earth(self, comparison_util, create_exoplanet):
        """Test rayon similaire à la Terre."""
        # 1 R_Earth = 1/11.209 R_Jupiter ≈ 0.089 R_J
        exo = create_exoplanet(pl_radius=ValueWithUncertainty(value=0.089))
        result = comparison_util.describe_radius_vs_known_planets(exo)
        assert "similaire à celui de la [[Terre]]" in result

    def test_describe_radius_larger_than_earth(self, comparison_util, create_exoplanet):
        """Test rayon plus grand que la Terre."""
        exo = create_exoplanet(pl_radius=ValueWithUncertainty(value=0.2))
        result = comparison_util.describe_radius_vs_known_planets(exo)
        assert "fois celui de la [[Terre]]" in result

    def test_describe_radius_smaller_than_earth(self, comparison_util, create_exoplanet):
        """Test rayon plus petit que la Terre."""
        exo = create_exoplanet(pl_radius=ValueWithUncertainty(value=0.05))
        result = comparison_util.describe_radius_vs_known_planets(exo)
        assert "plus petit que celui de la [[Terre]]" in result

    # Tests pour describe_mass_vs_known_planets

    def test_describe_mass_no_mass(self, comparison_util, create_exoplanet):
        """Test avec aucune masse."""
        exo = create_exoplanet()
        result = comparison_util.describe_mass_vs_known_planets(exo)
        assert result == ""

    def test_describe_mass_similar_to_jupiter(self, comparison_util, create_exoplanet):
        """Test masse similaire à Jupiter."""
        exo = create_exoplanet(pl_mass=ValueWithUncertainty(value=1.0))
        result = comparison_util.describe_mass_vs_known_planets(exo)
        assert "même masse que [[Jupiter" in result

    def test_describe_mass_larger_than_jupiter(self, comparison_util, create_exoplanet):
        """Test masse plus grande que Jupiter."""
        exo = create_exoplanet(pl_mass=ValueWithUncertainty(value=2.0))
        result = comparison_util.describe_mass_vs_known_planets(exo)
        assert "fois plus massif que [[Jupiter" in result
        assert "2" in result or "deux" in result

    def test_describe_mass_similar_to_earth(self, comparison_util, create_exoplanet):
        """Test masse similaire à la Terre."""
        # 1 M_Earth = 1/317.8 M_Jupiter ≈ 0.00315 M_J
        exo = create_exoplanet(pl_mass=ValueWithUncertainty(value=0.00315))
        result = comparison_util.describe_mass_vs_known_planets(exo)
        assert "même masse que la [[Terre]]" in result

    def test_describe_mass_larger_than_earth(self, comparison_util, create_exoplanet):
        """Test masse plus grande que la Terre."""
        exo = create_exoplanet(pl_mass=ValueWithUncertainty(value=0.01))
        result = comparison_util.describe_mass_vs_known_planets(exo)
        assert "fois plus massif que la [[Terre]]" in result

    def test_describe_mass_smaller_than_earth(self, comparison_util, create_exoplanet):
        """Test masse plus petite que la Terre."""
        exo = create_exoplanet(pl_mass=ValueWithUncertainty(value=0.001))
        result = comparison_util.describe_mass_vs_known_planets(exo)
        assert "fois moins massif que la [[Terre]]" in result

    # Tests pour describe_orbit_vs_solar_system

    def test_describe_orbit_no_sma(self, comparison_util, create_exoplanet):
        """Test avec aucun demi-grand axe."""
        exo = create_exoplanet()
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert result == ""

    def test_describe_orbit_closer_than_mercury(self, comparison_util, create_exoplanet):
        """Test orbite plus proche que Mercure."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=0.1))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "plus proche" in result
        assert "Mercure" in result

    def test_describe_orbit_similar_to_mercury(self, comparison_util, create_exoplanet):
        """Test orbite similaire à Mercure."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=0.387))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "comparable à celle de [[Mercure" in result

    def test_describe_orbit_between_mercury_and_venus(self, comparison_util, create_exoplanet):
        """Test orbite entre Mercure et Vénus."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=0.5))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "Mercure" in result
        assert "Vénus" in result

    def test_describe_orbit_similar_to_venus(self, comparison_util, create_exoplanet):
        """Test orbite similaire à Vénus."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=0.723))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "comparable à celle de [[Vénus" in result

    def test_describe_orbit_similar_to_earth(self, comparison_util, create_exoplanet):
        """Test orbite similaire à la Terre."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=1.0))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "comparable à celle de la [[Terre]]" in result

    def test_describe_orbit_similar_to_mars(self, comparison_util, create_exoplanet):
        """Test orbite similaire à Mars."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=1.524))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "comparable à celle de [[Mars" in result

    def test_describe_orbit_asteroid_belt(self, comparison_util, create_exoplanet):
        """Test orbite dans la ceinture d'astéroïdes."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=3.0))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "ceinture d'astéroïdes" in result

    def test_describe_orbit_similar_to_jupiter(self, comparison_util, create_exoplanet):
        """Test orbite similaire à Jupiter."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=5.203))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "comparable à celle de [[Jupiter" in result

    def test_describe_orbit_similar_to_saturn(self, comparison_util, create_exoplanet):
        """Test orbite similaire à Saturne."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=9.582))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "comparable à celle de [[Saturne" in result

    def test_describe_orbit_similar_to_uranus(self, comparison_util, create_exoplanet):
        """Test orbite similaire à Uranus."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=19.229))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "comparable à celle d'[[Uranus" in result

    def test_describe_orbit_similar_to_neptune(self, comparison_util, create_exoplanet):
        """Test orbite similaire à Neptune."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=30.103))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "comparable à celle de [[Neptune" in result

    def test_describe_orbit_farther_than_neptune(self, comparison_util, create_exoplanet):
        """Test orbite plus loin que Neptune."""
        exo = create_exoplanet(pl_semi_major_axis=ValueWithUncertainty(value=50.0))
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "plus éloignée" in result
        assert "Neptune" in result

    def test_describe_orbit_with_float_sma(self, comparison_util, create_exoplanet):
        """Test orbite avec sma en float direct."""
        exo = create_exoplanet(pl_semi_major_axis=1.0)
        result = comparison_util.describe_orbit_vs_solar_system(exo)
        assert "Terre" in result
