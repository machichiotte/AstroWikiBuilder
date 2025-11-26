from unittest.mock import Mock

import pytest

from src.generators.articles.star.sections.photometry_section import PhotometrySection
from src.models.entities.star_entity import Star, ValueWithUncertainty


@pytest.fixture
def mock_article_formatter():
    formatter = Mock()
    formatter.format_number_as_french_string.side_effect = lambda x, **kwargs: str(x).replace(
        ".", ","
    )
    return formatter


def test_collect_magnitudes_all_systems(mock_article_formatter):
    section = PhotometrySection(mock_article_formatter)
    star = Star(
        st_mag_v=ValueWithUncertainty(10.0),
        st_mag_j=ValueWithUncertainty(9.0),
        st_mag_w1=ValueWithUncertainty(8.5),
        st_mag_gaia=ValueWithUncertainty(9.8),
        st_mag_t=ValueWithUncertainty(9.9),
        st_mag_kep=ValueWithUncertainty(10.1),
    )

    magnitudes = section._collect_magnitudes(star)

    bands = [m["band"] for m in magnitudes]
    systems = [m["system"] for m in magnitudes]

    assert "V" in bands
    assert "J" in bands
    assert "W1" in bands
    assert "G" in bands
    assert "T" in bands
    assert "Kp" in bands

    assert "Johnson" in systems
    assert "2MASS" in systems
    assert "WISE" in systems
    assert "Gaia" in systems
    assert "TESS" in systems
    assert "Kepler" in systems


def test_generate_photometry_table(mock_article_formatter):
    section = PhotometrySection(mock_article_formatter)
    star = Star(st_mag_gaia=ValueWithUncertainty(12.34))

    content = section.generate(star)
    assert '{| class="wikitable"' in content
    assert "| G || 12,34 || Gaia" in content
