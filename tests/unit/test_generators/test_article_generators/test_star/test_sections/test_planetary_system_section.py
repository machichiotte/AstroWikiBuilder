# tests/unit/test_generators/test_article_generators/test_star/test_sections/test_planetary_system_section.py

"""Tests unitaires pour PlanetarySystemSection."""

from unittest.mock import MagicMock

import pytest

from src.generators.articles.star.sections.planetary_system_section import (
    PlanetarySystemSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
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
    return star


class TestPlanetarySystemSection:
    """Tests pour PlanetarySystemSection."""

    def test_planetary_system_empty(self, article_util, mock_star):
        section = PlanetarySystemSection(article_util)
        assert section.generate(mock_star, []) == ""

    def test_planetary_system_full(self, article_util, mock_star):
        exoplanet = MagicMock(spec=Exoplanet)
        exoplanet.pl_name = "Kepler-186 f"
        exoplanet.sy_snum = None
        exoplanet.cb_flag = None
        exoplanet.sy_mnum = None
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
        # French decimal format uses commas
        assert "1,5" in content  # masse
        assert "1,1" in content  # rayon
        assert "0,4" in content  # demi-grand axe
        assert "129,9" in content  # période
        assert "0,04" in content  # excentricité
        assert "89,9" in content  # inclinaison
        assert "{{Système planétaire fin}}" in content

    def test_planetary_system_with_multiple_stars(self, article_util, mock_star):
        """Test avec système multi-stellaire."""
        exoplanet = MagicMock(spec=Exoplanet)
        exoplanet.pl_name = "Test b"
        exoplanet.sy_snum = 2
        exoplanet.cb_flag = None
        exoplanet.sy_mnum = None
        exoplanet.pl_mass = None
        exoplanet.pl_radius = None
        exoplanet.pl_semi_major_axis = None
        exoplanet.pl_orbital_period = None
        exoplanet.pl_eccentricity = None
        exoplanet.pl_inclination = None

        section = PlanetarySystemSection(article_util)
        content = section.generate(mock_star, [exoplanet])

        assert "2 étoiles" in content

    def test_planetary_system_with_circumbinary(self, article_util, mock_star):
        """Test avec planètes circumbinaires."""
        exoplanet = MagicMock(spec=Exoplanet)
        exoplanet.pl_name = "Test b"
        exoplanet.sy_snum = None
        exoplanet.cb_flag = 1
        exoplanet.sy_mnum = None
        exoplanet.pl_mass = None
        exoplanet.pl_radius = None
        exoplanet.pl_semi_major_axis = None
        exoplanet.pl_orbital_period = None
        exoplanet.pl_eccentricity = None
        exoplanet.pl_inclination = None

        section = PlanetarySystemSection(article_util)
        content = section.generate(mock_star, [exoplanet])

        assert "circumbinaires" in content

    def test_planetary_system_with_moons(self, article_util, mock_star):
        """Test avec lunes."""
        exoplanet = MagicMock(spec=Exoplanet)
        exoplanet.pl_name = "Test b"
        exoplanet.sy_snum = None
        exoplanet.cb_flag = None
        exoplanet.sy_mnum = 3
        exoplanet.pl_mass = None
        exoplanet.pl_radius = None
        exoplanet.pl_semi_major_axis = None
        exoplanet.pl_orbital_period = None
        exoplanet.pl_eccentricity = None
        exoplanet.pl_inclination = None

        section = PlanetarySystemSection(article_util)
        content = section.generate(mock_star, [exoplanet])

        assert "3 lunes" in content

    def test_planetary_system_with_all_system_info(self, article_util, mock_star):
        """Test avec toutes les informations système."""
        exoplanet = MagicMock(spec=Exoplanet)
        exoplanet.pl_name = "Test b"
        exoplanet.sy_snum = 2
        exoplanet.cb_flag = 1
        exoplanet.sy_mnum = 1
        exoplanet.pl_mass = None
        exoplanet.pl_radius = None
        exoplanet.pl_semi_major_axis = None
        exoplanet.pl_orbital_period = None
        exoplanet.pl_eccentricity = None
        exoplanet.pl_inclination = None

        section = PlanetarySystemSection(article_util)
        content = section.generate(mock_star, [exoplanet])

        assert "2 étoiles" in content
        assert "circumbinaires" in content
        assert "1 lune" in content
