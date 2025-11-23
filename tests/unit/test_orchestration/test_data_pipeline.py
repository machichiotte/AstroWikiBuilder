"""
Tests unitaires pour le module data_pipeline.

Ce module teste les fonctions de collecte, ingestion et export de données.
"""

from datetime import datetime
from unittest.mock import Mock, mock_open, patch

import pytest

from src.models.entities.exoplanet_entity import Exoplanet
from src.models.entities.star_entity import Star
from src.models.references.reference import Reference, SourceType
from src.orchestration.data_pipeline import (
    _export_statistics_json,
    _log_statistics,
    export_consolidated_data,
    fetch_and_ingest_data,
    generate_and_export_statistics,
)


class TestFetchAndIngestData:
    """Tests pour fetch_and_ingest_data."""

    @pytest.fixture
    def mock_processor(self):
        """Fixture pour créer un processeur mocké."""
        processor = Mock()
        processor.ingest_exoplanets_from_source = Mock()
        processor.ingest_stars_from_source = Mock()
        return processor

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
        return Exoplanet(pl_name="Test b", st_name="Test", reference=ref)

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

    def test_fetch_and_ingest_data_success(
        self, mock_processor, sample_exoplanet, sample_star
    ):
        """Test de collecte et ingestion réussie."""
        mock_collector = Mock()
        mock_collector.collect_entities_from_source.return_value = (
            [sample_exoplanet],
            [sample_star],
        )

        collectors = {"NEA": mock_collector}

        fetch_and_ingest_data(collectors, mock_processor)

        # Vérifier que l'ingestion a été appelée
        mock_processor.ingest_exoplanets_from_source.assert_called_once_with(
            [sample_exoplanet], "NEA"
        )
        mock_processor.ingest_stars_from_source.assert_called_once_with(
            [sample_star], "NEA"
        )

    def test_fetch_and_ingest_data_empty_results(self, mock_processor):
        """Test avec résultats vides."""
        mock_collector = Mock()
        mock_collector.collect_entities_from_source.return_value = ([], None)

        collectors = {"NEA": mock_collector}

        fetch_and_ingest_data(collectors, mock_processor)

        # Vérifier que l'ingestion n'a pas été appelée
        mock_processor.ingest_exoplanets_from_source.assert_not_called()
        mock_processor.ingest_stars_from_source.assert_not_called()

    def test_fetch_and_ingest_data_invalid_type_exoplanets(self, mock_processor):
        """Test avec type invalide pour exoplanets."""
        mock_collector = Mock()
        mock_collector.collect_entities_from_source.return_value = ("invalid", None)

        collectors = {"NEA": mock_collector}

        # Ne doit pas lever d'exception, juste logger un warning
        fetch_and_ingest_data(collectors, mock_processor)

        # Vérifier que l'ingestion n'a pas été appelée
        mock_processor.ingest_exoplanets_from_source.assert_not_called()

    def test_fetch_and_ingest_data_invalid_type_stars(
        self, mock_processor, sample_exoplanet
    ):
        """Test avec type invalide pour stars."""
        mock_collector = Mock()
        mock_collector.collect_entities_from_source.return_value = (
            [sample_exoplanet],
            "invalid",
        )

        collectors = {"NEA": mock_collector}

        # Ne doit pas lever d'exception, juste logger un warning
        fetch_and_ingest_data(collectors, mock_processor)

        # Vérifier qu'aucune ingestion n'a été appelée (TypeError catchée)
        mock_processor.ingest_exoplanets_from_source.assert_not_called()
        mock_processor.ingest_stars_from_source.assert_not_called()

    def test_fetch_and_ingest_data_collector_exception(self, mock_processor):
        """Test avec exception levée par le collecteur."""
        mock_collector = Mock()
        mock_collector.collect_entities_from_source.side_effect = Exception(
            "Test error"
        )

        collectors = {"NEA": mock_collector}

        # Ne doit pas lever d'exception, juste logger un warning
        fetch_and_ingest_data(collectors, mock_processor)

        # Vérifier que l'ingestion n'a pas été appelée
        mock_processor.ingest_exoplanets_from_source.assert_not_called()

    def test_fetch_and_ingest_data_multiple_collectors(
        self, mock_processor, sample_exoplanet, sample_star
    ):
        """Test avec plusieurs collecteurs."""
        mock_collector1 = Mock()
        mock_collector1.collect_entities_from_source.return_value = (
            [sample_exoplanet],
            [sample_star],
        )

        mock_collector2 = Mock()
        mock_collector2.collect_entities_from_source.return_value = (
            [sample_exoplanet],
            None,
        )

        collectors = {"NEA": mock_collector1, "EU": mock_collector2}

        fetch_and_ingest_data(collectors, mock_processor)

        # Vérifier que l'ingestion a été appelée pour les deux sources
        assert mock_processor.ingest_exoplanets_from_source.call_count == 2
        assert mock_processor.ingest_stars_from_source.call_count == 1


