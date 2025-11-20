"""
Tests unitaires pour draft_pipeline.

Ce module teste la génération et la persistance des brouillons d'articles.
"""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from src.models.entities.exoplanet_model import Exoplanet
from src.models.entities.star import Star
from src.models.references.reference import Reference, SourceType
from src.orchestration.draft_pipeline import (
    generate_and_persist_exoplanet_drafts,
    generate_and_persist_star_drafts,
)


class TestDraftPipeline:
    """Tests pour draft_pipeline."""

    @pytest.fixture
    def mock_processor(self):
        """Fixture pour créer un processeur mocké."""
        return Mock()

    @pytest.fixture
    def sample_exoplanets(self):
        """Fixture pour créer des exoplanètes de test."""
        ref = Reference(
            source=SourceType.NEA,
            star_id="Test",
            planet_id="Test b",
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )
        exo = Exoplanet(pl_name="Test b", st_name="Test", reference=ref)
        return [exo]

    @pytest.fixture
    def sample_stars(self):
        """Fixture pour créer des étoiles de test."""
        ref = Reference(
            source=SourceType.NEA,
            star_id="Test",
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )
        star = Star(st_name="Test", reference=ref)
        return [star]

    @patch("src.orchestration.draft_pipeline.persist_drafts_by_entity_type")
    @patch("src.orchestration.draft_pipeline.build_exoplanet_article_draft")
    def test_generate_and_persist_exoplanet_drafts(
        self, mock_build, mock_persist, mock_processor, sample_exoplanets
    ):
        """Test de génération et persistance de brouillons d'exoplanètes."""
        mock_processor.collect_all_exoplanets.return_value = sample_exoplanets
        mock_build.return_value = "Draft content"

        generate_and_persist_exoplanet_drafts(mock_processor, "drafts")

        mock_processor.collect_all_exoplanets.assert_called_once()
        mock_build.assert_called_once_with(sample_exoplanets[0])
        mock_persist.assert_called_once()

    @patch("src.orchestration.draft_pipeline.persist_drafts_by_entity_type")
    @patch("src.orchestration.draft_pipeline.build_star_article_draft")
    def test_generate_and_persist_star_drafts(
        self, mock_build, mock_persist, mock_processor, sample_stars
    ):
        """Test de génération et persistance de brouillons d'étoiles."""
        mock_processor.collect_all_stars.return_value = sample_stars
        mock_build.return_value = "Draft content"

        generate_and_persist_star_drafts(mock_processor, "drafts")

        mock_processor.collect_all_stars.assert_called_once()
        mock_build.assert_called_once()
        mock_persist.assert_called_once()

    @patch("src.orchestration.draft_pipeline.persist_drafts_by_entity_type")
    @patch("src.orchestration.draft_pipeline.build_star_article_draft")
    def test_generate_and_persist_star_drafts_with_exoplanets(
        self, mock_build, mock_persist, mock_processor, sample_stars, sample_exoplanets
    ):
        """Test de génération avec exoplanètes associées."""
        mock_processor.collect_all_stars.return_value = sample_stars
        mock_build.return_value = "Draft content"

        generate_and_persist_star_drafts(mock_processor, "drafts", sample_exoplanets)

        mock_processor.collect_all_stars.assert_called_once()
        mock_build.assert_called_once()
        # Vérifier que les exoplanètes sont passées
        call_args = mock_build.call_args
        assert "exoplanets" in call_args.kwargs

    @patch("src.orchestration.draft_pipeline.persist_drafts_by_entity_type")
    @patch("src.orchestration.draft_pipeline.build_exoplanet_article_draft")
    def test_generate_exoplanet_drafts_empty_list(self, mock_build, mock_persist, mock_processor):
        """Test avec liste vide d'exoplanètes."""
        mock_processor.collect_all_exoplanets.return_value = []

        generate_and_persist_exoplanet_drafts(mock_processor, "drafts")

        mock_build.assert_not_called()
        mock_persist.assert_called_once()

    @patch("src.orchestration.draft_pipeline.persist_drafts_by_entity_type")
    @patch("src.orchestration.draft_pipeline.build_star_article_draft")
    def test_generate_star_drafts_empty_list(self, mock_build, mock_persist, mock_processor):
        """Test avec liste vide d'étoiles."""
        mock_processor.collect_all_stars.return_value = []

        generate_and_persist_star_drafts(mock_processor, "drafts")

        mock_build.assert_not_called()
        mock_persist.assert_called_once()
