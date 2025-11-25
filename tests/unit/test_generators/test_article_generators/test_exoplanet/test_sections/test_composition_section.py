from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.composition_section import CompositionSection
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


class TestCompositionSection:
    @pytest.fixture
    def mock_formatter(self):
        formatter = Mock()
        formatter.format_uncertain_value_for_article.side_effect = lambda x: str(x.value)
        return formatter

    @pytest.fixture
    def section(self, mock_formatter):
        return CompositionSection(mock_formatter)

    def test_generate_no_density(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_density = None
        assert section.generate(exoplanet) == ""

    def test_generate_invalid_density(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_density = ValueWithUncertainty(value="invalid")
        assert section.generate(exoplanet) == ""

    def test_generate_telluric_high_density(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_density = ValueWithUncertainty(value=5.5)
        content = section.generate(exoplanet)
        assert "5.5" in content
        assert "composition probablement [[Planète tellurique|tellurique]]" in content

    def test_generate_telluric_medium_density(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_density = ValueWithUncertainty(value=4.0)
        content = section.generate(exoplanet)
        assert "4.0" in content
        assert "pourrait avoir une composition [[Planète tellurique|tellurique]]" in content

    def test_generate_mini_neptune(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_density = ValueWithUncertainty(value=2.5)
        content = section.generate(exoplanet)
        assert "2.5" in content
        assert "pourrait être une [[mini-Neptune]]" in content

    def test_generate_gas_giant(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_density = ValueWithUncertainty(value=1.5)
        content = section.generate(exoplanet)
        assert "1.5" in content
        assert "probablement une [[géante gazeuse]]" in content
