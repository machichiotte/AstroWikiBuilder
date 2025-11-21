# tests/unit/test_models/test_star_entity.py
"""
Tests pour le modèle Star.
"""

from datetime import datetime

from src.models.entities.star_entity import Star
from src.models.references.reference import Reference, SourceType


class TestStar:
    """Tests du modèle Star."""

    def test_create_star_with_all_fields(self, sample_star):
        """Test de création d'une étoile avec tous les champs."""
        star = sample_star

        assert star.st_name == "HD 209458"
        assert star.st_spectral_type == "G0V"
        assert star.sy_constellation == "Pégase"
        assert star.st_distance.value == 47.1
        assert star.reference.source == SourceType.NEA

    def test_star_with_minimal_fields(self):
        """Test avec champs minimaux."""
        reference = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
            star_id="Test Star",
        )

        star = Star(
            st_name="Test Star",
            reference=reference,
        )

        assert star.st_name == "Test Star"
        assert star.st_spectral_type is None
        assert star.sy_constellation is None
        assert star.st_distance is None

    def test_star_distance_with_uncertainty(self, sample_star):
        """Test de la distance avec incertitudes."""
        star = sample_star

        assert star.st_distance.value == 47.1
        assert star.st_distance.error_positive == 0.5
        assert star.st_distance.error_negative == 0.5

    def test_star_str_representation(self, sample_star):
        """Test de la représentation string."""
        star = sample_star
        str_repr = str(star)

        assert "HD 209458" in str_repr
