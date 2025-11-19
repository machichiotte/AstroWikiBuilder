# tests/unit/test_generators/test_exoplanet_introduction_generator.py
"""
Tests unitaires pour ExoplanetIntroductionGenerator.
"""

import pytest
from src.generators.articles.exoplanet.parts.exoplanet_introduction_generator import (
    ExoplanetIntroductionGenerator,
)
from src.models.entities.exoplanet import Exoplanet, ValueWithUncertainty
from src.utils.astro.classification.exoplanet_comparison_utils import (
    ExoplanetComparisonUtils,
)
from src.utils.formatters.article_formatters import ArticleUtils


class TestExoplanetIntroductionGenerator:
    """Tests pour le générateur d'introduction d'exoplanètes."""

    @pytest.fixture
    def generator(self):
        """Fixture pour créer une instance du générateur."""
        comparison_utils = ExoplanetComparisonUtils()
        article_utils = ArticleUtils()
        return ExoplanetIntroductionGenerator(comparison_utils, article_utils)

    @pytest.fixture
    def sample_exoplanet_complete(self):
        """Fixture pour une exoplanète avec toutes les données."""
        return Exoplanet(
            pl_name="HD 209458 b",
            st_name="HD 209458",
            st_spectral_type="G0V",
            st_distance=ValueWithUncertainty(value=47.5),
            sy_constellation="Pégase",
            pl_mass=ValueWithUncertainty(value=0.69),
            pl_radius=ValueWithUncertainty(value=1.38),
        )

    @pytest.fixture
    def sample_exoplanet_minimal(self):
        """Fixture pour une exoplanète avec données minimales."""
        return Exoplanet(
            pl_name="Test Planet b",
            pl_mass=ValueWithUncertainty(value=1.0),
        )

    def test_compose_host_star_phrase_with_spectral_type(
        self, generator, sample_exoplanet_complete
    ):
        """Test de la génération de la phrase d'étoile hôte avec type spectral."""
        result = generator.compose_host_star_phrase(sample_exoplanet_complete)
        
        assert result is not None
        assert "HD 209458" in result
        assert "orbite autour" in result
        assert "[[" in result and "]]" in result

    def test_compose_host_star_phrase_without_star_name(self, generator):
        """Test avec une exoplanète sans nom d'étoile."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = generator.compose_host_star_phrase(exoplanet)
        
        assert result is None

    def test_compose_host_star_phrase_without_spectral_type(self, generator):
        """Test avec une étoile sans type spectral."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test Star",
        )
        result = generator.compose_host_star_phrase(exoplanet)
        
        assert result is not None
        assert "Test Star" in result
        assert "étoile hôte" in result

    def test_compose_distance_phrase_with_valid_distance(
        self, generator, sample_exoplanet_complete
    ):
        """Test de la génération de la phrase de distance avec distance valide."""
        result = generator.compose_distance_phrase(sample_exoplanet_complete)
        
        assert result is not None
        assert "située à environ" in result
        assert "année-lumière" in result
        assert "Terre" in result

    def test_compose_distance_phrase_without_distance(self, generator):
        """Test avec une exoplanète sans distance."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = generator.compose_distance_phrase(exoplanet)
        
        assert result is None

    def test_compose_distance_phrase_with_invalid_distance(self, generator):
        """Test avec une distance invalide."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_distance=ValueWithUncertainty(value=None),
        )
        result = generator.compose_distance_phrase(exoplanet)
        
        assert result is None

    def test_compose_constellation_phrase_with_constellation(
        self, generator, sample_exoplanet_complete
    ):
        """Test de la génération de la phrase de constellation."""
        result = generator.compose_constellation_phrase(sample_exoplanet_complete)
        
        assert result is not None
        assert "Pégase" in result

    def test_compose_constellation_phrase_without_constellation(self, generator):
        """Test avec une exoplanète sans constellation."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = generator.compose_constellation_phrase(exoplanet)
        
        assert result is None

    def test_compose_exoplanet_introduction_complete(
        self, generator, sample_exoplanet_complete
    ):
        """Test de la génération complète de l'introduction."""
        result = generator.compose_exoplanet_introduction(sample_exoplanet_complete)
        
        assert result is not None
        assert "HD 209458 b" in result
        assert "exoplanète" in result
        assert "HD 209458" in result
        assert "Pégase" in result
        assert result.endswith(".")

    def test_compose_exoplanet_introduction_minimal(
        self, generator, sample_exoplanet_minimal
    ):
        """Test de la génération de l'introduction avec données minimales."""
        result = generator.compose_exoplanet_introduction(sample_exoplanet_minimal)
        
        assert result is not None
        assert "Test Planet b" in result
        assert "exoplanète" in result
        assert result.endswith(".")

    def test_compose_exoplanet_introduction_without_name(self, generator):
        """Test avec une exoplanète sans nom."""
        exoplanet = Exoplanet(pl_mass=ValueWithUncertainty(value=1.0))
        result = generator.compose_exoplanet_introduction(exoplanet)
        
        assert result is not None
        assert "Nom inconnu" in result

    def test_introduction_format_consistency(self, generator, sample_exoplanet_complete):
        """Test de la cohérence du format de l'introduction."""
        result = generator.compose_exoplanet_introduction(sample_exoplanet_complete)
        
        # Vérifier le format Wikipedia
        assert result.startswith("'''")
        assert "'''" in result[3:]  # Deuxième occurrence pour fermer le gras
        assert "[[" in result  # Au moins un lien wiki
        assert "]]" in result
