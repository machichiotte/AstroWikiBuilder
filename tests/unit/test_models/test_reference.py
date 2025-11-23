# tests/unit/test_models/test_reference.py
"""
Tests pour le modèle Reference.
"""

from datetime import datetime

import pytest

from src.models.references.reference import Reference, SourceType


class TestReference:
    """Tests du modèle Reference."""

    def test_create_reference_with_all_fields(self):
        """Test de création d'une référence avec tous les champs."""
        ref = Reference(
            source=SourceType.NEA,
            update_date=datetime(2025, 1, 1),
            consultation_date=datetime(2025, 1, 15),
            star_id="HD 209458",
            planet_id="HD 209458 b",
        )

        assert ref.source == SourceType.NEA
        assert ref.update_date == datetime(2025, 1, 1)
        assert ref.consultation_date == datetime(2025, 1, 15)
        assert ref.star_id == "HD 209458"
        assert ref.planet_id == "HD 209458 b"

    def test_reference_with_minimal_fields(self):
        """Test avec champs minimaux."""
        ref = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )

        assert ref.source == SourceType.NEA
        assert ref.star_id is None
        assert ref.planet_id is None

    def test_source_types(self):
        """Test des différents types de source."""
        assert SourceType.NEA.value == "NEA"
        # Vérifier que l'enum existe
        assert hasattr(SourceType, "NEA")

    def test_reference_str_representation(self):
        """Test de la représentation string."""
        ref = Reference(
            source=SourceType.NEA,
            update_date=datetime(2025, 1, 1),
            consultation_date=datetime(2025, 1, 15),
            planet_id="HD 209458 b",
        )

        str_repr = str(ref)
        assert "NEA" in str_repr

    def test_to_url_with_unknown_source(self):
        """Test de to_url() avec une source inconnue."""
        from unittest.mock import Mock

        # Créer une source mockée
        unknown_source = Mock(spec=SourceType)
        unknown_source.value = "UNKNOWN"

        ref = Reference(
            source=unknown_source,
            update_date=datetime(2025, 1, 1),
            consultation_date=datetime(2025, 1, 15),
            planet_id="Test b",
        )

        # SOURCE_DETAILS ne contient pas cette source
        with pytest.raises(ValueError, match="Unknown source"):
            ref.to_url()

    def test_to_url_nea_without_identifiers(self):
        """Test de to_url() pour NEA sans star_id ni planet_id."""
        ref = Reference(
            source=SourceType.NEA,
            update_date=datetime(2025, 1, 1),
            consultation_date=datetime(2025, 1, 15),
        )

        with pytest.raises(ValueError, match="Both star name and planet identifier are required"):
            ref.to_url()

    def test_to_url_nea_with_only_star_id(self):
        """Test de to_url() pour NEA avec seulement star_id."""
        ref = Reference(
            source=SourceType.NEA,
            update_date=datetime(2025, 1, 1),
            consultation_date=datetime(2025, 1, 15),
            star_id="HD 209458",
        )

        url = ref.to_url()
        assert "hd-209458" in url
        assert "overview" in url

    def test_to_url_epe_without_planet_id(self):
        """Test de to_url() pour EPE sans planet_id."""
        ref = Reference(
            source=SourceType.EPE,
            update_date=datetime(2025, 1, 1),
            consultation_date=datetime(2025, 1, 15),
        )

        with pytest.raises(ValueError, match="Identifier is required"):
            ref.to_url()

    def test_to_url_oec_without_planet_id(self):
        """Test de to_url() pour OEC sans planet_id."""
        ref = Reference(
            source=SourceType.OEC,
            update_date=datetime(2025, 1, 1),
            consultation_date=datetime(2025, 1, 15),
        )

        with pytest.raises(ValueError, match="Identifier is required"):
            ref.to_url()

    def test_to_wiki_ref_with_unknown_source(self):
        """Test de to_wiki_ref() avec une source inconnue."""
        from unittest.mock import Mock

        # Créer une source mockée
        unknown_source = Mock(spec=SourceType)
        unknown_source.value = "UNKNOWN"

        ref = Reference(
            source=unknown_source,
            update_date=datetime(2025, 1, 1),
            consultation_date=datetime(2025, 1, 15),
            planet_id="Test b",
        )

        # SOURCE_DETAILS ne contient pas cette source
        result = ref.to_wiki_ref()
        assert "Unknown source" in result
        assert "UNKNOWN" in result
