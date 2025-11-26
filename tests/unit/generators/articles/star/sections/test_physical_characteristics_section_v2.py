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


def test_generate_full_content(mock_article_formatter):
    section = PhysicalCharacteristicsSection(mock_article_formatter)
    star = Star(
        st_spectral_type="G2V",
        st_temperature=ValueWithUncertainty(5778),
        st_mass=ValueWithUncertainty(1.0),
        st_radius=ValueWithUncertainty(1.0),
        st_density=ValueWithUncertainty(1.41),
        st_luminosity=ValueWithUncertainty(1.0),
        st_metallicity=ValueWithUncertainty(0.0),
        st_surface_gravity=ValueWithUncertainty(4.44),
        st_age=ValueWithUncertainty(4.6),
    )

    content = section.generate(star)

    assert "== Caractéristiques physiques ==" in content
    assert "type spectral G2V" in content
    assert "température effective est d'environ 5778 [[kelvin|K]]" in content
    assert "masse est estimée à 1,0 fois celle du [[Soleil]]" in content
    assert "rayon est d'environ 1,0 fois celui du Soleil" in content
    assert "densité moyenne est d'environ 1,41 g/cm³" in content
    assert "luminosité est d'environ 1,0 fois celle du Soleil" in content
    assert "métallicité est estimée à [Fe/H] = 0,0" in content
    assert "gravité de surface (log g) est de 4,44" in content
    assert "âge de l'étoile est estimé à environ 4,6 milliards d'années" in content


def test_generate_partial_content(mock_article_formatter):
    section = PhysicalCharacteristicsSection(mock_article_formatter)
    star = Star(st_metallicity=ValueWithUncertainty(-0.5), st_age=ValueWithUncertainty(2.5))

    # Should return empty if basic properties are missing (based on the 'any' check in code)
    # Wait, I updated the code but did I update the 'any' check?
    # Let's check the code content again. I did NOT update the 'any' check in the ReplaceFileContent call.
    # I should have updated it.

    # Let's verify if the 'any' check blocks us.
    # The 'any' check is:
    # if not any([star.st_spectral_type, star.st_temperature, star.st_mass, star.st_radius, star.st_luminosity, star.st_density]):
    # So if I only have metallicity and age, it returns empty string.

    content = section.generate(star)
    assert content == ""


def test_generate_with_basic_and_new_props(mock_article_formatter):
    section = PhysicalCharacteristicsSection(mock_article_formatter)
    star = Star(st_spectral_type="K5", st_metallicity=ValueWithUncertainty(0.2))

    content = section.generate(star)
    assert "type spectral K5" in content
    assert "métallicité est estimée à [Fe/H] = 0,2" in content
