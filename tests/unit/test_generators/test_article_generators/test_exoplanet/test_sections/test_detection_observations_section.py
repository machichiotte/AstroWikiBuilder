# tests/unit/test_generators/test_article_generators/test_exoplanet/test_sections/test_detection_observations_section.py

"""Tests unitaires pour DetectionObservationsSection."""

import pytest

from src.generators.articles.exoplanet.sections import DetectionObservationsSection
from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


@pytest.fixture
def article_formatter():
    return ArticleFormatter()


class TestDetectionObservationsSection:
    """Tests pour DetectionObservationsSection."""

    def test_detection_with_multiple_methods(self, article_formatter):
        """Test avec plusieurs méthodes de détection."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            tran_flag=1,
            rv_flag=1,
        )
        section = DetectionObservationsSection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "== Détection et observations ==" in result
        assert "transits" in result
        assert "vitesses radiales" in result

    def test_detection_with_all_methods(self, article_formatter):
        """Test avec toutes les méthodes de détection."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            tran_flag=1,
            rv_flag=1,
            ttv_flag=1,
            ast_flag=1,
        )
        section = DetectionObservationsSection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "transits" in result
        assert "vitesses radiales" in result
        assert "TTV" in result
        assert "astrométrie" in result

    def test_detection_with_facility(self, article_formatter):
        """Test avec facilité d'observation."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            tran_flag=1,
            rv_flag=1,
            disc_facility="Kepler",
        )
        section = DetectionObservationsSection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "Kepler" in result

    def test_detection_with_single_method(self, article_formatter):
        """Test avec une seule méthode (ne devrait pas générer de section)."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            tran_flag=1,
        )
        section = DetectionObservationsSection(article_formatter)
        result = section.generate(exoplanet)

        assert result == ""

    def test_detection_empty(self, article_formatter):
        """Test sans données de détection."""
        exoplanet = Exoplanet(pl_name="Test b")
        section = DetectionObservationsSection(article_formatter)
        result = section.generate(exoplanet)

        assert result == ""

    def test_detection_with_microlensing_and_pulsar(self, article_formatter):
        """Test avec microlentille et pulsar."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            micro_flag=1,
            pul_flag=1,
        )
        section = DetectionObservationsSection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "microlentille" in result
        assert "pulsar" in result
