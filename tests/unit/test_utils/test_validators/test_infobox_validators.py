"""Tests pour les validateurs d'infobox."""

import pytest
from src.utils.validators.infobox_validators import (
    is_valid_infobox_note,
    is_valid_infobox_value,
    is_needed_infobox_unit,
)


class TestIsValidInfoboxNote:
    """Tests pour is_valid_infobox_note."""

    def test_valid_note_lowercase(self):
        """Test avec une note valide en minuscules."""
        notes_fields = ["note1", "note2", "note3"]
        assert is_valid_infobox_note("note1", notes_fields) is True

    def test_valid_note_uppercase(self):
        """Test avec une note valide en majuscules."""
        notes_fields = ["note1", "note2", "note3"]
        assert is_valid_infobox_note("NOTE2", notes_fields) is True

    def test_valid_note_mixedcase(self):
        """Test avec une note valide en casse mixte."""
        notes_fields = ["note1", "note2", "note3"]
        assert is_valid_infobox_note("NoTe3", notes_fields) is True

    def test_invalid_note(self):
        """Test avec une note invalide."""
        notes_fields = ["note1", "note2", "note3"]
        assert is_valid_infobox_note("note4", notes_fields) is False

    def test_empty_notes_list(self):
        """Test avec une liste de notes vide."""
        assert is_valid_infobox_note("note1", []) is False


class TestIsValidInfoboxValue:
    """Tests pour is_valid_infobox_value."""

    def test_none_value(self):
        """Test avec une valeur None."""
        assert is_valid_infobox_value(None) is False

    def test_empty_string(self):
        """Test avec une chaîne vide."""
        assert is_valid_infobox_value("") is False

    def test_whitespace_only(self):
        """Test avec uniquement des espaces."""
        assert is_valid_infobox_value("   ") is False

    def test_nan_lowercase(self):
        """Test avec 'nan' en minuscules."""
        assert is_valid_infobox_value("nan") is False

    def test_nan_uppercase(self):
        """Test avec 'NaN' en majuscules."""
        assert is_valid_infobox_value("NaN") is False

    def test_nan_with_template(self):
        """Test avec 'nan{{...}}'."""
        assert is_valid_infobox_value("nan{{unité|km}}") is False

    def test_valid_string(self):
        """Test avec une chaîne valide."""
        assert is_valid_infobox_value("test value") is True

    def test_valid_number(self):
        """Test avec un nombre valide."""
        assert is_valid_infobox_value(42) is True

    def test_valid_float(self):
        """Test avec un float valide."""
        assert is_valid_infobox_value(3.14) is True

    def test_valid_zero(self):
        """Test avec zéro."""
        assert is_valid_infobox_value(0) is True

    def test_unicode_normalization(self):
        """Test avec des caractères unicode."""
        assert is_valid_infobox_value("café") is True

    def test_unconvertible_object(self):
        """Test avec un objet qui ne peut pas être converti en string."""

        class UnconvertibleObject:
            def __str__(self):
                raise ValueError("Cannot convert")

        assert is_valid_infobox_value(UnconvertibleObject()) is False


class TestIsNeededInfoboxUnit:
    """Tests pour is_needed_infobox_unit."""

    def test_unit_different_from_default(self):
        """Test avec une unité différente de la valeur par défaut."""
        default_mapping = {"mass": "kg", "distance": "m"}
        assert is_needed_infobox_unit("mass", "g", default_mapping) is True

    def test_unit_same_as_default(self):
        """Test avec une unité identique à la valeur par défaut."""
        default_mapping = {"mass": "kg", "distance": "m"}
        assert is_needed_infobox_unit("mass", "kg", default_mapping) is False

    def test_field_not_in_mapping(self):
        """Test avec un champ absent du mapping."""
        default_mapping = {"mass": "kg", "distance": "m"}
        assert is_needed_infobox_unit("temperature", "K", default_mapping) is True

    def test_field_lowercase_conversion(self):
        """Test avec un champ en majuscules."""
        default_mapping = {"mass": "kg", "distance": "m"}
        assert is_needed_infobox_unit("MASS", "kg", default_mapping) is False

    def test_empty_mapping(self):
        """Test avec un mapping vide."""
        assert is_needed_infobox_unit("mass", "kg", {}) is True
