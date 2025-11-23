"""Tests unitaires pour service_initializer."""

import argparse
import os
from unittest.mock import ANY, Mock, patch

import pytest

from src.collectors.implementations.exoplanet_eu_collector import ExoplanetEUCollector
from src.collectors.implementations.nasa_exoplanet_archive_collector import (
    NasaExoplanetArchiveCollector,
)
from src.collectors.implementations.open_exoplanet_catalogue_collector import (
    OpenExoplanetCatalogueCollector,
)
from src.orchestration.service_initializer import (
    _get_collector_instance,
    _log_collector_initialization,
    initialize_collectors,
    initialize_services,
)
from src.services.external.export_service import ExportService
from src.services.external.wikipedia_service import WikipediaService
from src.services.processors.statistics_service import StatisticsService
from src.services.repositories.exoplanet_repository import ExoplanetRepository
from src.services.repositories.star_repository import StarRepository


class TestServiceInitializer:
    """Tests pour service_initializer."""

    @patch("src.orchestration.service_initializer.logger")
    def test_initialize_services_default_user_agent(self, mock_logger):
        """Test l'initialisation des services avec le User-Agent par défaut."""
        # S'assurer que la variable d'environnement n'est pas définie
        with patch.dict(os.environ, {}, clear=True):
            (
                exoplanet_repo,
                star_repo,
                stat_service,
                wiki_service,
                export_service,
            ) = initialize_services()

            assert isinstance(exoplanet_repo, ExoplanetRepository)
            assert isinstance(star_repo, StarRepository)
            assert isinstance(stat_service, StatisticsService)
            assert isinstance(wiki_service, WikipediaService)
            assert isinstance(export_service, ExportService)

            # Vérifier le log pour le user agent par défaut
            assert any(
                "Using default Wikipedia User-Agent" in call[0][0]
                for call in mock_logger.info.call_args_list
            )

    @patch("src.orchestration.service_initializer.logger")
    def test_initialize_services_custom_user_agent(self, mock_logger):
        """Test l'initialisation des services avec un User-Agent personnalisé (ligne 65)."""
        custom_ua = "CustomBot/1.0"
        with patch.dict(os.environ, {"WIKI_USER_AGENT": custom_ua}):
            initialize_services()

            # Vérifier le log pour le user agent personnalisé
            # Le message attendu est: "Using Wikipedia User-Agent from environment variable WIKI_USER_AGENT: CustomBot/1.0"
            expected_msg = (
                f"Using Wikipedia User-Agent from environment variable WIKI_USER_AGENT: {custom_ua}"
            )
            assert any(
                expected_msg in call[0][0]
                for call in mock_logger.info.call_args_list
                if len(call[0]) > 0
                and isinstance(call[0][0], str)
                and "Using Wikipedia User-Agent" in call[0][0]
            )

    @patch("src.orchestration.service_initializer._get_collector_instance")
    def test_initialize_collectors_nasa(self, mock_get_instance):
        """Test l'initialisation du collecteur NASA."""
        args = argparse.Namespace(sources=["nasa_exoplanet_archive"], use_mock=[])
        mock_collector = Mock(spec=NasaExoplanetArchiveCollector)
        mock_get_instance.return_value = mock_collector

        collectors = initialize_collectors(args)

        assert "nasa_exoplanet_archive" in collectors
        assert collectors["nasa_exoplanet_archive"] == mock_collector
        mock_get_instance.assert_called_with("nasa_exoplanet_archive", False, ANY)

    def test_get_collector_instance_nasa(self):
        """Test la factory pour NASA."""
        collector = _get_collector_instance("nasa_exoplanet_archive", True, "cache.csv")
        assert isinstance(collector, NasaExoplanetArchiveCollector)

    def test_get_collector_instance_eu(self):
        """Test la factory pour ExoplanetEU (ligne 139)."""
        collector = _get_collector_instance("exoplanet_eu", True, "cache.csv")
        assert isinstance(collector, ExoplanetEUCollector)

    def test_get_collector_instance_open(self):
        """Test la factory pour OpenExoplanet (ligne 141)."""
        collector = _get_collector_instance("open_exoplanet", True, "cache.csv")
        assert isinstance(collector, OpenExoplanetCatalogueCollector)

    def test_get_collector_instance_unknown(self):
        """Test la factory avec source inconnue (ligne 143)."""
        with pytest.raises(ValueError, match="Source inconnue"):
            _get_collector_instance("unknown_source", True, "cache.csv")

    @patch("src.orchestration.service_initializer.logger")
    def test_log_collector_initialization_mock(self, mock_logger):
        """Test le logging avec mock (ligne 156)."""
        _log_collector_initialization("source", True, "cache.csv")
        mock_logger.info.assert_called_with(
            "Utilisation des données mockées pour source (chargement depuis cache.csv)."
        )

    @patch("src.orchestration.service_initializer.logger")
    def test_log_collector_initialization_real(self, mock_logger):
        """Test le logging sans mock (ligne 160)."""
        _log_collector_initialization("source", False, "cache.csv")
        mock_logger.info.assert_called_with(
            "sourceCollector initialisé pour télécharger les données (cache dans cache.csv)."
        )
