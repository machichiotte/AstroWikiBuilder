from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.observation_potential_section import (
    ObservationPotentialSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


class TestObservationPotentialSection:
    @pytest.fixture
    def mock_formatter(self):
        return Mock()

    @pytest.fixture
    def section(self, mock_formatter):
        return ObservationPotentialSection(mock_formatter)

    def test_generate_no_magnitude(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.st_apparent_magnitude = None
        assert section.generate(exoplanet) == ""

    def test_generate_high_magnitude(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.st_apparent_magnitude = 13.0
        assert section.generate(exoplanet) == ""

    def test_generate_invalid_magnitude(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.st_apparent_magnitude = "invalid"
        assert section.generate(exoplanet) == ""

    def test_generate_atmosphere_scenario(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.st_apparent_magnitude = 9.0
        exoplanet.disc_method = "Transit"
        exoplanet.pl_transit_depth = ValueWithUncertainty(value=1.0)

        content = section.generate(exoplanet)
        assert "cible de choix pour la [[spectroscopie de transmission]]" in content
        assert "9.0" in content

    def test_generate_bright_star_scenario(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.st_apparent_magnitude = 9.0
        exoplanet.disc_method = "Radial Velocity"  # Not transit

        content = section.generate(exoplanet)
        assert "cible brillante pour des observations photométriques" in content
        assert "9.0" in content

    def test_generate_medium_star_scenario(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.st_apparent_magnitude = 11.0

        content = section.generate(exoplanet)
        assert "accessible aux télescopes de taille moyenne" in content
        assert "11.0" in content

    def test_extract_apparent_magnitude_with_value_object(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")

        # Mocking an object with a .value attribute
        class MockQuantity:
            value = 10.5

        exoplanet.st_apparent_magnitude = MockQuantity()

        content = section.generate(exoplanet)
        assert "10.5" in content
