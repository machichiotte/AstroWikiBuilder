# tests/unit/test_generators/test_article_generators/test_star/test_sections/test_photometry_section.py

"""Tests unitaires pour PhotometrySection (étoiles)."""

from unittest.mock import MagicMock

import pytest

from src.generators.articles.star.sections.photometry_section import (
    PhotometrySection,
)
from src.models.entities.exoplanet_entity import ValueWithUncertainty
from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter


@pytest.fixture
def article_util():
    util = MagicMock(spec=ArticleFormatter)
    util.format_number_as_french_string.side_effect = lambda x: f"{x}".replace(".", ",")
    return util


@pytest.fixture
def mock_star():
    star = MagicMock(spec=Star)
    star.st_name = "Test Star"
    star.st_mag_u = None
    star.st_mag_b = None
    star.st_mag_v = None
    star.st_mag_g = None
    star.st_mag_r = None
    star.st_mag_i = None
    star.st_mag_j = None
    star.st_mag_h = None
    star.st_mag_k = None
    # Phase 2 fields
    star.st_mag_w1 = None
    star.st_mag_w2 = None
    star.st_mag_w3 = None
    star.st_mag_w4 = None
    star.st_mag_gaia = None
    star.st_mag_t = None
    star.st_mag_kep = None
    return star


class TestPhotometrySection:
    """Tests pour PhotometrySection (étoiles)."""

    def test_photometry_empty(self, article_util, mock_star):
        """Test sans données photométriques."""
        section = PhotometrySection(article_util)
        assert section.generate(mock_star) == ""

    def test_photometry_with_johnson_bands(self, article_util, mock_star):
        """Test avec bandes Johnson (U, B, V)."""
        mock_star.st_mag_u = ValueWithUncertainty(value=10.5)
        mock_star.st_mag_b = ValueWithUncertainty(value=11.2)
        mock_star.st_mag_v = ValueWithUncertainty(value=10.8)

        section = PhotometrySection(article_util)
        content = section.generate(mock_star)

        assert "== Photométrie ==" in content
        assert "wikitable" in content
        assert "Johnson" in content
        assert "10,5" in content
        assert "11,2" in content
        assert "10,8" in content

    def test_photometry_with_sloan_bands(self, article_util, mock_star):
        """Test avec bandes Sloan (g, r, i)."""
        mock_star.st_mag_g = ValueWithUncertainty(value=12.3)
        mock_star.st_mag_r = ValueWithUncertainty(value=11.9)
        mock_star.st_mag_i = ValueWithUncertainty(value=11.5)

        section = PhotometrySection(article_util)
        content = section.generate(mock_star)

        assert "== Photométrie ==" in content
        assert "Sloan" in content
        assert "12,3" in content
        assert "11,9" in content
        assert "11,5" in content

    def test_photometry_with_2mass_bands(self, article_util, mock_star):
        """Test avec bandes 2MASS (J, H, K)."""
        mock_star.st_mag_j = ValueWithUncertainty(value=9.5)
        mock_star.st_mag_h = ValueWithUncertainty(value=9.1)
        mock_star.st_mag_k = ValueWithUncertainty(value=8.9)

        section = PhotometrySection(article_util)
        content = section.generate(mock_star)

        assert "== Photométrie ==" in content
        assert "2MASS" in content
        assert "9,5" in content
        assert "9,1" in content
        assert "8,9" in content

    def test_photometry_with_all_bands(self, article_util, mock_star):
        """Test avec toutes les bandes."""
        mock_star.st_mag_u = ValueWithUncertainty(value=10.5)
        mock_star.st_mag_b = ValueWithUncertainty(value=11.2)
        mock_star.st_mag_v = ValueWithUncertainty(value=10.8)
        mock_star.st_mag_g = ValueWithUncertainty(value=12.3)
        mock_star.st_mag_r = ValueWithUncertainty(value=11.9)
        mock_star.st_mag_i = ValueWithUncertainty(value=11.5)
        mock_star.st_mag_j = ValueWithUncertainty(value=9.5)
        mock_star.st_mag_h = ValueWithUncertainty(value=9.1)
        mock_star.st_mag_k = ValueWithUncertainty(value=8.9)

        section = PhotometrySection(article_util)
        content = section.generate(mock_star)

        assert "== Photométrie ==" in content
        assert "Johnson" in content
        assert "Sloan" in content
        assert "2MASS" in content
        # Vérifier que le tableau est bien formé
        assert '{| class="wikitable"' in content
        assert "! Bande !! Magnitude !! Système" in content
        assert "|}" in content

    def test_photometry_with_uncertainties(self, article_util, mock_star):
        """Test avec incertitudes."""
        mock_star.st_mag_v = ValueWithUncertainty(
            value=10.8, error_positive=0.1, error_negative=0.1
        )

        section = PhotometrySection(article_util)
        content = section.generate(mock_star)

        assert "10,8" in content
        assert "±" in content or "0,1" in content
