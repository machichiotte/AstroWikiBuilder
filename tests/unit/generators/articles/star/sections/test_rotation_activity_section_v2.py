from unittest.mock import Mock

import pytest

from src.generators.articles.star.sections.rotation_activity_section import (
    RotationActivitySection,
)
from src.models.entities.star_entity import Star, ValueWithUncertainty


@pytest.fixture
def mock_article_formatter():
    formatter = Mock()
    formatter.format_number_as_french_string.side_effect = lambda x, **kwargs: str(x).replace(
        ".", ","
    )
    return formatter


def test_generate_with_log_rhk(mock_article_formatter):
    section = RotationActivitySection(mock_article_formatter)
    star = Star(st_log_rhk=ValueWithUncertainty(-4.95))

    result = section.generate(star)
    assert "indice d'activité chromosphérique (log R'HK) est de -4,95" in result


def test_generate_with_all_activity_props(mock_article_formatter):
    section = RotationActivitySection(mock_article_formatter)
    star = Star(st_rotation=ValueWithUncertainty(25.0), st_log_rhk=ValueWithUncertainty(-4.5))

    content = section.generate(star)
    assert "période de rotation d'environ 25,0 jours" in content
    assert "indice d'activité chromosphérique (log R'HK) est de -4,5" in content
