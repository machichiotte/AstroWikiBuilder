# tests/unit/test_generators/test_article_generators/test_star/test_sections/test_physical_characteristics_section.py

"""Tests unitaires pour PhysicalCharacteristicsSection (étoiles)."""

from unittest.mock import MagicMock

import pytest

from src.generators.articles.star.sections.physical_characteristics_section import (
    PhysicalCharacteristicsSection,
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
    star.st_name = "Kepler-186"
    star.st_spectral_type = None
    star.st_temperature = None
    star.st_mass = None
    star.st_radius = None
    star.st_luminosity = None
    return star


class TestPhysicalCharacteristicsSection:
    """Tests pour PhysicalCharacteristicsSection (étoiles)."""

    def test_physical_characteristics_empty(self, article_util, mock_star):
        section = PhysicalCharacteristicsSection(article_util)
        assert section.generate(mock_star) == ""

    def test_physical_characteristics_full(self, article_util, mock_star):
        mock_star.st_spectral_type = "G2V"
        mock_star.st_temperature = ValueWithUncertainty(value=5778)
        mock_star.st_mass = ValueWithUncertainty(value=1.0)
        mock_star.st_radius = ValueWithUncertainty(value=1.0)
        mock_star.st_luminosity = ValueWithUncertainty(value=1.0)

        section = PhysicalCharacteristicsSection(article_util)
        content = section.generate(mock_star)

        assert "== Caractéristiques physiques ==" in content
        assert "type spectral G2V" in content
        assert "5778" in content
        assert "1,0" in content
