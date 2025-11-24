"""Tests for PhysicalCharacteristicsSection."""

from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.physical_characteristics_section import (
    PhysicalCharacteristicsSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


class TestPhysicalCharacteristicsSection:
    """Test suite for PhysicalCharacteristicsSection."""

    @pytest.fixture
    def section(self):
        """Create a PhysicalCharacteristicsSection instance with mocked dependencies."""
        article_util = Mock()
        article_util.format_number_as_french_string.side_effect = lambda x, precision=None: str(x)
        return PhysicalCharacteristicsSection(article_util)

    def test_get_value_or_none_if_nan_string(self, section):
        """Test handling of 'nan' string."""
        data_point = Mock()
        data_point.value = "nan"
        assert section._get_value_or_none_if_nan(data_point) is None

    def test_format_mass_description_exception(self, section):
        """Test mass description with invalid value."""
        assert section._format_mass_description("invalid") is None

    def test_format_mass_description_low(self, section):
        """Test low mass description."""
        assert "faible" in section._format_mass_description(0.05)

    def test_format_mass_description_moderate(self, section):
        """Test moderate mass description."""
        assert "modérée" in section._format_mass_description(0.5)

    def test_format_mass_description_high(self, section):
        """Test high mass description."""
        assert "imposante" in section._format_mass_description(5.0)

    def test_format_radius_description_exception(self, section):
        """Test radius description with invalid value."""
        assert section._format_radius_description("invalid") is None

    def test_format_radius_description_compact(self, section):
        """Test compact radius description."""
        assert "compact" in section._format_radius_description(0.4)

    def test_format_radius_description_normal(self, section):
        """Test normal radius description (no label)."""
        desc = section._format_radius_description(1.0)
        assert "compact" not in desc
        assert "étendu" not in desc

    def test_format_radius_description_extended(self, section):
        """Test extended radius description."""
        assert "étendu" in section._format_radius_description(2.0)

    def test_format_temperature_description_nan_string(self, section):
        """Test temperature description with 'nan' string."""
        assert section._format_temperature_description("nan") is None

    def test_format_temperature_description_nan_float(self, section):
        """Test temperature description with NaN float."""
        assert section._format_temperature_description(float("nan")) is None

    def test_format_temperature_description_exception(self, section):
        """Test temperature description with invalid value."""

        # To trigger exception in float(temp), pass something that raises ValueError
        # But the first check `isinstance(temp, str) and temp.lower() == "nan"` handles "nan".
        # So we need something else.
        class BadFloat:
            def __float__(self):
                raise ValueError("Bad float")

        assert section._format_temperature_description(BadFloat()) is None

    def test_format_temperature_description_low(self, section):
        """Test low temperature description."""
        desc = section._format_temperature_description(400)
        assert "élevée" not in desc
        assert "extrême" not in desc

    def test_format_temperature_description_high(self, section):
        """Test high temperature description."""
        assert "élevée" in section._format_temperature_description(800)

    def test_format_temperature_description_extreme(self, section):
        """Test extreme temperature description."""
        assert "extrême" in section._format_temperature_description(2000)

    def test_format_temperature_description_string_value(self, section):
        """Test temperature description with string value that is convertible to float."""
        # This hits the `else` branch of `if isinstance(temp, int | float):`
        # But wait, `temp_f = float(temp)` is done before.
        # If temp is "1000", it is converted to float.
        # But `isinstance("1000", int | float)` is False.
        # So it goes to `else: temp_value = str(temp)`.
        desc = section._format_temperature_description("1200")
        assert "1200" in desc
        assert "extrême" in desc

    def test_generate_empty(self, section):
        """Test generate with no data."""
        exoplanet = Exoplanet(pl_name="Test Planet")
        assert section.generate(exoplanet) == ""

    def test_generate_full(self, section):
        """Test generate with all data."""
        exoplanet = Exoplanet(
            pl_name="Test Planet",
            pl_mass=ValueWithUncertainty(value=1.0),
            pl_radius=ValueWithUncertainty(value=1.0),
            pl_temperature=ValueWithUncertainty(value=1000),
        )
        content = section.generate(exoplanet)
        assert "Masse_jovienne" in content
        assert "Rayon_jovien" in content
        assert "Kelvin" in content
        assert "L'exoplanète se distingue par" in content

    def test_generate_partial(self, section):
        """Test generate with partial data."""
        exoplanet = Exoplanet(
            pl_name="Test Planet",
            pl_mass=ValueWithUncertainty(value=1.0),
        )
        content = section.generate(exoplanet)
        assert "Masse_jovienne" in content
        assert "Rayon_jovien" not in content
