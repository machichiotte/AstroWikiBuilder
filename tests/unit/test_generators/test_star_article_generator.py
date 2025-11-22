from unittest.mock import MagicMock

import pytest

from src.generators.articles.star.star_article_generator import (
    StarWikipediaArticleGenerator,
)
from src.models.entities.star_entity import Star


class TestStarWikipediaArticleGenerator:
    @pytest.fixture
    def generator(self):
        return StarWikipediaArticleGenerator()

    @pytest.fixture
    def mock_star(self):
        star = MagicMock(spec=Star)
        star.st_name = "Kepler-186"
        star.st_spectral_type = "M1V"
        star.sy_constellation = "Cygne"
        star.reference = None
        return star

    def test_init(self, generator):
        assert generator.stub_type == "étoile"
        assert generator.portals == ["astronomie", "étoiles", "exoplanètes"]
        assert generator.category_section is not None
        assert generator.infobox_section is not None
        assert generator.introduction_section is not None
        assert generator.physical_characteristics_section is not None
        assert generator.observation_section is not None
        assert generator.environment_section is not None
        assert generator.history_section is not None
        assert generator.planetary_system_section is not None

    def test_compose_wikipedia_article_content(self, generator, mock_star):
        # Mock all sub-generators to return simple strings
        generator.compose_stub_and_source = MagicMock(return_value="STUB")
        generator.infobox_section.generate = MagicMock(return_value="INFOBOX")
        generator.introduction_section.compose_star_introduction = MagicMock(return_value="INTRO")
        generator.physical_characteristics_section.generate = MagicMock(return_value="PHYSICAL")
        generator.observation_section.generate = MagicMock(return_value="OBSERVATION")
        generator.environment_section.generate = MagicMock(return_value="ENVIRONMENT")
        generator.history_section.generate = MagicMock(return_value="HISTORY")
        generator.planetary_system_section.generate = MagicMock(return_value="PLANETS")
        generator.build_references_section = MagicMock(return_value="REFS")
        generator.build_palettes_section = MagicMock(return_value="PALETTES")
        generator.build_portails_section = MagicMock(return_value="PORTALS")
        generator.build_category_section = MagicMock(return_value="CATEGORIES")

        content = generator.compose_wikipedia_article_content(mock_star)

        assert "STUB" in content
        assert "INFOBOX" in content
        assert "INTRO" in content
        assert "PHYSICAL" in content
        assert "OBSERVATION" in content
        assert "ENVIRONMENT" in content
        assert "HISTORY" in content
        assert "PLANETS" in content
        assert "REFS" in content
        assert "PALETTES" in content
        assert "PORTALS" in content
        assert "CATEGORIES" in content

    def test_build_palettes_section_valid(self, generator, mock_star):
        mock_star.sy_constellation = "Cygne"
        result = generator.build_palettes_section(mock_star)
        assert "{{Palette|Étoiles du Cygne}}" in result

    def test_build_palettes_section_invalid(self, generator, mock_star):
        mock_star.sy_constellation = "Unknown"
        result = generator.build_palettes_section(mock_star)
        assert result is None
