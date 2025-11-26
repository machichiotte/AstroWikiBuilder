from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.detection_observations_section import (
    DetectionObservationsSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


@pytest.fixture
def mock_article_formatter():
    formatter = Mock()
    formatter.format_uncertain_value_for_article.side_effect = (
        lambda x: str(x.value).replace(".", ",") if x and x.value else None
    )
    return formatter


def test_add_occultation_depth(mock_article_formatter):
    section = DetectionObservationsSection(mock_article_formatter)
    exoplanet = Exoplanet(
        pl_occultation_depth=ValueWithUncertainty(0.002), disc_facility="Hubble Space Telescope"
    )

    content = section.generate(exoplanet)
    assert "profondeur d'occultation mesurée est de 0,002" in content


def test_no_occultation_depth(mock_article_formatter):
    section = DetectionObservationsSection(mock_article_formatter)
    exoplanet = Exoplanet(disc_facility="Hubble Space Telescope")

    content = section.generate(exoplanet)
    assert "profondeur d'occultation" not in content
