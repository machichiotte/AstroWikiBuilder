"""Tests for FormationMechanismSection."""

from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.formation_mechanism_section import (
    FormationMechanismSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


@pytest.fixture
def article_util():
    """Create a mock article utility."""
    return Mock()


@pytest.fixture
def section(article_util):
    """Create a FormationMechanismSection instance."""
    return FormationMechanismSection(article_util)


class TestFormationMechanismSection:
    """Test suite for FormationMechanismSection."""

    def test_init(self, article_util):
        """Test section initialization."""
        section = FormationMechanismSection(article_util)
        assert section.article_util == article_util
        assert "hot_jupiter" in section.rules
        assert "red_dwarf" in section.rules
        assert "super_earth" in section.rules
        assert "eccentric" in section.rules
        assert len(section.templates) == 4

    def test_safe_float_with_valid_number(self, section):
        """Test _safe_float with valid number."""
        assert section._safe_float(3.14) == 3.14
        assert section._safe_float(42) == 42.0
        assert section._safe_float("2.5") == 2.5

    def test_safe_float_with_invalid_value(self, section):
        """Test _safe_float with invalid value."""
        assert section._safe_float(None) == 0.0
        assert section._safe_float("invalid") == 0.0
        assert section._safe_float([]) == 0.0

    def test_is_hot_jupiter_with_high_mass(self, section):
        """Test _is_hot_jupiter with high mass planet."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_mass=ValueWithUncertainty(value=0.1),  # 0.1 MJ = 31.8 ME
            pl_radius=ValueWithUncertainty(value=0.5),
            pl_orbital_period=ValueWithUncertainty(value=5.0),
        )
        assert section._is_hot_jupiter(exoplanet) is True

    def test_is_hot_jupiter_with_large_radius(self, section):
        """Test _is_hot_jupiter with large radius planet."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_mass=ValueWithUncertainty(value=0.01),
            pl_radius=ValueWithUncertainty(value=1.0),  # > 0.8 RJ
            pl_orbital_period=ValueWithUncertainty(value=5.0),
        )
        assert section._is_hot_jupiter(exoplanet) is True

    def test_is_hot_jupiter_with_long_period(self, section):
        """Test _is_hot_jupiter with long orbital period (not hot jupiter)."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_mass=ValueWithUncertainty(value=0.1),
            pl_radius=ValueWithUncertainty(value=1.0),
            pl_orbital_period=ValueWithUncertainty(value=100.0),
        )
        assert section._is_hot_jupiter(exoplanet) is False

    def test_is_hot_jupiter_with_none_values(self, section):
        """Test _is_hot_jupiter with None values."""
        exoplanet = Exoplanet(pl_name="Test b")
        assert section._is_hot_jupiter(exoplanet) is False

    def test_is_red_dwarf_system_with_m_type_star(self, section):
        """Test _is_red_dwarf_system with M-type star."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_spectral_type="M3V",
            st_name="Test",
        )
        assert section._is_red_dwarf_system(exoplanet) is True

    def test_is_red_dwarf_system_with_low_mass_star(self, section):
        """Test _is_red_dwarf_system with low mass star."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_spectral_type="K5V",
            st_mass=ValueWithUncertainty(value=0.3),
            st_name="Test",
        )
        assert section._is_red_dwarf_system(exoplanet) is True

    def test_is_red_dwarf_system_with_high_mass_star(self, section):
        """Test _is_red_dwarf_system with high mass star."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_spectral_type="G2V",
            st_mass=ValueWithUncertainty(value=1.0),
            st_name="Test",
        )
        assert section._is_red_dwarf_system(exoplanet) is False

    def test_is_red_dwarf_system_with_none_values(self, section):
        """Test _is_red_dwarf_system with None values."""
        exoplanet = Exoplanet(pl_name="Test b")
        # When st_mass is None, _safe_float returns 0.0, which is < 0.5
        assert section._is_red_dwarf_system(exoplanet) is True

    def test_is_super_earth_or_mini_neptune_with_valid_radius(self, section):
        """Test _is_super_earth_or_mini_neptune with valid radius."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_radius=ValueWithUncertainty(value=2.5),
        )
        assert section._is_super_earth_or_mini_neptune(exoplanet) is True

    def test_is_super_earth_or_mini_neptune_with_small_radius(self, section):
        """Test _is_super_earth_or_mini_neptune with small radius."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_radius=ValueWithUncertainty(value=1.0),
        )
        assert section._is_super_earth_or_mini_neptune(exoplanet) is False

    def test_is_super_earth_or_mini_neptune_with_large_radius(self, section):
        """Test _is_super_earth_or_mini_neptune with large radius."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_radius=ValueWithUncertainty(value=5.0),
        )
        assert section._is_super_earth_or_mini_neptune(exoplanet) is False

    def test_is_super_earth_or_mini_neptune_with_none_values(self, section):
        """Test _is_super_earth_or_mini_neptune with None values."""
        exoplanet = Exoplanet(pl_name="Test b")
        assert section._is_super_earth_or_mini_neptune(exoplanet) is False

    def test_has_eccentric_orbit_with_high_eccentricity(self, section):
        """Test _has_eccentric_orbit with high eccentricity."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_eccentricity=ValueWithUncertainty(value=0.5),
        )
        assert section._has_eccentric_orbit(exoplanet) is True

    def test_has_eccentric_orbit_with_low_eccentricity(self, section):
        """Test _has_eccentric_orbit with low eccentricity."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_eccentricity=ValueWithUncertainty(value=0.1),
        )
        assert section._has_eccentric_orbit(exoplanet) is False

    def test_has_eccentric_orbit_with_none_values(self, section):
        """Test _has_eccentric_orbit with None values."""
        exoplanet = Exoplanet(pl_name="Test b")
        assert section._has_eccentric_orbit(exoplanet) is False

    def test_generate_hot_jupiter(self, section):
        """Test generate with hot jupiter."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            pl_mass=ValueWithUncertainty(value=0.1),
            pl_radius=ValueWithUncertainty(value=1.0),
            pl_orbital_period=ValueWithUncertainty(value=5.0),
        )
        result = section.generate(exoplanet)
        assert "== Mécanismes de formation ==" in result
        assert "migration planétaire" in result

    def test_generate_red_dwarf(self, section):
        """Test generate with red dwarf system."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Proxima",
            st_spectral_type="M5V",
        )
        result = section.generate(exoplanet)
        assert "== Mécanismes de formation ==" in result
        assert "naine rouge" in result
        assert "Proxima" in result

    def test_generate_super_earth(self, section):
        """Test generate with super earth."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            pl_radius=ValueWithUncertainty(value=2.0),
            pl_orbital_period=ValueWithUncertainty(value=100.0),  # Long period to avoid hot jupiter
            st_spectral_type="G2V",  # Not a red dwarf
            st_mass=ValueWithUncertainty(value=1.0),  # Solar mass to avoid red dwarf
        )
        result = section.generate(exoplanet)
        assert "== Mécanismes de formation ==" in result
        assert "super-Terre" in result

    def test_generate_eccentric(self, section):
        """Test generate with eccentric orbit."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            pl_eccentricity=ValueWithUncertainty(value=0.6),
            pl_orbital_period=ValueWithUncertainty(value=100.0),  # Long period to avoid hot jupiter
            st_spectral_type="G2V",  # Not a red dwarf
            st_mass=ValueWithUncertainty(value=1.0),  # Solar mass to avoid red dwarf
            pl_radius=ValueWithUncertainty(value=1.0),  # Not a super earth
        )
        result = section.generate(exoplanet)
        assert "== Mécanismes de formation ==" in result
        assert "excentricité orbitale" in result

    def test_generate_no_match(self, section):
        """Test generate with no matching rule."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            pl_radius=ValueWithUncertainty(value=1.0),  # Not a super earth (1.5 < radius < 4.0)
            pl_eccentricity=ValueWithUncertainty(value=0.1),  # Not eccentric (> 0.3)
            pl_orbital_period=ValueWithUncertainty(value=100.0),  # Not a hot jupiter (period < 10)
            st_spectral_type="G2V",  # Not a red dwarf
            st_mass=ValueWithUncertainty(value=1.0),  # Not a red dwarf (mass < 0.5)
        )
        result = section.generate(exoplanet)
        assert result == ""

    def test_generate_with_none_star_name(self, section):
        """Test generate with None star name."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name=None,
            st_spectral_type="M5V",
        )
        result = section.generate(exoplanet)
        assert "== Mécanismes de formation ==" in result
        assert "l'étoile hôte" in result
