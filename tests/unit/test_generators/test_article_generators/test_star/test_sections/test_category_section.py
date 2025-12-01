# tests/unit/test_generators/test_article_generators/test_star/test_sections/test_category_section.py

"""Tests unitaires pour CategorySection (étoiles)."""

from unittest.mock import MagicMock

import pytest

from src.generators.articles.star.sections.category_section import CategorySection
from src.models.entities.star_entity import Star


@pytest.fixture
def mock_star():
    star = MagicMock(spec=Star)
    star.st_name = "Kepler-186"
    star.sy_constellation = None
    star.st_altname = []
    star.st_spectype = None
    return star


class TestCategorySection:
    """Tests pour CategorySection (étoiles)."""

    def test_map_constellation_to_category(self, mock_star):
        # Mock the rules manager to return a known mapping
        section = CategorySection()
        section._category_rules_manager = MagicMock()
        section._category_rules_manager.rules = {
            "common": {"mapped": {"sy_constellation": {"Cygne": "Constellation du Cygne"}}}
        }

        mock_star.sy_constellation = "Cygne"
        result = section.map_constellation_to_category(mock_star)
        assert result == "Constellation du Cygne"

        mock_star.sy_constellation = "Unknown"
        result = section.map_constellation_to_category(mock_star)
        assert result is None

    def test_categories_format(self, mock_star):
        """Test que les catégories sont correctement formatées sans double préfixe."""
        section = CategorySection()
        result = section.generate(mock_star)

        # Vérifier qu'il n'y a pas de double [[Catégorie:
        assert "[[Catégorie:[[Catégorie:" not in result

        # Vérifier que toutes les lignes commencent par [[Catégorie:
        for line in result.split("\n"):
            if line.strip():
                assert line.startswith("[[Catégorie:")
                assert line.endswith("]]")
