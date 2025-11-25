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

    def test_orbit_section_with_obliquity(self, article_formatter):
        """Test avec obliquité projetée et vraie."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_projobliq=ValueWithUncertainty(value=45.0),
            pl_trueobliq=ValueWithUncertainty(value=50.0),
        )
        section = OrbitSection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "obliquité projetée" in result
        assert "obliquité vraie" in result
        assert "45" in result
        assert "50" in result

    def test_orbit_section_with_impact_parameter(self, article_formatter):
        """Test avec paramètre d'impact."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_imppar=ValueWithUncertainty(value=0.5),
        )
        section = OrbitSection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "paramètre d'impact" in result
        assert "0,5" in result

    def test_orbit_section_with_geometric_ratios(self, article_formatter):
        """Test avec ratios géométriques."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_ratdor=ValueWithUncertainty(value=8.5),
            pl_ratror=ValueWithUncertainty(value=0.1),
        )
        section = OrbitSection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "a/R*" in result
        assert "Rp/R*" in result
        assert "8,5" in result
        assert "0,1" in result

    def test_orbit_section_with_all_new_parameters(self, article_formatter):
        """Test avec tous les nouveaux paramètres."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_projobliq=ValueWithUncertainty(value=30.0),
            pl_trueobliq=ValueWithUncertainty(value=35.0),
            pl_imppar=ValueWithUncertainty(value=0.3),
            pl_ratdor=ValueWithUncertainty(value=10.0),
            pl_ratror=ValueWithUncertainty(value=0.15),
        )
        section = OrbitSection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "obliquité projetée" in result
        assert "obliquité vraie" in result
        assert "paramètre d'impact" in result
        assert "a/R*" in result
        assert "Rp/R*" in result
