import argparse
from unittest.mock import Mock, patch

from src.orchestration.pipeline_executor import (
    _initialize_data_processor,
    _setup_output_directories,
)


class TestPipelineExecutorHelpers:
    def test_setup_output_directories(self):
        args = argparse.Namespace(
            output_dir="output", drafts_dir="drafts", consolidated_dir="consolidated"
        )

        with patch("src.orchestration.pipeline_executor.create_output_directories") as mock_create:
            _setup_output_directories(args)
            mock_create.assert_called_once_with("output", "drafts", "consolidated")

    def test_setup_output_directories_default_consolidated(self):
        args = argparse.Namespace(output_dir="output", drafts_dir="drafts")

        with patch("src.orchestration.pipeline_executor.create_output_directories") as mock_create:
            with patch(
                "src.orchestration.pipeline_executor.DEFAULT_CONSOLIDATED_DIR",
                "default_consolidated",
            ):
                _setup_output_directories(args)
                mock_create.assert_called_once_with("output", "drafts", "default_consolidated")

    def test_initialize_data_processor(self):
        exo_repo = Mock()
        star_repo = Mock()
        stat_service = Mock()
        wiki_service = Mock()
        export_service = Mock()

        services = (exo_repo, star_repo, stat_service, wiki_service, export_service)

        with patch("src.orchestration.pipeline_executor.DataProcessor") as mock_processor:
            mock_instance = Mock()
            mock_processor.return_value = mock_instance

            result = _initialize_data_processor(services)

            mock_processor.assert_called_once_with(
                exoplanet_repository=exo_repo,
                star_repository=star_repo,
                stat_service=stat_service,
                wiki_service=wiki_service,
                export_service=export_service,
            )
            assert result == mock_instance
