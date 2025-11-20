# tests/unit/test_orchestration/test_cli_parser.py
"""
Tests pour le module cli_parser.py
"""

from unittest.mock import patch

from src.core.config import DEFAULT_DRAFTS_DIR, DEFAULT_OUTPUT_DIR
from src.orchestration.cli_parser import parse_cli_arguments


class TestCLIParser:
    """Tests du parseur de ligne de commande."""

    @patch("sys.argv", ["main.py"])
    def test_parse_default_arguments(self):
        """Test avec les arguments par défaut."""
        args = parse_cli_arguments()

        assert args.sources == ["nasa_exoplanet_archive"]
        assert args.use_mock == []
        assert args.skip_wikipedia_check is False
        assert args.output_dir == DEFAULT_OUTPUT_DIR
        assert args.drafts_dir == DEFAULT_DRAFTS_DIR

    @patch("sys.argv", ["main.py", "--sources", "nasa_exoplanet_archive", "exoplanet_eu"])
    def test_parse_multiple_sources(self):
        """Test avec plusieurs sources."""
        args = parse_cli_arguments()

        assert "nasa_exoplanet_archive" in args.sources
        assert "exoplanet_eu" in args.sources
        assert len(args.sources) == 2

    @patch("sys.argv", ["main.py", "--use-mock", "nasa_exoplanet_archive"])
    def test_parse_with_mock(self):
        """Test avec données mockées."""
        args = parse_cli_arguments()

        assert "nasa_exoplanet_archive" in args.use_mock

    @patch("sys.argv", ["main.py", "--skip-wikipedia-check"])
    def test_parse_skip_wikipedia(self):
        """Test de l'option skip-wikipedia-check."""
        args = parse_cli_arguments()

        assert args.skip_wikipedia_check is True

    @patch(
        "sys.argv",
        ["main.py", "--output-dir", "custom/output", "--drafts-dir", "custom/drafts"],
    )
    def test_parse_custom_directories(self):
        """Test avec répertoires personnalisés."""
        args = parse_cli_arguments()

        assert args.output_dir == "custom/output"
        assert args.drafts_dir == "custom/drafts"

    @patch(
        "sys.argv",
        ["main.py", "--use-mock", "nasa_exoplanet_archive", "--skip-wikipedia-check"],
    )
    def test_parse_combined_options(self):
        """Test avec plusieurs options combinées."""
        args = parse_cli_arguments()

        assert "nasa_exoplanet_archive" in args.use_mock
        assert args.skip_wikipedia_check is True
