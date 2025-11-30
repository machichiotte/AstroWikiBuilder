"""Tests pour pipeline_executor."""

import argparse
from unittest.mock import Mock, patch

import pytest

from src.orchestration.pipeline_executor import (
    _initialize_data_processor,
    _setup_output_directories,
    execute_pipeline,
)


class TestSetupOutputDirectories:
    """Tests pour _setup_output_directories."""

    @patch("src.orchestration.pipeline_executor.create_output_directories")
    def test_setup_with_all_directories(self, mock_create):
        """Test de création avec tous les répertoires."""
        args = argparse.Namespace(
            output_dir="output", drafts_dir="drafts", consolidated_dir="consolidated"
        )

        _setup_output_directories(args)

        mock_create.assert_called_once_with("output", "drafts", "consolidated")

    @patch("src.orchestration.pipeline_executor.create_output_directories")
    def test_setup_with_default_consolidated_dir(self, mock_create):
        """Test de création avec répertoire consolidated par défaut."""
        args = argparse.Namespace(output_dir="output", drafts_dir="drafts")

        _setup_output_directories(args)

        # Vérifie que create_output_directories est appelé avec le répertoire par défaut
        assert mock_create.called


class TestInitializeDataProcessor:
    """Tests pour _initialize_data_processor."""

    def test_initialize_with_all_services(self):
        """Test d'initialisation avec tous les services."""
        exo_repo = Mock()
        star_repo = Mock()
        stat_service = Mock()
        wiki_service = Mock()
        export_service = Mock()

        services = (exo_repo, star_repo, stat_service, wiki_service, export_service)

        processor = _initialize_data_processor(services)

        assert processor.exoplanet_repository == exo_repo
        assert processor.star_repository == star_repo
        assert processor.stat_service == stat_service
        assert processor.wiki_service == wiki_service
        assert processor.export_service == export_service


