import pytest

from src.generators.articles.exoplanet.sections.system_architecture_section import (
    SystemArchitectureSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.utils.formatters.article_formatter import ArticleFormatter


class TestSystemArchitectureSection:
    @pytest.fixture
    def article_formatter(self):
        return ArticleFormatter()

    @pytest.fixture
    def section(self, article_formatter):
        return SystemArchitectureSection(article_formatter)

    def test_generate_single_planet_no_siblings(self, section):
        """Test avec une seule planète et pas de liste de siblings."""
        exoplanet = Exoplanet(pl_name="Test b", sy_planet_count=1)
        result = section.generate(exoplanet)
        assert result == ""

    def test_generate_multi_planet_no_siblings_fallback(self, section):
        """Test avec plusieurs planètes mais sans la liste détaillée (fallback)."""
        exoplanet = Exoplanet(pl_name="Test b", st_name="Star", sy_planet_count=3)
        result = section.generate(exoplanet)
        assert "== Architecture du système ==" in result
        assert "système de 3 planètes connues" in result

    def test_generate_with_siblings_sorted(self, section):
        """Test avec la liste des planètes du système, vérification du tri et de la position."""
        planet_b = Exoplanet(
            pl_name="Star b",
            st_name="Star",
            pl_semi_major_axis=ValueWithUncertainty(value=0.1),
        )
        planet_c = Exoplanet(
            pl_name="Star c",
            st_name="Star",
            pl_semi_major_axis=ValueWithUncertainty(value=0.2),
        )
        planet_d = Exoplanet(
            pl_name="Star d",
            st_name="Star",
            pl_semi_major_axis=ValueWithUncertainty(value=0.3),
        )

        system = [planet_c, planet_b, planet_d]  # Désordre

        # Test pour la planète du milieu (c)
        result_c = section.generate(planet_c, system_planets=system)

        assert "== Architecture du système ==" in result_c
        assert "compte au moins 3 planètes confirmées" in result_c
        assert "[[Star c]] est la 2e planète en partant de l'étoile" in result_c
        assert "Les autres planètes du système sont [[Star b]] et [[Star d]]" in result_c

    def test_generate_with_siblings_position_first(self, section):
        """Test position 'plus interne'."""
        planet_b = Exoplanet(
            pl_name="Star b",
            st_name="Star",
            pl_semi_major_axis=ValueWithUncertainty(value=0.1),
        )
        planet_c = Exoplanet(
            pl_name="Star c",
            st_name="Star",
            pl_semi_major_axis=ValueWithUncertainty(value=0.2),
        )
        system = [planet_b, planet_c]

        result = section.generate(planet_b, system_planets=system)
        assert "la plus interne" in result
        assert "L'autre planète connue du système est [[Star c]]" in result

    def test_generate_with_siblings_position_last(self, section):
        """Test position 'plus externe'."""
        planet_b = Exoplanet(
            pl_name="Star b",
            st_name="Star",
            pl_semi_major_axis=ValueWithUncertainty(value=0.1),
        )
        planet_c = Exoplanet(
            pl_name="Star c",
            st_name="Star",
            pl_semi_major_axis=ValueWithUncertainty(value=0.2),
        )
        system = [planet_b, planet_c]

        result = section.generate(planet_c, system_planets=system)
        assert "la plus externe" in result
