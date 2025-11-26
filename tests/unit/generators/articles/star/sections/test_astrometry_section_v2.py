from unittest.mock import Mock

import pytest

from src.generators.articles.star.sections.astrometry_section import AstrometrySection
from src.models.entities.star_entity import Star, ValueWithUncertainty


@pytest.fixture
def mock_article_formatter():
    formatter = Mock()
    formatter.format_number_as_french_string.side_effect = lambda x, **kwargs: str(x).replace(
        ".", ","
    )
    return formatter


def test_total_proper_motion(mock_article_formatter):
    section = AstrometrySection(mock_article_formatter)
    star = Star(sy_pm=ValueWithUncertainty(25.5))

    content = section.generate(star)
    assert "mouvement propre total est de 25,5 mas/an" in content


def test_ecliptic_coordinates(mock_article_formatter):
    section = AstrometrySection(mock_article_formatter)
    star = Star(elon=ValueWithUncertainty(120.5), elat=ValueWithUncertainty(45.2))

    content = section.generate(star)
    assert "longitude écliptique est de 120,5°" in content
    assert "latitude écliptique est de 45,2°" in content


def test_complete_astrometry(mock_article_formatter):
    section = AstrometrySection(mock_article_formatter)
    star = Star(
        st_proper_motion_ra=ValueWithUncertainty(10.5),
        st_proper_motion_dec=ValueWithUncertainty(-5.2),
        sy_pm=ValueWithUncertainty(11.7),
        st_parallax=ValueWithUncertainty(25.0),
        glon=ValueWithUncertainty(180.0),
        glat=ValueWithUncertainty(-30.0),
        elon=ValueWithUncertainty(90.0),
        elat=ValueWithUncertainty(15.0),
    )

    content = section.generate(star)
    assert "mouvement propre en ascension droite" in content
    assert "mouvement propre total" in content
    assert "parallaxe" in content
    assert "longitude galactique" in content
    assert "longitude écliptique" in content
