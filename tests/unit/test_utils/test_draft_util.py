"""
Tests unitaires pour draft_util.

Ce module teste les utilitaires de génération et sauvegarde de brouillons.
"""

from datetime import datetime
from unittest.mock import mock_open, patch

import pytest

from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.entities.star_entity import Star
from src.models.references.reference import Reference, SourceType
from src.utils.wikipedia.draft_util import (
    build_exoplanet_article_draft,
    build_star_article_draft,
    persist_drafts_by_entity_type,
    sanitize_draft_filename,
    write_separated_exoplanet_drafts,
    write_separated_star_drafts,
)


class TestSanitizeDraftFilename:
    """Tests pour sanitize_draft_filename."""

    def test_sanitize_simple_filename(self):
        """Test avec nom simple."""
        result = sanitize_draft_filename("Test b")
        assert result == "Test b"

    def test_sanitize_filename_with_invalid_chars(self):
        """Test avec caractères invalides."""
        result = sanitize_draft_filename('Test<>:"/\\|?*b')
        assert "<" not in result
        assert ">" not in result
        assert ":" not in result

    def test_sanitize_filename_with_double_underscores(self):
        """Test avec underscores multiples."""
        result = sanitize_draft_filename("Test___b")
        assert "___" not in result
        assert result == "Test_b"

    def test_sanitize_filename_with_value_with_uncertainty(self):
        """Test avec ValueWithUncertainty."""
        value = ValueWithUncertainty(value=123.45)
        result = sanitize_draft_filename(value)
        assert "123.45" in result

    def test_sanitize_filename_strips_underscores(self):
        """Test que les underscores en début/fin sont supprimés."""
        result = sanitize_draft_filename("_Test_b_")
        assert result == "Test_b"


class TestBuildArticleDrafts:
    """Tests pour build_exoplanet_article_draft et build_star_article_draft."""

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

    def test_build_exoplanet_article_draft(self, sample_exoplanet):
        """Test de génération de brouillon d'exoplanète."""
        result = build_exoplanet_article_draft(sample_exoplanet)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_build_star_article_draft(self, sample_star):
        """Test de génération de brouillon d'étoile."""
        result = build_star_article_draft(sample_star)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_build_star_article_draft_with_exoplanets(self, sample_star, sample_exoplanet):
        """Test de génération de brouillon d'étoile avec exoplanètes."""
        result = build_star_article_draft(sample_star, exoplanets=[sample_exoplanet])
        assert isinstance(result, str)
        assert len(result) > 0


class TestWriteSeparatedDrafts:
    """Tests pour write_separated_exoplanet_drafts et write_separated_star_drafts."""

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_write_separated_exoplanet_drafts(self, mock_makedirs, mock_file):
        """Test d'écriture de brouillons d'exoplanètes."""
        missing = [("Test b", "Content 1")]
        existing = [("Test c", "Content 2")]

        write_separated_exoplanet_drafts(missing, existing, "drafts/exoplanet")

        assert mock_makedirs.call_count == 2
        assert mock_file.call_count == 2

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_write_separated_star_drafts(self, mock_makedirs, mock_file):
        """Test d'écriture de brouillons d'étoiles."""
        missing = [("Test", "Content 1")]
        existing = [("Test 2", "Content 2")]

        write_separated_star_drafts(missing, existing, "drafts/star")

        assert mock_makedirs.call_count == 2
        assert mock_file.call_count == 2

    @patch("builtins.open", side_effect=OSError("Permission denied"))
    @patch("os.makedirs")
    def test_write_separated_exoplanet_drafts_error(self, mock_makedirs, mock_file):
        """Test de gestion d'erreur lors de l'écriture."""
        missing = [("Test b", "Content 1")]

        # Ne doit pas lever d'exception
        write_separated_exoplanet_drafts(missing, [], "drafts/exoplanet")


class TestPersistDraftsByEntityType:
    """Tests pour persist_drafts_by_entity_type."""

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_persist_drafts_by_entity_type(self, mock_makedirs, mock_file):
        """Test de persistance de brouillons."""
        missing = {"Test b": "Content 1"}
        existing = {"Test c": "Content 2"}

        persist_drafts_by_entity_type(missing, existing, "drafts", "exoplanet")

        # 2 pour les répertoires de base (missing_entity_dir, existing_entity_dir)
        # + 2 pour les sous-dossiers catalogue (un pour missing, un pour existing)
        assert mock_makedirs.call_count == 4
        assert mock_file.call_count == 2

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_persist_drafts_empty(self, mock_makedirs, mock_file):
        """Test avec dictionnaires vides."""
        persist_drafts_by_entity_type({}, {}, "drafts", "exoplanet")

        # Seulement les 2 répertoires de base sont créés
        assert mock_makedirs.call_count == 2
        mock_file.assert_not_called()