class TestExportConsolidatedData:
    """Tests pour export_consolidated_data."""

    @pytest.fixture
    def mock_processor(self):
        """Fixture pour créer un processeur mocké."""
        processor = Mock()
        processor.export_all_exoplanets = Mock()
        return processor

    def test_export_consolidated_data_success(self, mock_processor, tmp_path):
        """Test d'export réussi."""
        output_dir = str(tmp_path)
        timestamp = "20231120_120000"

        export_consolidated_data(mock_processor, output_dir, timestamp)

        # Vérifier que l'export a été appelé
        expected_path = (
            f"{output_dir}/consolidated/exoplanets_consolidated_{timestamp}.csv"
        )
        mock_processor.export_all_exoplanets.assert_called_once_with(
            "csv", expected_path
        )

    def test_export_consolidated_data_exception(self, mock_processor, tmp_path):
        """Test avec exception lors de l'export."""
        mock_processor.export_all_exoplanets.side_effect = Exception("Export error")

        output_dir = str(tmp_path)
        timestamp = "20231120_120000"

        # Ne doit pas lever d'exception, juste logger une erreur
        export_consolidated_data(mock_processor, output_dir, timestamp)


class TestGenerateAndExportStatistics:
    """Tests pour generate_and_export_statistics."""

    @pytest.fixture
    def mock_stat_service(self):
        """Fixture pour créer un service de stats mocké."""
        service = Mock()
        service.generate_statistics_exoplanet.return_value = {
            "total": 100,
            "discovery_methods": {"Transit": 80, "Radial Velocity": 20},
            "discovery_years": {2020: 50, 2021: 50},
            "mass_ranges": {"< 1 MJ": 60, "1-10 MJ": 40},
            "radius_ranges": {"< 1 RJ": 70, "1-2 RJ": 30},
        }
        service.generate_statistics_star.return_value = {
            "total_stars": 80,
            "spectral_types": {"G": 40, "K": 30, "M": 10},
            "data_points_by_source": {"NEA": 80},
        }
        return service

    @pytest.fixture
    def mock_processor(self):
        """Fixture pour créer un processeur mocké."""
        processor = Mock()
        processor.collect_all_exoplanets.return_value = []
        processor.collect_all_stars.return_value = []
        return processor

    def test_generate_and_export_statistics_without_timestamp(
        self, mock_stat_service, mock_processor, tmp_path
    ):
        """Test de génération de stats sans export."""
        output_dir = str(tmp_path)

        stats = generate_and_export_statistics(
            mock_stat_service, mock_processor, output_dir, timestamp=None
        )

        # Vérifier que les stats ont été générées
        assert "exoplanet" in stats
        assert "star" in stats
        assert stats["exoplanet"]["total"] == 100
        assert stats["star"]["total_stars"] == 80

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_generate_and_export_statistics_with_timestamp(
        self, mock_makedirs, mock_file, mock_stat_service, mock_processor, tmp_path
    ):
        """Test de génération de stats avec export."""
        output_dir = str(tmp_path)
        timestamp = "20231120_120000"

        stats = generate_and_export_statistics(
            mock_stat_service, mock_processor, output_dir, timestamp=timestamp
        )

        # Vérifier que les stats ont été générées
        assert "exoplanet" in stats
        assert "star" in stats

        # Vérifier que le répertoire a été créé
        mock_makedirs.assert_called_once()

        # Vérifier que le fichier a été ouvert
        assert mock_file.called


class TestLogStatistics:
    """Tests pour _log_statistics."""

    def test_log_statistics_complete(self):
        """Test de logging de stats complètes."""
        stats = {
            "exoplanet": {
                "total": 100,
                "discovery_methods": {"Transit": 80, "Radial Velocity": 20},
                "discovery_years": {2020: 50, 2021: 50},
                "mass_ranges": {"< 1 MJ": 60, "1-10 MJ": 40},
                "radius_ranges": {"< 1 RJ": 70, "1-2 RJ": 30},
            },
            "star": {
                "total_stars": 80,
                "spectral_types": {"G": 40, "K": 30, "M": 10},
                "data_points_by_source": {"NEA": 80},
            },
        }

        # Ne doit pas lever d'exception
        _log_statistics(stats)

    def test_log_statistics_empty(self):
        """Test de logging de stats vides."""
        stats = {"exoplanet": {}, "star": {}}

        # Ne doit pas lever d'exception
        _log_statistics(stats)


class TestExportStatisticsJson:
    """Tests pour _export_statistics_json."""

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_export_statistics_json(self, mock_makedirs, mock_file, tmp_path):
        """Test d'export JSON."""
        stats = {"exoplanet": {"total": 100}, "star": {"total_stars": 80}}
        output_dir = str(tmp_path)
        timestamp = "20231120_120000"

        _export_statistics_json(stats, output_dir, timestamp)

        # Vérifier que le répertoire a été créé
        mock_makedirs.assert_called_once()

        # Vérifier que le fichier a été ouvert
        assert mock_file.called
