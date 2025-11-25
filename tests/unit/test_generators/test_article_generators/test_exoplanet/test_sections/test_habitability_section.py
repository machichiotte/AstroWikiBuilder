# tests/unit/test_generators/test_article_generators/test_exoplanet/test_sections/test_habitability_section.py

"""Tests unitaires pour HabitabilitySection."""

import pytest

from src.generators.articles.exoplanet.sections import HabitabilitySection
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.utils.formatters.article_formatter import ArticleFormatter


@pytest.fixture
def article_formatter():
    return ArticleFormatter()


class TestHabitabilitySection:
    """Tests pour HabitabilitySection."""

    def test_habitability_section_unknown(self, article_formatter):
        """Test habitabilité inconnue."""
        exoplanet = Exoplanet(pl_name="Test b")
        section = HabitabilitySection(article_formatter)
        result = section.generate(exoplanet)
        assert "ne sont pas déterminées" in result

    def test_habitability_section_too_hot(self, article_formatter):
        """Test habitabilité trop chaud."""
        exoplanet = Exoplanet(pl_name="Hot b", pl_temperature=ValueWithUncertainty(value=500))
        section = HabitabilitySection(article_formatter)
        result = section.generate(exoplanet)
        assert "trop chaude" in result
        assert "500" in result

    def test_habitability_section_too_cold(self, article_formatter):
        """Test habitabilité trop froid."""
        exoplanet = Exoplanet(pl_name="Cold b", pl_temperature=ValueWithUncertainty(value=100))
        section = HabitabilitySection(article_formatter)
        result = section.generate(exoplanet)
        assert "trop froide" in result
        assert "100" in result

    def test_habitability_section_habitable(self, article_formatter):
        """Test zone habitable théorique."""
        exoplanet = Exoplanet(pl_name="Earth 2.0", pl_temperature=ValueWithUncertainty(value=288))
        section = HabitabilitySection(article_formatter)
        result = section.generate(exoplanet)
        assert "zone habitable" in result
        assert "288" in result
