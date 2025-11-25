# tests/unit/test_generators/test_article_generators/test_star/test_sections/test_environment_section.py

"""Tests unitaires pour EnvironmentSection."""

from unittest.mock import MagicMock, patch

import pytest

from src.generators.articles.star.sections.environment_section import EnvironmentSection
from src.models.entities.exoplanet_entity import ValueWithUncertainty
from src.models.entities.star_entity import Star


@pytest.fixture
def mock_star():
    star = MagicMock(spec=Star)
    star.st_name = "Kepler-186"
    star.sy_constellation = None
    star.st_distance = None
    return star


class TestEnvironmentSection:
    """Tests pour EnvironmentSection."""

    def test_environment_empty(self, mock_star):
        section = EnvironmentSection()
        assert section.generate(mock_star) == ""

    @patch("src.generators.articles.star.sections.environment_section.phrase_dans_constellation")
    def test_environment_full(self, mock_phrase, mock_star):
        mock_star.sy_constellation = "Cygne"
        mock_star.st_distance = ValueWithUncertainty(value=150.5)
        mock_phrase.return_value = "dans la constellation du Cygne"

        section = EnvironmentSection()
        content = section.generate(mock_star)

        assert "== Environnement stellaire ==" in content
        assert "dans la constellation du Cygne" in content
        assert "{{unité|150.50|[[parsec]]s}}" in content
