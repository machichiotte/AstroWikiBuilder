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

    def test_discovery_section_with_telescope_and_instrument(self, article_formatter):
        """Test avec télescope et instrument."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            disc_year=2021,
            disc_telescope="Kepler",
            disc_instrument="Kepler Cam",
        )
        section = DiscoverySection(article_formatter)
        result = section.generate(exoplanet)

        assert "Kepler" in result
        assert "Kepler Cam" in result
        assert "télescope Kepler" in result
        assert "instrument Kepler Cam" in result

    def test_discovery_section_with_telescope_only(self, article_formatter):
        """Test avec télescope uniquement."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            disc_year=2021,
            disc_telescope="TESS",
        )
        section = DiscoverySection(article_formatter)
        result = section.generate(exoplanet)

        assert "TESS" in result
        assert "télescope TESS" in result
        assert "instrument" not in result

    def test_discovery_section_with_instrument_only(self, article_formatter):
        """Test avec instrument uniquement."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            disc_year=2021,
            disc_instrument="HARPS",
        )
        section = DiscoverySection(article_formatter)
        result = section.generate(exoplanet)

        assert "HARPS" in result
        assert "instrument HARPS" in result
        assert "télescope" not in result

    def test_discovery_section_with_pubdate(self, article_formatter):
        """Test avec date de publication."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            disc_year=2021,
            disc_pubdate="2021-05",
        )
        section = DiscoverySection(article_formatter)
        result = section.generate(exoplanet)

        assert "mai 2021" in result
        assert "annoncée en mai 2021" in result

    def test_discovery_section_with_invalid_pubdate(self, article_formatter):
        """Test avec date de publication invalide (format inattendu)."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            disc_year=2021,
            disc_pubdate="2021",  # Trop court pour extraire le mois
        )
        section = DiscoverySection(article_formatter)
        result = section.generate(exoplanet)

        assert "annoncée" not in result
