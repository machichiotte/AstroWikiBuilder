"""
Tests unitaires pour DataProcessor.

Ce module teste la coordination de l'ingestion, collecte, analyse et export des données.
"""

from datetime import datetime
from unittest.mock import Mock

import pytest

from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.entities.star_entity import Star
from src.models.references.reference import Reference, SourceType
from src.services.processors.data_processor import DataProcessor
from src.utils.wikipedia.wikipedia_checker import WikiArticleInfo


class TestDataProcessor:
    """Tests pour DataProcessor."""

    @pytest.fixture
    def mock_repositories_and_services(self):
        """Fixture pour créer tous les mocks nécessaires."""
        exoplanet_repo = Mock()
        star_repo = Mock()
        stat_service = Mock()
        wiki_service = Mock()
        export_service = Mock()

        return {
            "exoplanet_repo": exoplanet_repo,
            "star_repo": star_repo,
            "stat_service": stat_service,
            "wiki_service": wiki_service,
            "export_service": export_service,
        }

    @pytest.fixture
    def data_processor(self, mock_repositories_and_services):
        """Fixture pour créer un DataProcessor."""
        mocks = mock_repositories_and_services
        return DataProcessor(
            mocks["exoplanet_repo"],
            mocks["star_repo"],
            mocks["stat_service"],
            mocks["wiki_service"],
            mocks["export_service"],
        )

    @pytest.fixture
    def sample_exoplanet(self):
        """Fixture pour créer une exoplanète de test."""
        ref = Reference(
            source=SourceType.NEA,
            star_id="Test",
            planet_id="Test b",
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )
        return Exoplanet(
            pl_name="Test b",
            st_name="Test",
            pl_mass=ValueWithUncertainty(value=1.5),
            reference=ref,
        )

    @pytest.fixture
    def sample_star(self):
        """Fixture pour créer une étoile de test."""
        ref = Reference(
            source=SourceType.NEA,
            star_id="Test",
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )
        return Star(st_name="Test", reference=ref)

    def test_init(self, data_processor, mock_repositories_and_services):
        """Test d'initialisation."""
        mocks = mock_repositories_and_services
        assert data_processor.exoplanet_repository == mocks["exoplanet_repo"]
        assert data_processor.star_repository == mocks["star_repo"]
        assert data_processor.stat_service == mocks["stat_service"]
        assert data_processor.wiki_service == mocks["wiki_service"]
        assert data_processor.export_service == mocks["export_service"]

    def test_ingest_exoplanets_from_source(
        self, data_processor, mock_repositories_and_services, sample_exoplanet
    ):
        """Test d'ingestion d'exoplanètes."""
        exoplanets = [sample_exoplanet]
        data_processor.ingest_exoplanets_from_source(exoplanets, "NEA")

        mock_repositories_and_services["exoplanet_repo"].add_exoplanets.assert_called_once_with(
            exoplanets, "NEA"
        )

    def test_ingest_stars_from_source(
        self, data_processor, mock_repositories_and_services, sample_star
    ):
        """Test d'ingestion d'étoiles."""
        stars = [sample_star]
        data_processor.ingest_stars_from_source(stars, "NEA")

        mock_repositories_and_services["star_repo"].add_stars.assert_called_once_with(stars, "NEA")

    def test_collect_all_exoplanets(
        self, data_processor, mock_repositories_and_services, sample_exoplanet
    ):
        """Test de collecte de toutes les exoplanètes."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = [
            sample_exoplanet
        ]

        result = data_processor.collect_all_exoplanets()

        assert result == [sample_exoplanet]
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.assert_called_once()

    def test_collect_all_stars(self, data_processor, mock_repositories_and_services, sample_star):
        """Test de collecte de toutes les étoiles."""
        mock_repositories_and_services["star_repo"].get_all_stars.return_value = [sample_star]

        result = data_processor.collect_all_stars()

        assert result == [sample_star]
        mock_repositories_and_services["star_repo"].get_all_stars.assert_called_once()

    def test_compute_exoplanet_statistics(
        self, data_processor, mock_repositories_and_services, sample_exoplanet
    ):
        """Test de calcul des statistiques d'exoplanètes."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = [
            sample_exoplanet
        ]
        mock_repositories_and_services[
            "stat_service"
        ].generate_statistics_exoplanet.return_value = {"total": 1}

        result = data_processor.compute_exoplanet_statistics()

        assert result == {"total": 1}
        mock_repositories_and_services[
            "stat_service"
        ].generate_statistics_exoplanet.assert_called_once_with([sample_exoplanet])

    def test_compute_star_statistics(
        self, data_processor, mock_repositories_and_services, sample_star
    ):
        """Test de calcul des statistiques d'étoiles."""
        mock_repositories_and_services["star_repo"].get_all_stars.return_value = [sample_star]
        mock_repositories_and_services["stat_service"].generate_statistics_star.return_value = {
            "total_stars": 1
        }

        result = data_processor.compute_star_statistics()

        assert result == {"total_stars": 1}
        mock_repositories_and_services[
            "stat_service"
        ].generate_statistics_star.assert_called_once_with([sample_star])

    def test_generate_data_statistics(
        self, data_processor, mock_repositories_and_services, sample_exoplanet, sample_star
    ):
        """Test de génération de toutes les statistiques."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = [
            sample_exoplanet
        ]
        mock_repositories_and_services["star_repo"].get_all_stars.return_value = [sample_star]
        mock_repositories_and_services[
            "stat_service"
        ].generate_statistics_exoplanet.return_value = {"total": 1}
        mock_repositories_and_services["stat_service"].generate_statistics_star.return_value = {
            "total_stars": 1
        }

        result = data_processor.generate_data_statistics()

        assert "exoplanet" in result
        assert "star" in result
        assert result["exoplanet"] == {"total": 1}
        assert result["star"] == {"total_stars": 1}

    def test_fetch_wikipedia_articles_for_exoplanets(
        self, data_processor, mock_repositories_and_services, sample_exoplanet
    ):
        """Test de récupération des articles Wikipedia."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = [
            sample_exoplanet
        ]
        mock_repositories_and_services[
            "wiki_service"
        ].fetch_articles_for_exoplanet_batch.return_value = {"Test b": {}}

        result = data_processor.fetch_wikipedia_articles_for_exoplanets()

        assert result == {"Test b": {}}
        mock_repositories_and_services[
            "wiki_service"
        ].fetch_articles_for_exoplanet_batch.assert_called_once_with([sample_exoplanet])

    def test_fetch_wikipedia_articles_for_exoplanets_empty(
        self, data_processor, mock_repositories_and_services
    ):
        """Test de récupération avec aucune exoplanète."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = []

        result = data_processor.fetch_wikipedia_articles_for_exoplanets()

        assert result == {}

    def test_resolve_wikipedia_status_for_exoplanets(
        self, data_processor, mock_repositories_and_services, sample_exoplanet
    ):
        """Test de résolution du statut Wikipedia."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = [
            sample_exoplanet
        ]
        mock_repositories_and_services[
            "wiki_service"
        ].fetch_articles_for_exoplanet_batch.return_value = {
            "Test b": {
                "Test b": WikiArticleInfo(
                    exists=True,
                    title="Test b",
                    queried_title="Test b",
                    url="https://fr.wikipedia.org/wiki/Test_b",
                )
            }
        }
        mock_repositories_and_services["wiki_service"].split_by_article_existence.return_value = (
            {"Test b": {}},
            {},
        )

        existing, missing = data_processor.resolve_wikipedia_status_for_exoplanets()

        assert len(existing) == 1
        assert len(missing) == 0

    def test_resolve_wikipedia_status_for_exoplanets_empty(
        self, data_processor, mock_repositories_and_services
    ):
        """Test de résolution avec aucun article."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = []

        existing, missing = data_processor.resolve_wikipedia_status_for_exoplanets()

        assert existing == {}
        assert missing == {}

    def test_export_all_exoplanets_csv(
        self, data_processor, mock_repositories_and_services, sample_exoplanet
    ):
        """Test d'export CSV."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = [
            sample_exoplanet
        ]

        data_processor.export_all_exoplanets("csv", "test.csv")

        mock_repositories_and_services[
            "export_service"
        ].export_exoplanets_to_csv.assert_called_once_with("test.csv", [sample_exoplanet])

    def test_export_all_exoplanets_json(
        self, data_processor, mock_repositories_and_services, sample_exoplanet
    ):
        """Test d'export JSON."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = [
            sample_exoplanet
        ]

        data_processor.export_all_exoplanets("json", "test.json")

        mock_repositories_and_services[
            "export_service"
        ].export_exoplanets_to_json.assert_called_once_with("test.json", [sample_exoplanet])

    def test_export_all_exoplanets_invalid_format(
        self, data_processor, mock_repositories_and_services, sample_exoplanet
    ):
        """Test d'export avec format invalide."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = [
            sample_exoplanet
        ]

        with pytest.raises(ValueError, match="Unsupported export format"):
            data_processor.export_all_exoplanets("xml", "test.xml")

    def test_export_exoplanet_wikipedia_links_by_status(
        self, data_processor, mock_repositories_and_services, sample_exoplanet
    ):
        """Test d'export des liens Wikipedia."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = [
            sample_exoplanet
        ]
        mock_repositories_and_services[
            "wiki_service"
        ].format_article_links_for_export.return_value = [{"exoplanet_primary_name": "Test b"}]

        wiki_data = {"Test b": {}}
        data_processor.export_exoplanet_wikipedia_links_by_status(
            "output/test", wiki_data, "existing"
        )

        mock_repositories_and_services[
            "export_service"
        ].export_generic_list_of_dicts_to_csv.assert_called_once()
        mock_repositories_and_services[
            "export_service"
        ].export_generic_list_of_dicts_to_json.assert_called_once()

    def test_export_exoplanet_wikipedia_links_by_status_empty_repo(
        self, data_processor, mock_repositories_and_services
    ):
        """Test d'export avec repo vide."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = []

        wiki_data = {"Test b": {}}
        data_processor.export_exoplanet_wikipedia_links_by_status(
            "output/test", wiki_data, "existing"
        )

        mock_repositories_and_services[
            "export_service"
        ].export_generic_list_of_dicts_to_csv.assert_not_called()

    def test_export_exoplanet_wikipedia_links_by_status_empty_data(
        self, data_processor, mock_repositories_and_services, sample_exoplanet
    ):
        """Test d'export avec données vides."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = [
            sample_exoplanet
        ]

        data_processor.export_exoplanet_wikipedia_links_by_status("output/test", {}, "existing")

        mock_repositories_and_services[
            "export_service"
        ].export_generic_list_of_dicts_to_csv.assert_not_called()

    def test_export_exoplanet_wikipedia_links_by_status_empty_formatted(
        self, data_processor, mock_repositories_and_services, sample_exoplanet
    ):
        """Test d'export avec données formatées vides."""
        mock_repositories_and_services["exoplanet_repo"].get_all_exoplanets.return_value = [
            sample_exoplanet
        ]
        mock_repositories_and_services[
            "wiki_service"
        ].format_article_links_for_export.return_value = []

        wiki_data = {"Test b": {}}
        data_processor.export_exoplanet_wikipedia_links_by_status(
            "output/test", wiki_data, "existing"
        )

        mock_repositories_and_services[
            "export_service"
        ].export_generic_list_of_dicts_to_csv.assert_not_called()
