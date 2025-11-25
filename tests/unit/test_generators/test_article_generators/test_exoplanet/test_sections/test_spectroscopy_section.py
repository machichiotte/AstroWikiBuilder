# tests/unit/test_generators/test_article_generators/test_exoplanet/test_sections/test_spectroscopy_section.py

"""Tests unitaires pour SpectroscopySection."""

import pytest

from src.generators.articles.exoplanet.sections import SpectroscopySection
from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


@pytest.fixture
def article_formatter():
    return ArticleFormatter()


class TestSpectroscopySection:
    """Tests pour SpectroscopySection."""

    def test_spectroscopy_section_with_transmission(self, article_formatter):
        """Test avec spectres de transmission."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_ntranspec=3,
        )
        section = SpectroscopySection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "== Spectroscopie ==" in result
        assert "transmission" in result
        assert "3 spectres" in result

    def test_spectroscopy_section_with_eclipse(self, article_formatter):
        """Test avec spectres d'éclipse."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_nespec=2,
        )
        section = SpectroscopySection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "éclipse" in result
        assert "2 spectres" in result

    def test_spectroscopy_section_with_direct_imaging(self, article_formatter):
        """Test avec spectres d'imagerie directe."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_ndispec=1,
        )
        section = SpectroscopySection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "imagerie directe" in result
        assert "1 spectre" in result

    def test_spectroscopy_section_with_all_types(self, article_formatter):
        """Test avec tous les types de spectres."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_ntranspec=5,
            pl_nespec=3,
            pl_ndispec=2,
        )
        section = SpectroscopySection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "transmission" in result
        assert "éclipse" in result
        assert "imagerie directe" in result

    def test_spectroscopy_section_empty(self, article_formatter):
        """Test sans données spectroscopiques."""
        exoplanet = Exoplanet(pl_name="Test b")
        section = SpectroscopySection(article_formatter)
        result = section.generate(exoplanet)

        assert result == ""

    def test_spectroscopy_section_with_zero_spectra(self, article_formatter):
        """Test avec zéro spectres."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_ntranspec=0,
            pl_nespec=0,
        )
        section = SpectroscopySection(article_formatter)
        result = section.generate(exoplanet)

        assert result == ""
