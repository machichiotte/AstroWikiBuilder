from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.tidal_locking_section import TidalLockingSection
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


class TestTidalLockingSection:
    @pytest.fixture
    def mock_formatter(self):
        return Mock()

    @pytest.fixture
    def section(self, mock_formatter):
        return TidalLockingSection(mock_formatter)

    def test_generate_no_period(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_orbital_period = None
        assert section.generate(exoplanet) == ""

    def test_generate_invalid_period(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_orbital_period = ValueWithUncertainty(value="invalid")
        assert section.generate(exoplanet) == ""

    def test_generate_long_period_not_locked(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_orbital_period = ValueWithUncertainty(value=20.0)
        exoplanet.pl_eccentricity = ValueWithUncertainty(value=0.05)
        assert section.generate(exoplanet) == ""

    def test_generate_high_eccentricity_not_locked(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_orbital_period = ValueWithUncertainty(value=10.0)
        exoplanet.pl_eccentricity = ValueWithUncertainty(value=0.2)
        assert section.generate(exoplanet) == ""

    def test_generate_likely_locked(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_orbital_period = ValueWithUncertainty(value=10.0)
        exoplanet.pl_eccentricity = ValueWithUncertainty(value=0.05)
        content = section.generate(exoplanet)
        assert "Rotation et verrouillage gravitationnel" in content
        assert "verrouillage par effet de marée" in content

    def test_generate_likely_locked_no_eccentricity(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_orbital_period = ValueWithUncertainty(value=10.0)
        # No eccentricity data -> defaults to 0.0
        content = section.generate(exoplanet)
        assert "Rotation et verrouillage gravitationnel" in content

    def test_generate_invalid_eccentricity_defaults_to_zero(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_orbital_period = ValueWithUncertainty(value=10.0)
        exoplanet.pl_eccentricity = ValueWithUncertainty(value="invalid")
        content = section.generate(exoplanet)
        # Invalid eccentricity -> defaults to 0.0 -> likely locked
        assert "Rotation et verrouillage gravitationnel" in content
