# tests/unit/test_generators/test_article_generators/test_star/test_sections/test_astrometry_section.py

"""Tests unitaires pour AstrometrySection (étoiles)."""

from unittest.mock import MagicMock

import pytest

from src.generators.articles.star.sections.astrometry_section import (
    AstrometrySection,
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
    star.st_proper_motion_ra = None
    star.st_proper_motion_dec = None
    star.st_parallax = None
    star.st_distance = None
    star.glon = None
    star.glat = None
    return star


class TestAstrometrySection:
    """Tests pour AstrometrySection (étoiles)."""

    def test_astrometry_empty(self, article_util, mock_star):
        """Test sans données astrométriques."""
        section = AstrometrySection(article_util)
        assert section.generate(mock_star) == ""

    def test_astrometry_with_proper_motion(self, article_util, mock_star):
        """Test avec mouvement propre."""
        mock_star.st_proper_motion_ra = ValueWithUncertainty(value=12.5)
        mock_star.st_proper_motion_dec = ValueWithUncertainty(value=-8.3)

        section = AstrometrySection(article_util)
        content = section.generate(mock_star)

        assert "== Astrométrie ==" in content
        assert "mouvement propre" in content
        assert "12,5" in content
        assert "-8,3" in content
        assert "mas/an" in content

    def test_astrometry_with_parallax(self, article_util, mock_star):
        """Test avec parallaxe."""
        mock_star.st_parallax = ValueWithUncertainty(value=45.2)

        section = AstrometrySection(article_util)
        content = section.generate(mock_star)

        assert "== Astrométrie ==" in content
        assert "parallaxe" in content
        assert "45,2" in content
        assert "mas" in content

    def test_astrometry_with_distance(self, article_util, mock_star):
        """Test avec distance."""
        mock_star.st_distance = ValueWithUncertainty(value=22.1)

        section = AstrometrySection(article_util)
        content = section.generate(mock_star)

        assert "== Astrométrie ==" in content
        assert "distance" in content
        assert "22,1" in content
        assert "pc" in content

    def test_astrometry_with_galactic_coordinates(self, article_util, mock_star):
        """Test avec coordonnées galactiques."""
        mock_star.glon = ValueWithUncertainty(value=123.45)
        mock_star.glat = ValueWithUncertainty(value=-15.67)

        section = AstrometrySection(article_util)
        content = section.generate(mock_star)

        assert "== Astrométrie ==" in content
        assert "longitude galactique" in content
        assert "latitude galactique" in content
        assert "123,45" in content
        assert "-15,67" in content

    def test_astrometry_with_all_fields(self, article_util, mock_star):
        """Test avec tous les champs."""
        mock_star.st_proper_motion_ra = ValueWithUncertainty(value=12.5)
        mock_star.st_proper_motion_dec = ValueWithUncertainty(value=-8.3)
        mock_star.st_parallax = ValueWithUncertainty(value=45.2)
        mock_star.st_distance = ValueWithUncertainty(value=22.1)
        mock_star.glon = ValueWithUncertainty(value=123.45)
        mock_star.glat = ValueWithUncertainty(value=-15.67)

        section = AstrometrySection(article_util)
        content = section.generate(mock_star)

        assert "== Astrométrie ==" in content
        assert "mouvement propre" in content
        assert "parallaxe" in content
        assert "distance" in content
        assert "longitude galactique" in content
        assert "latitude galactique" in content
