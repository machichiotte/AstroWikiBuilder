# tests/unit/test_generators/test_article_generators/test_star/test_sections/test_observation_section.py

"""Tests unitaires pour ObservationSection."""

from unittest.mock import MagicMock

import pytest

from src.generators.articles.star.sections.observation_section import ObservationSection
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
    star.st_apparent_magnitude = None
    star.st_right_ascension = None
    star.st_declination = None
    return star


class TestObservationSection:
    """Tests pour ObservationSection."""

    def test_observation_empty(self, article_util, mock_star):
        section = ObservationSection(article_util)
        assert section.generate(mock_star) == ""

    def test_observation_full(self, article_util, mock_star):
        mock_star.st_apparent_magnitude = ValueWithUncertainty(value=4.5)
        mock_star.st_right_ascension = "12/34/56.7"
        mock_star.st_declination = "+12/34/56.7"

        section = ObservationSection(article_util)
        content = section.generate(mock_star)

        assert "== Observation ==" in content
        assert "4,5" in content
        assert "{{ascension droite|12|34|56,7}}" in content
        assert "{{déclinaison|+12|34|56,7}}" in content
