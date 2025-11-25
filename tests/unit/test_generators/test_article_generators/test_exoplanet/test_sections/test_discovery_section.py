# tests/unit/test_generators/test_article_generators/test_exoplanet/test_sections/test_discovery_section.py

"""Tests unitaires pour DiscoverySection."""

import pytest

from src.generators.articles.exoplanet.sections import DiscoverySection
from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


@pytest.fixture
def article_formatter():
    return ArticleFormatter()


@pytest.fixture
def exoplanet_with_discovery():
    """Exoplanète avec informations de découverte."""

    class MethodEnum:
        def __init__(self, value):
            self.value = value
            self.name = value  # Mock name attribute if needed

    return Exoplanet(
        pl_name="Test Planet b",
        disc_year=1999,
        disc_method=MethodEnum("Transit"),
    )


class TestDiscoverySection:
    """Tests pour DiscoverySection."""

    def test_discovery_section_complete(self, article_formatter, exoplanet_with_discovery):
        """Test de la section découverte complète."""
        section = DiscoverySection(article_formatter)
        result = section.generate(exoplanet_with_discovery)

        assert result != ""
        assert "== Découverte ==" in result
        assert "1999" in result
        assert "transits" in result

    def test_discovery_section_empty(self, article_formatter):
        """Test avec une exoplanète sans année de découverte."""
        exoplanet = Exoplanet(pl_name="Test b")
        section = DiscoverySection(article_formatter)
        result = section.generate(exoplanet)

        assert result == ""

    def test_discovery_section_without_method(self, article_formatter):
        """Test avec seulement l'année de découverte."""
        exoplanet = Exoplanet(pl_name="Test b", disc_year=2020)
        section = DiscoverySection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "2020" in result
        assert "découverte" in result

    def test_discovery_section_method_translations(self, article_formatter):
        """Test des traductions de méthodes de découverte."""
        section = DiscoverySection(article_formatter)

        # Créer un objet simple avec un attribut value pour simuler un enum
        class MethodEnum:
            def __init__(self, value):
                self.value = value
                self.name = value

        methods_to_test = [
            (MethodEnum("Radial Velocity"), "vitesses radiales"),
            (MethodEnum("Imaging"), "imagerie directe"),
            (MethodEnum("Microlensing"), "microlentille"),
        ]

        for method, expected_text in methods_to_test:
            exoplanet = Exoplanet(
                pl_name="Test b",
                disc_year=2000,
                disc_method=method,
            )
            result = section.generate(exoplanet)
            assert expected_text in result
