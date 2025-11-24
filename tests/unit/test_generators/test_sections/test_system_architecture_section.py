"""Tests for SystemArchitectureSection."""

from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.system_architecture_section import (
    SystemArchitectureSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


class TestSystemArchitectureSection:
    """Test suite for SystemArchitectureSection."""

    @pytest.fixture
    def section(self):
        """Create a SystemArchitectureSection instance with mocked dependencies."""
        article_util = Mock()
        return SystemArchitectureSection(article_util)

    def test_generate_no_count(self, section):
        """Test generate with no planet count."""
        exoplanet = Exoplanet(pl_name="Test Planet", sy_planet_count=None)
        assert section.generate(exoplanet) == ""

    def test_generate_invalid_count(self, section):
        """Test generate with invalid planet count."""
        exoplanet = Exoplanet(pl_name="Test Planet", sy_planet_count="invalid")
        assert section.generate(exoplanet) == ""

    def test_generate_single_planet(self, section):
        """Test generate with single planet system."""
        exoplanet = Exoplanet(pl_name="Test Planet", sy_planet_count=1)
        assert section.generate(exoplanet) == ""

    def test_generate_binary_system(self, section):
        """Test generate with 2 planets."""
        exoplanet = Exoplanet(pl_name="Test Planet", st_name="Star", sy_planet_count=2)
        content = section.generate(exoplanet)
        assert "système binaire" in content
        assert "[[Star]]" in content

    def test_generate_medium_system(self, section):
        """Test generate with 3-5 planets."""
        exoplanet = Exoplanet(pl_name="Test Planet", st_name="Star", sy_planet_count=4)
        content = section.generate(exoplanet)
        assert "système de 4 planètes" in content

    def test_generate_large_system(self, section):
        """Test generate with >5 planets."""
        exoplanet = Exoplanet(pl_name="Test Planet", st_name="Star", sy_planet_count=7)
        content = section.generate(exoplanet)
        assert "système planétaire remarquable" in content
        assert "7 planètes" in content

    def test_generate_count_as_value_object(self, section):
        """Test generate with planet count as ValueWithUncertainty."""
        count = ValueWithUncertainty(value=3)
        exoplanet = Exoplanet(pl_name="Test Planet", st_name="Star", sy_planet_count=count)
        content = section.generate(exoplanet)
        assert "système de 3 planètes" in content

    def test_generate_with_siblings_fallback(self, section):
        """Test fallback when siblings list is small."""
        exoplanet = Exoplanet(pl_name="Test Planet", sy_planet_count=1)
        # List has only 1 planet, so should fallback to count logic (which returns empty for 1)
        assert section.generate(exoplanet, [exoplanet]) == ""

    def test_generate_with_siblings_inner(self, section):
        """Test with siblings, current planet is inner."""
        p1 = Exoplanet(
            pl_name="P1", st_name="Star", pl_semi_major_axis=ValueWithUncertainty(value=1.0)
        )
        p2 = Exoplanet(
            pl_name="P2", st_name="Star", pl_semi_major_axis=ValueWithUncertainty(value=2.0)
        )
        p3 = Exoplanet(
            pl_name="P3", st_name="Star", pl_semi_major_axis=ValueWithUncertainty(value=3.0)
        )

        content = section.generate(p1, [p1, p2, p3])
        assert "la plus interne" in content
        assert "Les autres planètes du système sont [[P2]] et [[P3]]" in content

    def test_generate_with_siblings_outer(self, section):
        """Test with siblings, current planet is outer."""
        p1 = Exoplanet(
            pl_name="P1", st_name="Star", pl_semi_major_axis=ValueWithUncertainty(value=1.0)
        )
        p2 = Exoplanet(
            pl_name="P2", st_name="Star", pl_semi_major_axis=ValueWithUncertainty(value=2.0)
        )

        content = section.generate(p2, [p1, p2])
        assert "la plus externe" in content
        assert "L'autre planète connue du système est [[P1]]" in content

    def test_generate_with_siblings_middle(self, section):
        """Test with siblings, current planet is in middle."""
        p1 = Exoplanet(
            pl_name="P1", st_name="Star", pl_semi_major_axis=ValueWithUncertainty(value=1.0)
        )
        p2 = Exoplanet(
            pl_name="P2", st_name="Star", pl_semi_major_axis=ValueWithUncertainty(value=2.0)
        )
        p3 = Exoplanet(
            pl_name="P3", st_name="Star", pl_semi_major_axis=ValueWithUncertainty(value=3.0)
        )

        content = section.generate(p2, [p1, p2, p3])
        assert "la 2e planète" in content

    def test_generate_with_siblings_sorting_fallback(self, section):
        """Test sorting by name when axis missing."""
        p1 = Exoplanet(pl_name="A", st_name="Star")
        p2 = Exoplanet(pl_name="B", st_name="Star")

        content = section.generate(p1, [p2, p1])  # Passed unsorted
        # Should be sorted A, B. A is first (inner)
        assert "la plus interne" in content

    def test_generate_with_siblings_not_found(self, section):
        """Test when current planet not in list (should not happen but handled)."""
        p1 = Exoplanet(pl_name="P1", st_name="Star")
        p2 = Exoplanet(pl_name="P2", st_name="Star")

        # p1 is not in the list passed
        content = section._generate_with_siblings(p1, [p2])
        # Should not crash, just missing position sentence
        assert f"[[{p1.pl_name}]] est" not in content
        # But it will list others
        assert "L'autre planète connue du système est [[P2]]" in content
