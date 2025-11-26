from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.physical_characteristics_section import (
    PhysicalCharacteristicsSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


@pytest.fixture
def mock_article_formatter():
    formatter = Mock()
    formatter.format_number_as_french_string.side_effect = lambda x, **kwargs: str(x).replace(
        ".", ","
    )
    return formatter


def test_mass_description_standard(mock_article_formatter):
    section = PhysicalCharacteristicsSection(mock_article_formatter)
    exoplanet = Exoplanet(pl_mass=ValueWithUncertainty(1.5), disc_method="Transit")

    desc = section._format_mass_description(exoplanet)
    assert "sa masse imposante de 1,5" in desc
    assert "masse minimale" not in desc


def test_mass_description_radial_velocity(mock_article_formatter):
    section = PhysicalCharacteristicsSection(mock_article_formatter)
    exoplanet = Exoplanet(pl_mass=ValueWithUncertainty(2.0), disc_method="Radial Velocity")

    desc = section._format_mass_description(exoplanet)
    assert "sa masse minimale imposante de 2,0" in desc


def test_generate_with_mass_distinction(mock_article_formatter):
    section = PhysicalCharacteristicsSection(mock_article_formatter)
    exoplanet = Exoplanet(pl_mass=ValueWithUncertainty(0.8), disc_method="Radial Velocity")

    content = section.generate(exoplanet)
    assert "masse minimale modérée de 0,8" in content
