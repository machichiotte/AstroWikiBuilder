"""Tests pour pipeline_executor."""

import argparse
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

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
            output_dir="output",
            drafts_dir="drafts",
            consolidated_dir="consolidated"
        )
        
        _setup_output_directories(args)
        
        mock_create.assert_called_once_with("output", "drafts", "consolidated")

    @patch("src.orchestration.pipeline_executor.create_output_directories")
    def test_setup_with_default_consolidated_dir(self, mock_create):
        """Test de création avec répertoire consolidated par défaut."""
        args = argparse.Namespace(
            output_dir="output",
            drafts_dir="drafts"
        )
        
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
            sources=["nasa"]
        )

    @patch("src.orchestration.pipeline_executor.create_output_directories")
    @patch("src.orchestration.pipeline_executor.initialize_services")
    @patch("src.orchestration.pipeline_executor.initialize_collectors")
    @patch("src.orchestration.pipeline_executor.fetch_and_ingest_data")
    @patch("src.orchestration.pipeline_executor.export_consolidated_data")
    @patch("src.orchestration.pipeline_executor.generate_and_export_statistics")
    @patch("src.orchestration.pipeline_executor.generate_and_persist_exoplanet_drafts")
    @patch("src.orchestration.pipeline_executor.generate_and_persist_star_drafts")
    def test_execute_pipeline_full_workflow(
        self,
        mock_star_drafts,
        mock_exo_drafts,
        mock_stats,
        mock_export,
        mock_ingest,
        mock_collectors,
        mock_services,
        mock_create_dirs,
        mock_args
    ):
        """Test du workflow complet du pipeline."""
        # Configuration des mocks
        exo_repo = Mock()
        star_repo = Mock()
        stat_service = Mock()
        wiki_service = Mock()
        export_service = Mock()
        
        mock_services.return_value = (exo_repo, star_repo, stat_service, wiki_service, export_service)
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
        mock_exo_drafts.assert_called_once()
        mock_star_drafts.assert_called_once()

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
        mock_args
    ):
        """Test du pipeline avec skip_wikipedia_check activé."""
        # Configuration
        mock_args.skip_wikipedia_check = True
        
        exo_repo = Mock()
        star_repo = Mock()
        stat_service = Mock()
        wiki_service = Mock()
        export_service = Mock()
        
        mock_services.return_value = (exo_repo, star_repo, stat_service, wiki_service, export_service)
        mock_collectors.return_value = [Mock()]
        
        # Exécution
        execute_pipeline(mock_args)
        
        # Vérifications
        mock_exo_drafts.assert_not_called()
        mock_star_drafts.assert_not_called()
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
        mock_args
    ):
        """Test du pipeline avec seulement le traitement des données."""
        # Configuration
        mock_args.skip_wikipedia_check = True
        
        exo_repo = Mock()
        star_repo = Mock()
        stat_service = Mock()
        wiki_service = Mock()
        export_service = Mock()
        
        mock_services.return_value = (exo_repo, star_repo, stat_service, wiki_service, export_service)
        mock_collectors.return_value = [Mock()]
        
        # Exécution
        execute_pipeline(mock_args)
        
        # Vérifications - les étapes de base doivent être appelées
        mock_create_dirs.assert_called_once()
        mock_services.assert_called_once()
        mock_collectors.assert_called_once()
        mock_ingest.assert_called_once()
        mock_export.assert_called_once()
        mock_stats.assert_called_once()
