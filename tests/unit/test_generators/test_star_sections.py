from unittest.mock import MagicMock, patch

import pytest

from src.generators.articles.star.sections.environment_section import EnvironmentSection
from src.generators.articles.star.sections.history_section import HistorySection
from src.generators.articles.star.sections.observation_section import ObservationSection
from src.generators.articles.star.sections.physical_characteristics_section import (
    PhysicalCharacteristicsSection,
)
from src.generators.articles.star.sections.planetary_system_section import (
    PlanetarySystemSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter


class TestStarSections:
    @pytest.fixture
    def article_util(self):
        util = MagicMock(spec=ArticleFormatter)
        util.format_number_as_french_string.side_effect = lambda x: f"{x}".replace(".", ",")
        return util

    @pytest.fixture
    def mock_star(self):
        star = MagicMock(spec=Star)
        star.st_name = "Kepler-186"
        star.st_spectral_type = None
        star.st_temperature = None
        star.st_mass = None
        star.st_radius = None
        star.st_luminosity = None
        star.st_apparent_magnitude = None
        star.st_right_ascension = None
        star.st_declination = None
        star.sy_constellation = None
        star.st_distance = None
        return star

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

    def test_history_empty(self, mock_star):
        mock_star.st_name = None
        section = HistorySection()
        assert section.generate(mock_star) == ""

    def test_history_full(self, mock_star):
        section = HistorySection()
        content = section.generate(mock_star)
        assert "== Histoire ==" in content
        assert "Kepler-186" in content

    def test_planetary_system_empty(self, article_util, mock_star):
        section = PlanetarySystemSection(article_util)
        assert section.generate(mock_star, []) == ""

    def test_planetary_system_full(self, article_util, mock_star):
        exoplanet = MagicMock(spec=Exoplanet)
        exoplanet.pl_name = "Kepler-186 f"
        exoplanet.pl_mass = ValueWithUncertainty(value=1.5)
        exoplanet.pl_radius = ValueWithUncertainty(value=1.1)
        exoplanet.pl_semi_major_axis = ValueWithUncertainty(value=0.4)
        exoplanet.pl_orbital_period = ValueWithUncertainty(value=129.9)
        exoplanet.pl_eccentricity = ValueWithUncertainty(value=0.04)
        exoplanet.pl_inclination = ValueWithUncertainty(value=89.9)

        section = PlanetarySystemSection(article_util)
        content = section.generate(mock_star, [exoplanet])

        assert "== Système planétaire ==" in content
        assert "{{Système planétaire début" in content
        assert "{{Système planétaire" in content
        assert "Kepler-186 f" in content
        assert "1.50" in content
        assert "1.10" in content
        assert "0.40" in content
        assert "129.90" in content
        assert "0.040" in content
        assert "89.90" in content
        assert "{{Système planétaire fin}}" in content

    def test_map_constellation_to_category(self, mock_star):
        from src.generators.articles.star.sections.category_section import (
            CategorySection,
        )

        # Mock the rules manager to return a known mapping
        section = CategorySection()
        section._category_rules_manager = MagicMock()
        section._category_rules_manager.rules = {
            "common": {
                "mapped": {"sy_constellation": {"Cygne": "[[Catégorie:Constellation du Cygne]]"}}
            }
        }

        mock_star.sy_constellation = "Cygne"
        result = section.map_constellation_to_category(mock_star)
        assert result == "[[Catégorie:Constellation du Cygne]]"

        mock_star.sy_constellation = "Unknown"
        result = section.map_constellation_to_category(mock_star)
        assert result is None
