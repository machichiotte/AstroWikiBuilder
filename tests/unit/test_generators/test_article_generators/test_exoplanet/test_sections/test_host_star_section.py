# tests/unit/test_generators/test_article_generators/test_exoplanet/test_sections/test_host_star_section.py

"""Tests unitaires pour HostStarSection."""

import pytest

from src.generators.articles.exoplanet.sections import HostStarSection
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.utils.formatters.article_formatter import ArticleFormatter


@pytest.fixture
def article_formatter():
    return ArticleFormatter()


class TestHostStarSection:
    """Tests pour HostStarSection."""

    def test_host_star_section_empty(self, article_formatter):
        """Test avec étoile vide."""
        exoplanet = Exoplanet(pl_name="Test b")
        section = HostStarSection(article_formatter)
        result = section.generate(exoplanet)
        assert result == ""

    def test_host_star_section_name_only(self, article_formatter):
        """Test avec seulement le nom de l'étoile."""
        exoplanet = Exoplanet(pl_name="Test b", st_name="Test Star")
        section = HostStarSection(article_formatter)
        result = section.generate(exoplanet)
        assert "== Étoile hôte ==" in result
        assert "Test Star" in result
        assert "type spectral" not in result

    def test_host_star_section_full_info(self, article_formatter):
        """Test avec toutes les infos de l'étoile."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test Star",
            st_spectral_type="G2V",
            st_mass=ValueWithUncertainty(value=1.0),
            st_metallicity=ValueWithUncertainty(value=0.1),
            st_age=ValueWithUncertainty(value=4.5),
        )
        section = HostStarSection(article_formatter)
        result = section.generate(exoplanet)
        assert "== Étoile hôte ==" in result
        assert "Test Star" in result
        assert "G2V" in result
        assert "masse de 1" in result
        assert "métallicité de 0,1" in result
        assert "âgée de 4,5" in result

    def test_host_star_section_partial_info(self, article_formatter):
        """Test avec info partielle de l'étoile."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test Star",
            st_spectral_type="K5",
        )
        section = HostStarSection(article_formatter)
        result = section.generate(exoplanet)
        assert "== Étoile hôte ==" in result
        assert "type spectral K5" in result
        assert "masse" not in result
