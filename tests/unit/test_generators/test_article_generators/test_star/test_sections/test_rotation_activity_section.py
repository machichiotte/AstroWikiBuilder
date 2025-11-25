# tests/unit/test_generators/test_article_generators/test_star/test_sections/test_rotation_activity_section.py

"""Tests unitaires pour RotationActivitySection (étoiles)."""

from unittest.mock import MagicMock

import pytest

from src.generators.articles.star.sections.rotation_activity_section import (
    RotationActivitySection,
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
    star.st_rotation = None
    star.st_vsin = None
    star.st_radial_velocity = None
    return star


class TestRotationActivitySection:
    """Tests pour RotationActivitySection (étoiles)."""

    def test_rotation_activity_empty(self, article_util, mock_star):
        """Test sans données de rotation/activité."""
        section = RotationActivitySection(article_util)
        assert section.generate(mock_star) == ""

    def test_rotation_activity_with_rotation_period(self, article_util, mock_star):
        """Test avec période de rotation."""
        mock_star.st_rotation = ValueWithUncertainty(value=25.4)

        section = RotationActivitySection(article_util)
        content = section.generate(mock_star)

        assert "== Rotation et activité ==" in content
        assert "période de rotation" in content
        assert "25,4" in content
        assert "jours" in content

    def test_rotation_activity_with_vsin(self, article_util, mock_star):
        """Test avec vitesse de rotation projetée."""
        mock_star.st_vsin = ValueWithUncertainty(value=4.5)

        section = RotationActivitySection(article_util)
        content = section.generate(mock_star)

        assert "== Rotation et activité ==" in content
        assert "v sin i" in content
        assert "4,5" in content
        assert "km/s" in content

    def test_rotation_activity_with_radial_velocity(self, article_util, mock_star):
        """Test avec vitesse radiale."""
        mock_star.st_radial_velocity = ValueWithUncertainty(value=-12.3)

        section = RotationActivitySection(article_util)
        content = section.generate(mock_star)

        assert "== Rotation et activité ==" in content
        assert "vitesse radiale systémique" in content
        assert "-12,3" in content
        assert "km/s" in content

    def test_rotation_activity_with_all_fields(self, article_util, mock_star):
        """Test avec tous les champs."""
        mock_star.st_rotation = ValueWithUncertainty(value=25.4)
        mock_star.st_vsin = ValueWithUncertainty(value=4.5)
        mock_star.st_radial_velocity = ValueWithUncertainty(value=-12.3)

        section = RotationActivitySection(article_util)
        content = section.generate(mock_star)

        assert "== Rotation et activité ==" in content
        assert "période de rotation" in content
        assert "v sin i" in content
        assert "vitesse radiale systémique" in content
        assert "25,4" in content
        assert "4,5" in content
        assert "-12,3" in content
