# tests/unit/test_generators/test_article_generators/test_exoplanet/test_sections/test_orbit_section.py

"""Tests unitaires pour OrbitSection."""

import pytest

from src.generators.articles.exoplanet.sections import OrbitSection
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.utils.formatters.article_formatter import ArticleFormatter


@pytest.fixture
def article_formatter():
    return ArticleFormatter()


@pytest.fixture
def exoplanet_with_orbit():
    """Exoplanète avec données orbitales complètes."""
    return Exoplanet(
        pl_name="Test Planet b",
        pl_semi_major_axis=ValueWithUncertainty(value=0.047),
        pl_eccentricity=ValueWithUncertainty(value=0.014),
        pl_orbital_period=ValueWithUncertainty(value=3.52),
        pl_inclination=ValueWithUncertainty(value=86.7),
    )


class TestOrbitSection:
    """Tests pour OrbitSection."""

    def test_orbit_section_complete(self, article_formatter, exoplanet_with_orbit):
        """Test de la section orbite avec toutes les données."""
        section = OrbitSection(article_formatter)
        result = section.generate(exoplanet_with_orbit)

        assert result != ""
        assert "== Orbite ==" in result
        assert "UA" in result
        assert "excentricité" in result
        assert "période orbitale" in result
        assert "inclinaison" in result

    def test_orbit_section_empty(self, article_formatter):
        """Test avec une exoplanète sans données orbitales."""
        exoplanet = Exoplanet(pl_name="Test b")
        section = OrbitSection(article_formatter)
        result = section.generate(exoplanet)

        assert result == ""

    def test_orbit_section_partial(self, article_formatter):
        """Test avec seulement certaines données orbitales."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_semi_major_axis=ValueWithUncertainty(value=1.0),
        )
        section = OrbitSection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "== Orbite ==" in result
        assert "UA" in result
