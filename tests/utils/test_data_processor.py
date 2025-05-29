import unittest
from unittest.mock import MagicMock, patch

from src.utils.data_processor import DataProcessor
from src.models.exoplanet import Exoplanet
from src.utils.wikipedia_checker import WikiArticleInfo
# Assuming ExoplanetRepository, StatisticsService, WikipediaService, ExportService are importable for type hinting if needed
# but they are mocked, so direct import might not be strictly necessary for runtime.


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        """
        Set up for each test method.
        This method is called before each test function is executed.
        """
        self.mock_repository = MagicMock()
        self.mock_stat_service = MagicMock()
        self.mock_wiki_service = MagicMock()
        self.mock_export_service = MagicMock()

        self.processor = DataProcessor(
            repository=self.mock_repository,
            stat_service=self.mock_stat_service,
            wiki_service=self.mock_wiki_service,
            export_service=self.mock_export_service,
        )

    def test_initialization(self):
        """Test that DataProcessor initializes with its dependencies."""
        self.assertIsNotNone(self.processor.exoplanet_repository)
        self.assertIsNotNone(self.processor.stat_service)
        self.assertIsNotNone(self.processor.wiki_service)
        self.assertIsNotNone(self.processor.export_service)
        # Check if logger is available, though not strictly necessary for this test
        self.assertTrue(hasattr(self.processor, "logger"))

    def test_add_exoplanets_from_source(self):
        """Test adding exoplanets from a source."""
        sample_exoplanets = [Exoplanet(name="PlanetA"), Exoplanet(name="PlanetB")]
        self.processor.add_exoplanets_from_source(sample_exoplanets, "test_source")
        self.mock_repository.add_exoplanets.assert_called_once_with(
            sample_exoplanets, "test_source"
        )

    def test_get_all_exoplanets(self):
        """Test getting all exoplanets."""
        expected_exoplanets = [Exoplanet(name="PlanetA")]
        self.mock_repository.get_all_exoplanets.return_value = expected_exoplanets

        result = self.processor.get_all_exoplanets()

        self.mock_repository.get_all_exoplanets.assert_called_once()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "PlanetA")
        self.assertEqual(result, expected_exoplanets)

    def test_get_statistics(self):
        """Test getting statistics."""
        mock_exoplanets = [Exoplanet(name="PlanetA")]
        self.mock_repository.get_all_exoplanets.return_value = mock_exoplanets
        expected_stats = {"total": 1, "discovery_methods": {"Transit": 1}}
        self.mock_stat_service.generate_statistics.return_value = expected_stats

        result = self.processor.get_statistics()

        self.mock_repository.get_all_exoplanets.assert_called_once()
        self.mock_stat_service.generate_statistics.assert_called_once_with(
            mock_exoplanets
        )
        self.assertEqual(result, expected_stats)

    def test_get_and_separate_wikipedia_articles_by_status(self):
        """Test getting and separating Wikipedia articles by status."""
        mock_exoplanets = [Exoplanet(name="PlanetA")]
        mock_all_articles_info = {
            "PlanetA": {
                "enwiki": WikiArticleInfo(
                    query_name="PlanetA",
                    article_exists=True,
                    title="PlanetA_title",
                    url="http://en.wikipedia.org/wiki/PlanetA_title",
                    is_redirect=False,
                    redirect_target=None,
                )
            }
        }
        # Simplified mock_separated_articles structure
        mock_separated_articles = (
            {"PlanetA": mock_all_articles_info["PlanetA"]},  # existing
            {},  # missing
        )

        self.mock_repository.get_all_exoplanets.return_value = mock_exoplanets
        self.mock_wiki_service.get_all_articles_info_for_exoplanets.return_value = (
            mock_all_articles_info
        )
        self.mock_wiki_service.separate_articles_by_status.return_value = (
            mock_separated_articles
        )

        existing, missing = (
            self.processor.get_and_separate_wikipedia_articles_by_status()
        )

        self.mock_repository.get_all_exoplanets.assert_called_once()
        self.mock_wiki_service.get_all_articles_info_for_exoplanets.assert_called_once_with(
            mock_exoplanets
        )
        self.mock_wiki_service.separate_articles_by_status.assert_called_once_with(
            mock_all_articles_info
        )
        self.assertEqual(existing, mock_separated_articles[0])
        self.assertEqual(missing, mock_separated_articles[1])

    def test_get_and_separate_wikipedia_articles_by_status_no_repo_data(self):
        """Test separation when no exoplanets are in the repository."""
        self.mock_repository.get_all_exoplanets.return_value = []

        existing, missing = (
            self.processor.get_and_separate_wikipedia_articles_by_status()
        )

        self.mock_repository.get_all_exoplanets.assert_called_once()
        # get_all_articles_info_for_exoplanets is called, but returns {} due to no exoplanets
        self.mock_wiki_service.get_all_articles_info_for_exoplanets.assert_called_once_with(
            []
        )
        # separate_articles_by_status should not be called if all_articles_info is empty
        # as per the logic in DataProcessor (it returns {}, {} before calling separate_articles_by_status)
        self.mock_wiki_service.separate_articles_by_status.assert_not_called()
        self.assertEqual(existing, {})
        self.assertEqual(missing, {})

    def test_get_and_separate_wikipedia_articles_by_status_no_wiki_info(self):
        """Test separation when Wikipedia service returns no article info."""
        mock_exoplanets = [Exoplanet(name="PlanetA")]
        self.mock_repository.get_all_exoplanets.return_value = mock_exoplanets
        self.mock_wiki_service.get_all_articles_info_for_exoplanets.return_value = {}  # No info found

        existing, missing = (
            self.processor.get_and_separate_wikipedia_articles_by_status()
        )

        self.mock_repository.get_all_exoplanets.assert_called_once()
        self.mock_wiki_service.get_all_articles_info_for_exoplanets.assert_called_once_with(
            mock_exoplanets
        )
        # separate_articles_by_status should not be called if all_articles_info is empty
        self.mock_wiki_service.separate_articles_by_status.assert_not_called()
        self.assertEqual(existing, {})
        self.assertEqual(missing, {})

    def test_export_exoplanet_data_csv(self):
        """Test exporting exoplanet data to CSV."""
        mock_exoplanets = [Exoplanet(name="PlanetA")]
        self.mock_repository.get_all_exoplanets.return_value = mock_exoplanets

        self.processor.export_exoplanet_data("csv", "file.csv")

        self.mock_repository.get_all_exoplanets.assert_called_once()
        self.mock_export_service.export_exoplanets_to_csv.assert_called_once_with(
            "file.csv", mock_exoplanets
        )

    def test_export_exoplanet_data_json(self):
        """Test exporting exoplanet data to JSON."""
        mock_exoplanets = [Exoplanet(name="PlanetA")]
        self.mock_repository.get_all_exoplanets.return_value = mock_exoplanets

        self.processor.export_exoplanet_data("json", "file.json")

        self.mock_repository.get_all_exoplanets.assert_called_once()
        self.mock_export_service.export_exoplanets_to_json.assert_called_once_with(
            "file.json", mock_exoplanets
        )

    def test_export_exoplanet_data_unsupported(self):
        """Test exporting with an unsupported format raises ValueError."""
        # No need to mock repository here as it should fail before that
        with self.assertRaises(ValueError):
            self.processor.export_exoplanet_data("xml", "file.xml")
        self.mock_export_service.export_exoplanets_to_csv.assert_not_called()
        self.mock_export_service.export_exoplanets_to_json.assert_not_called()

    def test_export_wikipedia_links_data(self):
        """Test exporting Wikipedia links data."""
        mock_repo_exoplanets = [
            Exoplanet(name="PlanetA", host_star=MagicMock())
        ]  # Added host_star as it's in headers
        self.mock_repository.get_all_exoplanets.return_value = mock_repo_exoplanets

        mock_wiki_article_info = WikiArticleInfo(
            query_name="PlanetA",
            article_exists=True,
            title="PlanetA_title",
            url="url",
            is_redirect=False,
            redirect_target=None,
        )
        mock_wiki_data_map = {"PlanetA": {"enwiki": mock_wiki_article_info}}

        mock_formatted_list = [
            {
                "exoplanet_primary_name": "PlanetA",
                "queried_name": "PlanetA",
                "article_exists": True,
                "wikipedia_title": "PlanetA_title",
                "is_redirect": False,
                "redirect_target": None,
                "url": "url",
                "host_star": "Some Star",  # Assuming format_wiki_links_data_for_export extracts this
            }
        ]
        self.mock_wiki_service.format_wiki_links_data_for_export.return_value = (
            mock_formatted_list
        )

        self.processor.export_wikipedia_links_data(
            "base_file", mock_wiki_data_map, "existing"
        )

        self.mock_repository.get_all_exoplanets.assert_called_once()  # Called by export_wikipedia_links_data
        self.mock_wiki_service.format_wiki_links_data_for_export.assert_called_once_with(
            mock_repo_exoplanets, mock_wiki_data_map
        )

        self.mock_export_service.export_generic_list_of_dicts_to_csv.assert_called_once()
        args_csv, kwargs_csv = (
            self.mock_export_service.export_generic_list_of_dicts_to_csv.call_args
        )
        self.assertEqual(args_csv[0], "base_file_existing_wiki_links.csv")
        self.assertEqual(args_csv[1], mock_formatted_list)
        self.assertIn("headers", kwargs_csv)  # Check if headers are passed

        self.mock_export_service.export_generic_list_of_dicts_to_json.assert_called_once()
        args_json, _ = (
            self.mock_export_service.export_generic_list_of_dicts_to_json.call_args
        )
        self.assertEqual(args_json[0], "base_file_existing_wiki_links.json")
        self.assertEqual(args_json[1], mock_formatted_list)

    def test_export_wikipedia_links_data_no_repo_data(self):
        """Test export when repository has no exoplanets."""
        self.mock_repository.get_all_exoplanets.return_value = []

        # Call the method with an empty map as well, as it would be if no data
        self.processor.export_wikipedia_links_data("base", {}, "existing")

        self.mock_repository.get_all_exoplanets.assert_called_once()
        self.mock_wiki_service.format_wiki_links_data_for_export.assert_not_called()
        self.mock_export_service.export_generic_list_of_dicts_to_csv.assert_not_called()
        self.mock_export_service.export_generic_list_of_dicts_to_json.assert_not_called()

    def test_export_wikipedia_links_data_no_wiki_map_data(self):
        """Test export when the wiki_data_map_to_export is empty."""
        mock_repo_exoplanets = [Exoplanet(name="PlanetA")]
        self.mock_repository.get_all_exoplanets.return_value = mock_repo_exoplanets

        self.processor.export_wikipedia_links_data("base", {}, "existing")  # Empty map

        self.mock_repository.get_all_exoplanets.assert_called_once()  # Still called
        # format_wiki_links_data_for_export should not be called if wiki_data_map_to_export is empty
        # as per DataProcessor's internal logic.
        self.mock_wiki_service.format_wiki_links_data_for_export.assert_not_called()
        self.mock_export_service.export_generic_list_of_dicts_to_csv.assert_not_called()
        self.mock_export_service.export_generic_list_of_dicts_to_json.assert_not_called()

    def test_export_wikipedia_links_data_no_formatted_list(self):
        """Test export when formatting returns an empty list."""
        mock_repo_exoplanets = [Exoplanet(name="PlanetA")]
        self.mock_repository.get_all_exoplanets.return_value = mock_repo_exoplanets

        mock_wiki_article_info = WikiArticleInfo(
            query_name="PlanetA",
            article_exists=True,
            title="PlanetA_title",
            url="url",
            is_redirect=False,
            redirect_target=None,
        )
        mock_wiki_data_map = {"PlanetA": {"enwiki": mock_wiki_article_info}}

        self.mock_wiki_service.format_wiki_links_data_for_export.return_value = []  # Empty formatted list

        self.processor.export_wikipedia_links_data(
            "base", mock_wiki_data_map, "existing"
        )

        self.mock_repository.get_all_exoplanets.assert_called_once()
        self.mock_wiki_service.format_wiki_links_data_for_export.assert_called_once_with(
            mock_repo_exoplanets, mock_wiki_data_map
        )
        self.mock_export_service.export_generic_list_of_dicts_to_csv.assert_not_called()
        self.mock_export_service.export_generic_list_of_dicts_to_json.assert_not_called()


if __name__ == "__main__":
    unittest.main()
