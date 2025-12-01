# tests/unit/test_generators/test_article_generators/test_exoplanet/test_sections/test_category_section.py

"""Tests unitaires pour CategorySection (exoplanètes)."""

import pytest

from src.generators.articles.exoplanet.sections import CategorySection
from src.models.entities.exoplanet_entity import Exoplanet


@pytest.fixture
def exoplanet():
    return Exoplanet(pl_name="Test b", st_name="Test")


class TestCategorySection:
    """Tests pour CategorySection (exoplanètes)."""

    def test_generate(self, exoplanet):
        """Test basique de génération."""
        section = CategorySection()
        result = section.generate(exoplanet)
        # Should return categories
        assert result != ""

    def test_categories_format(self, exoplanet):
        """Test que les catégories sont correctement formatées sans double préfixe."""
        section = CategorySection()
        result = section.generate(exoplanet)

        # Vérifier qu'il n'y a pas de double [[Catégorie:
        assert "[[Catégorie:[[Catégorie:" not in result

        # Vérifier que toutes les lignes commencent par [[Catégorie:
        for line in result.split("\n"):
            if line.strip():
                assert line.startswith("[[Catégorie:")
                assert line.endswith("]]")
