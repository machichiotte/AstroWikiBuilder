# tests/unit/test_generators/test_article_generators/test_star/test_sections/test_history_section.py

"""Tests unitaires pour HistorySection."""

from unittest.mock import MagicMock

import pytest

from src.generators.articles.star.sections.history_section import HistorySection
from src.models.entities.star_entity import Star


@pytest.fixture
def mock_star():
    star = MagicMock(spec=Star)
    star.st_name = "Kepler-186"
    return star


class TestHistorySection:
    """Tests pour HistorySection."""

    def test_history_empty(self, mock_star):
        mock_star.st_name = None
        section = HistorySection()
        assert section.generate(mock_star) == ""

    def test_history_full(self, mock_star):
        section = HistorySection()
        content = section.generate(mock_star)
        assert "== Histoire ==" in content
        assert "Kepler-186" in content
