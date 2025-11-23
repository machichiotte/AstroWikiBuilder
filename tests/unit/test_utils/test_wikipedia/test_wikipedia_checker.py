"""Tests pour WikipediaChecker."""

from unittest.mock import Mock, patch

import pytest
import requests

from src.utils.wikipedia.wikipedia_checker import WikiArticleInfo, WikipediaChecker


class TestWikipediaChecker:
    """Tests pour WikipediaChecker."""

    @pytest.fixture
    def checker(self):
        """Fixture pour créer un WikipediaChecker."""
        return WikipediaChecker(user_agent="TestBot/1.0")

    def test_init_with_custom_user_agent(self):
        """Test de l'initialisation avec un user agent personnalisé."""
        checker = WikipediaChecker(user_agent="CustomBot/2.0")
        assert checker.session.headers["User-Agent"] == "CustomBot/2.0"

    def test_init_with_default_user_agent(self):
        """Test de l'initialisation avec le user agent par défaut."""
        checker = WikipediaChecker()
        assert "AstroWikiBuilder" in checker.session.headers["User-Agent"]

    def test_normalize_title_basic(self, checker):
        """Test de normalisation basique d'un titre."""
        assert checker._normalize_title("Test Article") == "test-article"

    def test_normalize_title_with_accents(self, checker):
        """Test de normalisation avec des accents."""
        assert checker._normalize_title("Café Français") == "cafe-francais"

    def test_normalize_title_with_special_chars(self, checker):
        """Test de normalisation avec des caractères spéciaux."""
        assert checker._normalize_title("Test@Article#123") == "testarticle123"

    def test_normalize_title_with_underscores(self, checker):
        """Test de normalisation avec des underscores."""
        assert checker._normalize_title("Test_Article_Name") == "test-article-name"

    def test_normalize_title_with_multiple_spaces(self, checker):
        """Test de normalisation avec plusieurs espaces."""
        assert checker._normalize_title("Test   Article") == "test-article"

    def test_build_empty_article_info_results(self, checker):
        """Test de création de résultats vides."""
        titles = ["Article1", "Article2"]
        results = checker.build_empty_article_info_results(titles)

        assert len(results) == 2
        assert "Article1" in results
        assert "Article2" in results
        assert results["Article1"].exists is False
        assert results["Article1"].title == "Article1"
        assert results["Article1"].queried_title == "Article1"

    def test_check_article_existence_batch_empty_list(self, checker):
        """Test avec une liste vide."""
        results = checker.check_article_existence_batch([])
        assert results == {}

    def test_check_article_existence_batch_too_many_titles(self, checker):
        """Test avec plus de 50 titres."""
        titles = [f"Article{i}" for i in range(51)]
        with pytest.raises(ValueError, match="L'API MediaWiki limite à 50 titres"):
            checker.check_article_existence_batch(titles)

    @patch("requests.Session.get")
    def test_fetch_raw_article_query_from_mediawiki_success(self, mock_get, checker):
        """Test de récupération réussie depuis MediaWiki."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "query": {
                "pages": {
                    "123": {
                        "pageid": 123,
                        "title": "Test Article",
                        "fullurl": "https://fr.wikipedia.org/wiki/Test_Article",
                    }
                }
            }
        }
        mock_get.return_value = mock_response

        result = checker.fetch_raw_article_query_from_mediawiki(["Test Article"])

        assert "pages" in result
        mock_get.assert_called_once()

    @patch("requests.Session.get")
    def test_fetch_raw_article_query_from_mediawiki_error(self, mock_get, checker):
        """Test de gestion d'erreur lors de la récupération."""
        mock_get.side_effect = requests.RequestException("Network error")

        with pytest.raises(requests.RequestException):
            checker.fetch_raw_article_query_from_mediawiki(["Test Article"])

    def test_build_title_normalization_and_redirect_maps_no_data(self, checker):
        """Test de construction des maps sans données."""
        data = {}
        titles = ["Article1"]

        normalized, redirect, resolved = (
            checker.build_title_normalization_and_redirect_maps(data, titles)
        )

        assert normalized == {}
        assert redirect == {}
        assert "Article1" in resolved

    def test_build_title_normalization_and_redirect_maps_with_normalization(
        self, checker
    ):
        """Test de construction des maps avec normalisation."""
        data = {"normalized": [{"from": "article 1", "to": "Article 1"}]}
        titles = ["article 1"]

        normalized, redirect, resolved = (
            checker.build_title_normalization_and_redirect_maps(data, titles)
        )

        assert normalized["article 1"] == "Article 1"
        assert "Article 1" in resolved

    def test_build_title_normalization_and_redirect_maps_with_redirect(self, checker):
        """Test de construction des maps avec redirection."""
        data = {"redirects": [{"from": "Old Name", "to": "New Name"}]}
        titles = ["Old Name"]

        normalized, redirect, resolved = (
            checker.build_title_normalization_and_redirect_maps(data, titles)
        )

        assert redirect["Old Name"] == "New Name"

    def test_resolve_article_existence_missing_page(self, checker):
        """Test de résolution pour une page manquante."""
        data = {"pages": {"-1": {"title": "Missing Article", "missing": ""}}}
        results = {
            "Missing Article": WikiArticleInfo(
                exists=False, title="Missing Article", queried_title="Missing Article"
            )
        }
        resolved_map = {"Missing Article": "Missing Article"}
        # Correction : définir explicitement les cartes vides
        redirect_map = {}
        normalized_map = {}

        checker.resolve_article_existence_from_pages(
            data, resolved_map, redirect_map, normalized_map, results, None
        )

        assert results["Missing Article"].exists is False

    def test_resolve_article_existence_existing_page(self, checker):
        """Test de résolution pour une page existante."""
        data = {
            "pages": {
                "123": {
                    "pageid": 123,
                    "title": "Existing Article",
                    "fullurl": "https://fr.wikipedia.org/wiki/Existing_Article",
                }
            }
        }
        results = {
            "Existing Article": WikiArticleInfo(
                exists=False, title="Existing Article", queried_title="Existing Article"
            )
        }
        resolved_map = {"Existing Article": "Existing Article"}
        # Correction : définir explicitement les cartes vides
        redirect_map = {}
        normalized_map = {}

        checker.resolve_article_existence_from_pages(
            data, resolved_map, redirect_map, normalized_map, results, None
        )

        assert results["Existing Article"].exists is True
        assert (
            results["Existing Article"].url
            == "https://fr.wikipedia.org/wiki/Existing_Article"
        )

    def test_resolve_article_existence_with_redirect(self, checker):
        """Test de résolution avec redirection."""
        data = {
            "pages": {
                "123": {
                    "pageid": 123,
                    "title": "Target Article",
                    "fullurl": "https://fr.wikipedia.org/wiki/Target_Article",
                }
            }
        }
        results = {
            "Source Article": WikiArticleInfo(
                exists=False, title="Source Article", queried_title="Source Article"
            )
        }
        resolved_map = {"Target Article": "Source Article"}
        redirect_map = {"Source Article": "Target Article"}
        # Correction : définir explicitement la carte vide
        normalized_map = {}

        checker.resolve_article_existence_from_pages(
            data, resolved_map, redirect_map, normalized_map, results, None
        )

        assert results["Source Article"].exists is True
        assert results["Source Article"].is_redirect is True
        assert results["Source Article"].redirect_target == "Target Article"

    def test_resolve_article_existence_with_host_star_match(self, checker):
        """Test de résolution avec correspondance d'étoile hôte."""
        data = {
            "pages": {
                "123": {
                    "pageid": 123,
                    "title": "Kepler-22",
                    "fullurl": "https://fr.wikipedia.org/wiki/Kepler-22",
                }
            }
        }
        results = {
            "Kepler-22 b": WikiArticleInfo(
                exists=False, title="Kepler-22 b", queried_title="Kepler-22 b"
            )
        }
        resolved_map = {"Kepler-22": "Kepler-22 b"}
        exoplanet_context = {"Kepler-22 b": {"st_name": "Kepler-22"}}
        # Correction : définir explicitement les cartes vides
        redirect_map = {}
        normalized_map = {}

        checker.resolve_article_existence_from_pages(
            data, resolved_map, redirect_map, normalized_map, results, exoplanet_context
        )

        assert results["Kepler-22 b"].exists is False
        assert results["Kepler-22 b"].host_star == "Kepler-22"

    @patch("requests.Session.get")
    def test_check_article_existence_batch_api_error(self, mock_get, checker):
        """Test de gestion d'erreur API."""
        mock_get.side_effect = requests.RequestException("API Error")

        results = checker.check_article_existence_batch(["Test Article"])

        assert "Test Article" in results
        assert "Erreur API" in results["Test Article"].url

    @patch("requests.Session.get")
    def test_check_article_existence_batch_full_workflow(self, mock_get, checker):
        """Test du workflow complet."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "query": {
                "pages": {
                    "123": {
                        "pageid": 123,
                        "title": "Test Article",
                        "fullurl": "https://fr.wikipedia.org/wiki/Test_Article",
                    }
                }
            }
        }
        mock_get.return_value = mock_response

        results = checker.check_article_existence_batch(["Test Article"])

        assert "Test Article" in results
        assert results["Test Article"].exists is True
        assert (
            results["Test Article"].url == "https://fr.wikipedia.org/wiki/Test_Article"
        )
