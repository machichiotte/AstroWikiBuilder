from unittest.mock import Mock

import pytest

from src.generators.articles.star.sections.physical_characteristics_section import (
    PhysicalCharacteristicsSection,
)
from src.models.entities.star_entity import Star, ValueWithUncertainty


@pytest.fixture
def mock_article_formatter():
    formatter = Mock()
    formatter.format_number_as_french_string.side_effect = lambda x, **kwargs: str(x).replace(
        ".", ","
    )
    return formatter


def test_single_star_format(mock_article_formatter):
    """Test format classique pour une étoile simple"""
    section = PhysicalCharacteristicsSection(mock_article_formatter)
    star = Star(
        sy_star_count=1,
        st_spectral_type="G2V",
        st_mass=ValueWithUncertainty(1.0),
        st_radius=ValueWithUncertainty(1.0),
    )

    content = section.generate(star)

    assert "Cette étoile est de type spectral G2V" in content
    assert "Sa masse est estimée à 1,0 fois celle du [[Soleil]]" in content
    assert "Les étoiles composant ce système sont" not in content


def test_binary_star_format(mock_article_formatter):
    """Test format liste pour un système binaire"""
    section = PhysicalCharacteristicsSection(mock_article_formatter)
    star = Star(
        st_name="Kepler-16",
        sy_star_count=2,
        st_spectral_type="K7V",
        st_mass=ValueWithUncertainty(0.69),
        st_radius=ValueWithUncertainty(0.649),
        st_spectral_type_2="M",
        st_mass_2=ValueWithUncertainty(0.203),
        st_radius_2=ValueWithUncertainty(0.226),
    )

    content = section.generate(star)

    assert "Les étoiles composant ce système sont :" in content
    assert "Kepler-16 A" in content
    assert "Kepler-16 B" in content
    assert "naine orange" in content  # K7V
    assert "naine rouge" in content  # M
    assert "0,69" in content
    assert "0,203" in content


def test_binary_without_component_b_data(mock_article_formatter):
    """Test système binaire sans données pour composante B"""
    section = PhysicalCharacteristicsSection(mock_article_formatter)
    star = Star(
        st_name="Test Star",
        sy_star_count=2,
        st_spectral_type="G4V",
        st_mass=ValueWithUncertainty(0.94),
        st_radius=ValueWithUncertainty(1.75),
    )

    content = section.generate(star)

    assert "Les étoiles composant ce système sont :" in content
    assert "Test Star A" in content
    assert "Test Star B" not in content  # Pas de données pour B


def test_star_type_classification(mock_article_formatter):
    """Test classification des types d'étoiles"""
    section = PhysicalCharacteristicsSection(mock_article_formatter)

    # Test naine jaune (G)
    assert "naine jaune" in section._get_star_type_description(Star(st_spectral_type="G2V"), "A")

    # Test naine orange (K)
    assert "naine orange" in section._get_star_type_description(Star(st_spectral_type="K5V"), "A")

    # Test naine rouge (M)
    assert "naine rouge" in section._get_star_type_description(Star(st_spectral_type="M3V"), "A")

    # Test étoile blanche (F)
    assert "étoile blanche" in section._get_star_type_description(Star(st_spectral_type="F5V"), "A")


def test_triple_star_system(mock_article_formatter):
    """Test système triple (affiche seulement A et B pour l'instant)"""
    section = PhysicalCharacteristicsSection(mock_article_formatter)
    star = Star(
        st_name="Alpha Centauri",
        sy_star_count=3,
        st_spectral_type="G2V",
        st_mass=ValueWithUncertainty(1.1),
        st_spectral_type_2="K1V",
        st_mass_2=ValueWithUncertainty(0.9),
    )

    content = section.generate(star)

    assert "Les étoiles composant ce système sont :" in content
    assert "Alpha Centauri A" in content
    assert "Alpha Centauri B" in content
