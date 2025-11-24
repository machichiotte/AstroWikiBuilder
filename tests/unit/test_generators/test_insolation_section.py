from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.insolation_section import InsolationSection
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


class TestInsolationSection:
    @pytest.fixture
    def mock_formatter(self):
        formatter = Mock()
        formatter.format_uncertain_value_for_article.side_effect = lambda x: str(x.value)
        return formatter

    @pytest.fixture
    def section(self, mock_formatter):
        return InsolationSection(mock_formatter)

    def test_generate_no_flux(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_insolation_flux = None
        assert section.generate(exoplanet) == ""

    def test_generate_invalid_flux(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_insolation_flux = ValueWithUncertainty(value="invalid")
        assert section.generate(exoplanet) == ""

    def test_generate_very_low_flux(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_insolation_flux = ValueWithUncertainty(value=0.05)
        content = section.generate(exoplanet)
        assert "0.05" in content
        assert "zone très froide et sombre" in content

    def test_generate_low_flux(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_insolation_flux = ValueWithUncertainty(value=0.2)
        content = section.generate(exoplanet)
        assert "0.2" in content
        assert "inférieur à celui de [[Mars (planète)|Mars]]" in content

    def test_generate_habitable_zone_outer(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_insolation_flux = ValueWithUncertainty(value=0.6)
        content = section.generate(exoplanet)
        assert "0.6" in content
        assert "limite externe de la [[zone habitable]]" in content

    def test_generate_earth_like_flux(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_insolation_flux = ValueWithUncertainty(value=1.0)
        content = section.generate(exoplanet)
        assert "1.0" in content
        assert "niveau d'insolation relativement comparable" in content

    def test_generate_habitable_zone_inner(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_insolation_flux = ValueWithUncertainty(value=1.5)
        content = section.generate(exoplanet)
        assert "1.5" in content
        assert "limite interne de la zone habitable" in content

    def test_generate_high_flux(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_insolation_flux = ValueWithUncertainty(value=3.0)
        content = section.generate(exoplanet)
        assert "3.0" in content
        assert "proximité importante avec son étoile hôte" in content

    def test_generate_very_high_flux(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_insolation_flux = ValueWithUncertainty(value=5.0)
        content = section.generate(exoplanet)
        assert "5.0" in content
        assert "supérieur à celui de [[Mercure (planète)|Mercure]]" in content
