# tests/unit/test_models/test_reference.py
"""
Tests pour le modèle Reference.
"""

from datetime import datetime

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
