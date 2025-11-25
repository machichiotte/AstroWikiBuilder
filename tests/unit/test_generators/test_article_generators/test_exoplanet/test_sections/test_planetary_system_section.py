"""Tests for PlanetarySystemSection."""

from unittest.mock import Mock

import pytest

from src.generators.articles.star.sections.planetary_system_section import (
    PlanetarySystemSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.entities.star_entity import Star


class TestPlanetarySystemSection:
    """Test suite for PlanetarySystemSection."""

    @pytest.fixture
    def section(self):
        """Create a PlanetarySystemSection instance with mocked dependencies."""
        article_util = Mock()
        return PlanetarySystemSection(article_util)

    def test_generate_no_exoplanets(self, section):
        """Test generate with empty exoplanet list."""
        star = Star(st_name="Test Star")
        assert section.generate(star, []) == ""

    def test_generate_with_exoplanets_sorting(self, section):
        """Test generate sorts exoplanets by semi-major axis."""
        star = Star(st_name="Test Star")

        exo1 = Exoplanet(pl_name="Planet B", pl_semi_major_axis=ValueWithUncertainty(value=2.0))
        exo2 = Exoplanet(pl_name="Planet A", pl_semi_major_axis=ValueWithUncertainty(value=1.0))

        content = section.generate(star, [exo1, exo2])

        # Planet A should appear before Planet B
        pos_a = content.find("Planet A")
        pos_b = content.find("Planet B")
        assert pos_a < pos_b

    def test_generate_with_exoplanets_sorting_fallback(self, section):
        """Test generate sorts by name when semi-major axis is missing."""
        star = Star(st_name="Test Star")

        exo1 = Exoplanet(pl_name="Planet B", pl_semi_major_axis=None)
        exo2 = Exoplanet(pl_name="Planet A", pl_semi_major_axis=None)

        content = section.generate(star, [exo1, exo2])

        # Planet A should appear before Planet B
        pos_a = content.find("Planet A")
        pos_b = content.find("Planet B")
        assert pos_a < pos_b

    def test_generate_with_exoplanets_sorting_invalid_axis(self, section):
        """Test generate sorts by name when semi-major axis is invalid."""
        star = Star(st_name="Test Star")

        exo1 = Exoplanet(
            pl_name="Planet B", pl_semi_major_axis=ValueWithUncertainty(value="invalid")
        )
        exo2 = Exoplanet(pl_name="Planet A", pl_semi_major_axis=ValueWithUncertainty(value=1.0))

        content = section.generate(star, [exo1, exo2])

        # Planet A (valid axis 1.0) should be first (priority 0)
        # Planet B (invalid axis) should be second (priority 1)
        pos_a = content.find("Planet A")
        pos_b = content.find("Planet B")
        assert pos_a < pos_b

    def test_format_field_with_uncertainty_invalid(self, section):
        """Test formatting with invalid value."""
        val = ValueWithUncertainty(value="invalid")
        assert section._format_field_with_uncertainty(val) == ""

    def test_format_field_with_uncertainty_none(self, section):
        """Test formatting with None value."""
        val = ValueWithUncertainty(value=None)
        assert section._format_field_with_uncertainty(val) == ""

    def test_format_uncertainty_symmetric(self, section):
        """Test formatting with symmetric uncertainty."""
        # 1.0 +/- 0.1
        result = section._format_uncertainty(1.0, 0.1, 0.1)
        assert "1 {{±|0,1}}" in result

    def test_format_uncertainty_asymmetric(self, section):
        """Test formatting with asymmetric uncertainty."""
        # 1.0 +0.2 -0.1
        result = section._format_uncertainty(1.0, 0.2, 0.1)
        assert "1 {{±|0,2|0,1}}" in result

    def test_format_uncertainty_positive_only(self, section):
        """Test formatting with only positive uncertainty."""
        result = section._format_uncertainty(1.0, 0.1, None)
        assert "1 +0,1" in result

    def test_format_uncertainty_negative_only(self, section):
        """Test formatting with only negative uncertainty."""
        result = section._format_uncertainty(1.0, None, 0.1)
        assert "1 -0,1" in result

    def test_format_uncertainty_none(self, section):
        """Test formatting with no uncertainty."""
        result = section._format_uncertainty(1.0, None, None)
        assert result == "1"

    def test_to_french_decimal(self, section):
        """Test french decimal formatting."""
        assert section._to_french_decimal(1.5) == "1,5"
        assert section._to_french_decimal(1.0) == "1"
        assert section._to_french_decimal(1.23456, precision=2) == "1,23"
