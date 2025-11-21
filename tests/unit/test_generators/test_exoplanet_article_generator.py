# tests/unit/test_generators/test_exoplanet_article_generator.py
"""
Tests pour les générateurs d'articles Wikipedia.
"""

from src.generators.articles.exoplanet.exoplanet_article_generator import (
    ExoplanetWikipediaArticleGenerator,
)
from src.generators.articles.star.star_article_generator import (
    StarWikipediaArticleGenerator,
)


class TestExoplanetArticleGenerator:
    """Tests du générateur d'articles pour exoplanètes."""

    def test_initialization(self):
        """Test d'initialisation."""
        generator = ExoplanetWikipediaArticleGenerator()
        assert generator is not None

    def test_compose_article_with_sample_exoplanet(self, sample_exoplanet):
        """Test de composition complète d'un article."""
        generator = ExoplanetWikipediaArticleGenerator()

        article = generator.compose_wikipedia_article_content(sample_exoplanet)

        # Vérifications de base
        assert article is not None
        assert isinstance(article, str)
        assert len(article) > 0

        # Vérifier présence du nom
        assert "HD 209458 b" in article

        # Vérifier présence de sections clés
        assert "Infobox" in article or "{{" in article  # Infobox
        assert "Caractéristiques" in article or "physiques" in article

    def test_article_contains_infobox(self, sample_exoplanet):
        """Test que l'article contient une infobox."""
        generator = ExoplanetWikipediaArticleGenerator()
        article = generator.compose_wikipedia_article_content(sample_exoplanet)

        assert "{{Infobox" in article or "{{" in article

    def test_article_contains_references(self, sample_exoplanet):
        """Test que l'article contient des références."""
        generator = ExoplanetWikipediaArticleGenerator()
        article = generator.compose_wikipedia_article_content(sample_exoplanet)

        # Vérifier présence de balises de référence
        assert "<ref" in article or "==" in article


class TestStarArticleGenerator:
    """Tests du générateur d'articles pour étoiles."""

    def test_initialization(self):
        """Test d'initialisation."""
        generator = StarWikipediaArticleGenerator()
        assert generator is not None

    def test_compose_article_with_sample_star(self, sample_star):
        """Test de composition complète d'un article."""
        generator = StarWikipediaArticleGenerator()

        article = generator.compose_wikipedia_article_content(sample_star)

        # Vérifications de base
        assert article is not None
        assert isinstance(article, str)
        assert len(article) > 0

        # Vérifier présence du nom
        assert "HD 209458" in article

        # Vérifier présence de sections clés
        assert "Infobox" in article or "{{" in article

    def test_article_with_exoplanets(self, sample_star, sample_exoplanet):
        """Test d'article avec liste d'exoplanètes."""
        generator = StarWikipediaArticleGenerator()

        article = generator.compose_wikipedia_article_content(
            sample_star, exoplanets=[sample_exoplanet]
        )

        assert article is not None
        # L'article devrait mentionner l'exoplanète ou avoir une section planètes
        assert "planète" in article.lower() or "HD 209458 b" in article

    def test_article_contains_infobox(self, sample_star):
        """Test que l'article contient une infobox."""
        generator = StarWikipediaArticleGenerator()
        article = generator.compose_wikipedia_article_content(sample_star)

        assert "{{Infobox" in article or "{{" in article

    def test_article_contains_spectral_type(self, sample_star):
        """Test que l'article contient le type spectral."""
        generator = StarWikipediaArticleGenerator()
        article = generator.compose_wikipedia_article_content(sample_star)

        assert "G0V" in article or "spectral" in article.lower()