class TestExecutePipeline:
    """Tests pour execute_pipeline."""

    @pytest.fixture
    def mock_args(self):
        """Fixture pour créer des arguments mock."""
        return argparse.Namespace(
            output_dir="output",
            drafts_dir="drafts",
            consolidated_dir="consolidated",
            skip_wikipedia_check=False,
            sources=["nasa"],
            generate_exoplanets=True,
            generate_stars=True,
        )

    @patch("src.orchestration.pipeline_executor.create_output_directories")
    @patch("src.orchestration.pipeline_executor.initialize_services")
    @patch("src.orchestration.pipeline_executor.initialize_collectors")
    @patch("src.orchestration.pipeline_executor.fetch_and_ingest_data")
    @patch("src.orchestration.pipeline_executor.export_consolidated_data")
    @patch("src.orchestration.pipeline_executor.generate_and_export_statistics")
    @patch("src.utils.wikipedia.draft_util.build_exoplanet_article_draft")
    @patch("src.utils.wikipedia.draft_util.persist_drafts_by_entity_type")
    @patch("src.orchestration.draft_pipeline.generate_and_persist_star_drafts_separated")
    def test_execute_pipeline_full_workflow(
        self,
        mock_star_drafts_separated,
        mock_persist_drafts,
        mock_build_draft,
        mock_stats,
        mock_export,
        mock_ingest,
        mock_collectors,
        mock_services,
        mock_create_dirs,
        mock_args,
    ):
        """Test du workflow complet du pipeline."""
        # Configuration des mocks
        exo_repo = Mock()
        star_repo = Mock()
        stat_service = Mock()
        wiki_service = Mock()
        export_service = Mock()

        # Create a mock processor
        mock_processor = Mock()
        # Configure resolve_wikipedia_status_for_exoplanets to return some articles
        mock_processor.resolve_wikipedia_status_for_exoplanets.return_value = (
            ["Existing Planet"],  # existing
            ["Missing Planet"],  # missing
        )
        # Configure resolve_wikipedia_status_for_stars
        mock_processor.resolve_wikipedia_status_for_stars.return_value = (
            ["Existing Star"],
            ["Missing Star"],
        )

        # Mock collect_all_exoplanets
        mock_planet1 = Mock()
        mock_planet1.pl_name = "Existing Planet"
        mock_planet1.st_name = "Existing Star"
        mock_planet2 = Mock()
        mock_planet2.pl_name = "Missing Planet"
        mock_planet2.st_name = "Missing Star"

        mock_processor.collect_all_exoplanets.return_value = [mock_planet1, mock_planet2]

        # We need to patch _initialize_data_processor to return our mock_processor
        with patch(
            "src.orchestration.pipeline_executor._initialize_data_processor",
            return_value=mock_processor,
        ):
            mock_services.return_value = (
                exo_repo,
                star_repo,
                stat_service,
                wiki_service,
                export_service,
            )
            mock_collectors.return_value = [Mock()]

            # Exécution
            execute_pipeline(mock_args)

            # Vérifications
            mock_create_dirs.assert_called_once()
            mock_services.assert_called_once()
            mock_collectors.assert_called_once_with(mock_args)
            mock_ingest.assert_called_once()
            mock_export.assert_called_once()
            mock_stats.assert_called_once()

            # Vérifier que build_exoplanet_article_draft est appelé pour les deux planètes
            assert mock_build_draft.call_count == 2

            # Vérifier que persist_drafts_by_entity_type est appelé
            mock_persist_drafts.assert_called_once()

            # Vérifier que generate_and_persist_star_drafts_separated est appelé
            mock_star_drafts_separated.assert_called_once()

    @patch("src.orchestration.pipeline_executor.create_output_directories")
    @patch("src.orchestration.pipeline_executor.initialize_services")
    @patch("src.orchestration.pipeline_executor.initialize_collectors")
    @patch("src.orchestration.pipeline_executor.fetch_and_ingest_data")
    @patch("src.orchestration.pipeline_executor.export_consolidated_data")
    @patch("src.orchestration.pipeline_executor.generate_and_export_statistics")
    @patch("src.orchestration.pipeline_executor.generate_and_persist_exoplanet_drafts")
    @patch("src.orchestration.pipeline_executor.generate_and_persist_star_drafts")
    def test_execute_pipeline_skip_wikipedia_check(
        self,
        mock_star_drafts,
        mock_exo_drafts,
        mock_stats,
        mock_export,
        mock_ingest,
        mock_collectors,
        mock_services,
        mock_create_dirs,
        mock_args,
    ):
        """Test du pipeline avec skip_wikipedia_check activé."""
        # Configuration
        mock_args.skip_wikipedia_check = True

        exo_repo = Mock()
        star_repo = Mock()
        stat_service = Mock()
        wiki_service = Mock()
        export_service = Mock()

        mock_services.return_value = (
            exo_repo,
            star_repo,
            stat_service,
            wiki_service,
            export_service,
        )
        mock_collectors.return_value = [Mock()]

        # Mock processor
        mock_processor = Mock()
        # Mock collect_all_exoplanets to return a list (needed for star drafts generation)
        mock_processor.collect_all_exoplanets.return_value = []

        with patch(
            "src.orchestration.pipeline_executor._initialize_data_processor",
            return_value=mock_processor,
        ):
            # Exécution
            execute_pipeline(mock_args)

        # Vérifications
        # With skip_wikipedia_check=True, we DO generate drafts now
        mock_exo_drafts.assert_called_once()
        mock_star_drafts.assert_called_once()
        mock_ingest.assert_called_once()
        mock_export.assert_called_once()

    @patch("src.orchestration.pipeline_executor.create_output_directories")
    @patch("src.orchestration.pipeline_executor.initialize_services")
    @patch("src.orchestration.pipeline_executor.initialize_collectors")
    @patch("src.orchestration.pipeline_executor.fetch_and_ingest_data")
    @patch("src.orchestration.pipeline_executor.export_consolidated_data")
    @patch("src.orchestration.pipeline_executor.generate_and_export_statistics")
    def test_execute_pipeline_data_processing_only(
        self,
        mock_stats,
        mock_export,
        mock_ingest,
        mock_collectors,
        mock_services,
        mock_create_dirs,
        mock_args,
    ):
        """Test du pipeline avec seulement le traitement des données."""
        # Configuration
        mock_args.skip_wikipedia_check = True
        mock_args.generate_exoplanets = False
        mock_args.generate_stars = False

        exo_repo = Mock()
        star_repo = Mock()
        stat_service = Mock()
        wiki_service = Mock()
        export_service = Mock()

        mock_services.return_value = (
            exo_repo,
            star_repo,
            stat_service,
            wiki_service,
            export_service,
        )
        mock_collectors.return_value = [Mock()]

        # Mock processor
        mock_processor = Mock()
        # Mock collect_all_exoplanets to return a list (needed for star drafts generation)
        mock_processor.collect_all_exoplanets.return_value = []
        # Mock collect_all_stars to return a list (needed for star drafts generation)
        mock_processor.collect_all_stars.return_value = []

        with patch(
            "src.orchestration.pipeline_executor._initialize_data_processor",
            return_value=mock_processor,
        ):
            # Exécution
            execute_pipeline(mock_args)

        # Vérifications - les étapes de base doivent être appelées
        mock_create_dirs.assert_called_once()
        mock_services.assert_called_once()
        mock_collectors.assert_called_once()
        mock_ingest.assert_called_once()
        mock_export.assert_called_once()
        mock_stats.assert_called_once()

    @patch("src.orchestration.pipeline_executor.create_output_directories")
    @patch("src.orchestration.pipeline_executor.initialize_services")
    @patch("src.orchestration.pipeline_executor.initialize_collectors")
    @patch("src.orchestration.pipeline_executor.fetch_and_ingest_data")
    @patch("src.orchestration.pipeline_executor.export_consolidated_data")
    @patch("src.orchestration.pipeline_executor.generate_and_export_statistics")
    @patch("src.utils.wikipedia.draft_util.build_exoplanet_article_draft")
    @patch("src.utils.wikipedia.draft_util.persist_drafts_by_entity_type")
    @patch("src.orchestration.draft_pipeline.generate_and_persist_star_drafts_separated")
    def test_execute_pipeline_with_missing_articles(
        self,
        mock_star_drafts_separated,
        mock_persist,
        mock_build_draft,
        mock_stats,
        mock_export,
        mock_ingest,
        mock_collectors,
        mock_services,
        mock_create_dirs,
        mock_args,
    ):
        """Test du pipeline avec des articles manquants sur Wikipedia."""
        # Configuration
        mock_args.skip_wikipedia_check = False

        exo_repo = Mock()
        star_repo = Mock()
        stat_service = Mock()
        wiki_service = Mock()
        export_service = Mock()

        mock_services.return_value = (
            exo_repo,
            star_repo,
            stat_service,
            wiki_service,
            export_service,
        )
        mock_collectors.return_value = [Mock()]

        # Mock processor
        mock_processor = Mock()

        # Mock exoplanets
        mock_planet1 = Mock()
        mock_planet1.pl_name = "Planet A"
        mock_planet2 = Mock()
        mock_planet2.pl_name = "Planet B"
        mock_planet3 = Mock()
        mock_planet3.pl_name = "Planet C"

        # Configure resolve_wikipedia_status_for_exoplanets to return some missing articles
        mock_processor.resolve_wikipedia_status_for_exoplanets.return_value = (
            ["Planet A"],  # existing articles
            ["Planet B", "Planet C"],  # missing articles
        )

        # Configure resolve_wikipedia_status_for_stars
        mock_processor.resolve_wikipedia_status_for_stars.return_value = (
            [],
            [],
        )

        # Mock collect_all_exoplanets to return all planets
        mock_processor.collect_all_exoplanets.return_value = [
            mock_planet1,
            mock_planet2,
            mock_planet3,
        ]

        # Mock draft generation
        mock_build_draft.side_effect = lambda exo, system_planets=None: f"Draft for {exo.pl_name}"

        with patch(
            "src.orchestration.pipeline_executor._initialize_data_processor",
            return_value=mock_processor,
        ):
            # Exécution
            execute_pipeline(mock_args)

        # Vérifications
        mock_create_dirs.assert_called_once()
        mock_services.assert_called_once()
        mock_collectors.assert_called_once()
        mock_ingest.assert_called_once()
        mock_export.assert_called_once()
        mock_stats.assert_called_once()

        # Vérifier que resolve_wikipedia_status_for_exoplanets a été appelé
        mock_processor.resolve_wikipedia_status_for_exoplanets.assert_called_once()

        # Vérifier que collect_all_exoplanets a été appelé
        mock_processor.collect_all_exoplanets.assert_called_once()

        # Vérifier que build_exoplanet_article_draft a été appelé 3 fois (pour Planet A, B et C)
        # Car on génère maintenant aussi les drafts pour les articles existants
        assert mock_build_draft.call_count == 3

        # Vérifier que persist_drafts_by_entity_type a été appelé
        mock_persist.assert_called_once()

        # Vérifier que generate_and_persist_star_drafts_separated a été appelé
        mock_star_drafts_separated.assert_called_once()

    @patch("src.orchestration.pipeline_executor.create_output_directories")
    @patch("src.orchestration.pipeline_executor.initialize_services")
    @patch("src.orchestration.pipeline_executor.initialize_collectors")
    @patch("src.orchestration.pipeline_executor.fetch_and_ingest_data")
    @patch("src.orchestration.pipeline_executor.export_consolidated_data")
    @patch("src.orchestration.pipeline_executor.generate_and_export_statistics")
    @patch("src.utils.wikipedia.draft_util.build_exoplanet_article_draft")
    @patch("src.utils.wikipedia.draft_util.persist_drafts_by_entity_type")
    @patch("src.orchestration.draft_pipeline.generate_and_persist_star_drafts_separated")
    def test_execute_pipeline_no_missing_articles(
        self,
        mock_star_drafts_separated,
        mock_persist_drafts,
        mock_build_draft,
        mock_stats,
        mock_export,
        mock_ingest,
        mock_collectors,
        mock_services,
        mock_create_dirs,
        mock_args,
    ):
        """Test du pipeline sans articles manquants sur Wikipedia."""
        # Configuration
        mock_args.skip_wikipedia_check = False

        exo_repo = Mock()
        star_repo = Mock()
        stat_service = Mock()
        wiki_service = Mock()
        export_service = Mock()

        mock_services.return_value = (
            exo_repo,
            star_repo,
            stat_service,
            wiki_service,
            export_service,
        )
        mock_collectors.return_value = [Mock()]

        # Mock processor
        mock_processor = Mock()

        # Mock exoplanets
        mock_planet1 = Mock()
        mock_planet1.pl_name = "Planet A"
        mock_planet1.st_name = "Star A"
        mock_planet2 = Mock()
        mock_planet2.pl_name = "Planet B"
        mock_planet2.st_name = "Star B"

        # Configure resolve_wikipedia_status_for_exoplanets to return no missing articles
        mock_processor.resolve_wikipedia_status_for_exoplanets.return_value = (
            ["Planet A", "Planet B"],  # all existing
            [],  # no missing articles
        )

        # Configure resolve_wikipedia_status_for_stars
        mock_processor.resolve_wikipedia_status_for_stars.return_value = (
            ["Star A", "Star B"],
            [],
        )

        # Mock collect_all_exoplanets to return all planets
        mock_processor.collect_all_exoplanets.return_value = [
            mock_planet1,
            mock_planet2,
        ]

        with patch(
            "src.orchestration.pipeline_executor._initialize_data_processor",
            return_value=mock_processor,
        ):
            # Exécution
            execute_pipeline(mock_args)

        # Vérifications
        mock_create_dirs.assert_called_once()
        mock_services.assert_called_once()
        mock_collectors.assert_called_once()
        mock_ingest.assert_called_once()
        mock_export.assert_called_once()
        mock_stats.assert_called_once()

        # Vérifier que resolve_wikipedia_status_for_exoplanets a été appelé
        mock_processor.resolve_wikipedia_status_for_exoplanets.assert_called_once()

        # Vérifier que build_exoplanet_article_draft a été appelé pour les articles existants
        assert mock_build_draft.call_count == 2

        # Vérifier que persist_drafts_by_entity_type a été appelé
        mock_persist_drafts.assert_called_once()

        # Vérifier que generate_and_persist_star_drafts_separated a été appelé
        mock_star_drafts_separated.assert_called_once()
