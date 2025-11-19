# tests/integration/test_full_pipeline.py
"""
Test d'intégration du pipeline complet.
"""

from unittest.mock import patch


class TestFullPipeline:
    """Tests du pipeline complet end-to-end."""

    @patch(
        "sys.argv",
        ["main.py", "--use-mock", "nasa_exoplanet_archive", "--skip-wikipedia-check"],
    )
    def test_pipeline_with_mock_data(self, tmp_path):
        """Test du pipeline complet avec données mockées."""
        from src.orchestration.cli_parser import parse_cli_arguments
        from src.orchestration.service_initializer import (
            initialize_services,
            initialize_collectors,
        )

        # Parse arguments
        args = parse_cli_arguments()
        assert args.use_mock == ["nasa_exoplanet_archive"]

        # Initialize services
        services = initialize_services()
        assert len(services) == 5  # 5 services returned

        # Initialize collectors
        collectors = initialize_collectors(args)
        assert "nasa_exoplanet_archive" in collectors

    def test_collector_to_generator_flow(self, sample_exoplanet):
        """Test du flux collector → processor → generator."""
        from src.services.repositories.exoplanet_repository import ExoplanetRepository
        from src.generators.articles.exoplanet.exoplanet_article_generator import (
            ExoplanetWikipediaArticleGenerator,
        )

        # Repository
        repo = ExoplanetRepository()
        repo.add_exoplanets_from_source([sample_exoplanet], "test")

        # Récupération
        exoplanets = repo.get_all_exoplanets()
        assert len(exoplanets) == 1

        # Génération d'article
        generator = ExoplanetWikipediaArticleGenerator()
        article = generator.compose_wikipedia_article_content(exoplanets[0])

        assert article is not None
        assert "HD 209458 b" in article

    def test_statistics_generation_flow(self, sample_exoplanet, sample_star):
        """Test du flux de génération de statistiques."""
        from src.services.processors.statistics_service import StatisticsService

        stat_service = StatisticsService()

        # Statistiques exoplanètes
        exo_stats = stat_service.generate_statistics_exoplanet([sample_exoplanet])
        assert exo_stats["total"] == 1

        # Statistiques étoiles
        star_stats = stat_service.generate_statistics_star([sample_star])
        assert star_stats["total_stars"] == 1
