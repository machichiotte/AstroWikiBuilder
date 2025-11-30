from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.host_star_section import (
    HostStarSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


@pytest.fixture
def mock_article_formatter():
    formatter = Mock()
    formatter.format_uncertain_value_for_article.side_effect = lambda x: f"{x.value}"
    return formatter


def test_host_star_with_planetary_system(mock_article_formatter):
    """Test section étoile avec tableau système planétaire"""
    section = HostStarSection(mock_article_formatter)
    exoplanet = Exoplanet(
        pl_name="Kepler-10 b",
        st_name="Kepler-10",
        sy_planet_count=2,
        st_spectral_type="G",
        st_mass=ValueWithUncertainty(0.91),
    )

    content = section.generate(exoplanet)

    assert "== Étoile ==" in content
    assert "[[Kepler-10]]" in content
    assert "type spectral G" in content


def test_host_star_single_planet_no_table(mock_article_formatter):
    """Test section étoile sans tableau (1 seule planète)"""
    section = HostStarSection(mock_article_formatter)
    exoplanet = Exoplanet(
        pl_name="Test b",
        st_name="Test",
        sy_planet_count=1,
        st_spectral_type="K5V",
    )

    content = section.generate(exoplanet)

    assert "== Étoile ==" in content
    assert "[[Test]]" in content
    assert "{{Système planétaire" not in content


def test_host_star_with_all_characteristics(mock_article_formatter):
    """Test avec toutes les caractéristiques"""
    section = HostStarSection(mock_article_formatter)
    exoplanet = Exoplanet(
        pl_name="Test b",
        st_name="Test Star",
        sy_planet_count=3,
        st_spectral_type="G2V",
        st_mass=ValueWithUncertainty(1.0),
        st_metallicity=ValueWithUncertainty(0.1),
        st_age=ValueWithUncertainty(4.5),
    )

    content = section.generate(exoplanet)

    assert "type spectral G2V" in content
    assert "masse de 1.0" in content
    assert "métallicité de 0.1" in content
    assert "âgée de 4.5" in content


def test_host_star_empty(mock_article_formatter):
    """Test sans nom d'étoile"""
    section = HostStarSection(mock_article_formatter)
    exoplanet = Exoplanet(pl_name="Test b")

    content = section.generate(exoplanet)

    assert content == ""
