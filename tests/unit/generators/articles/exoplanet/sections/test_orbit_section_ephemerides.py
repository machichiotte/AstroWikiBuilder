from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.orbit_section import OrbitSection
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


@pytest.fixture
def mock_article_formatter():
    formatter = Mock()
    formatter.format_number_as_french_string.side_effect = lambda x, **kwargs: str(x).replace(
        ".", ","
    )
    formatter.format_uncertain_value_for_article.side_effect = (
        lambda x: str(x.value).replace(".", ",") if x and x.value else None
    )
    return formatter


def test_add_periastron_time(mock_article_formatter):
    section = OrbitSection(mock_article_formatter)
    exoplanet = Exoplanet(pl_periastron_time=ValueWithUncertainty(2459000.5))

    content = section.generate(exoplanet)
    assert "passage au périastre a lieu à JD 2459000,5" in content


def test_add_argument_of_periastron(mock_article_formatter):
    section = OrbitSection(mock_article_formatter)
    exoplanet = Exoplanet(pl_argument_of_periastron=ValueWithUncertainty(90.5))

    content = section.generate(exoplanet)
    assert "argument du périastre (ω) est de 90,5 degrés" in content


def test_ephemerides_combined(mock_article_formatter):
    section = OrbitSection(mock_article_formatter)
    exoplanet = Exoplanet(
        pl_periastron_time=ValueWithUncertainty(2459000.5),
        pl_argument_of_periastron=ValueWithUncertainty(90.5),
        pl_eccentricity=ValueWithUncertainty(0.05),
    )

    content = section.generate(exoplanet)
    assert "passage au périastre" in content
    assert "argument du périastre" in content
    assert "excentricité" in content
