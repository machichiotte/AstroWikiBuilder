"""Tests pour infobox_field_formatters."""

import pytest

from src.models.entities.exoplanet_model import ValueWithUncertainty
from src.models.infobox_fields import FieldMapping
from src.utils.formatters.infobox_field_formatters import FieldFormatter, InfoboxField


class TestFieldFormatter:
    """Tests pour FieldFormatter."""

    @pytest.fixture
    def formatter(self):
        """Fixture pour créer un FieldFormatter."""
        return FieldFormatter()

    def test_format_error_number_with_both_errors(self):
        """Test de formatage avec erreurs positive et négative."""
        value = ValueWithUncertainty(value=1.234, error_positive=0.05, error_negative=0.03)
        result = FieldFormatter._format_error_number(value)
        assert "1.23" in result
        assert "{{±|0.05|0.03}}" in result

    def test_format_error_number_with_positive_error_only(self):
        """Test de formatage avec erreur positive seulement."""
        value = ValueWithUncertainty(value=2.5, error_positive=0.1, error_negative=None)
        result = FieldFormatter._format_error_number(value)
        assert "2.50" in result
        assert "{{±|0.10|}}" in result

    def test_format_error_number_with_negative_error_only(self):
        """Test de formatage avec erreur négative seulement."""
        value = ValueWithUncertainty(value=3.7, error_positive=None, error_negative=0.2)
        result = FieldFormatter._format_error_number(value)
        assert "3.70" in result
        assert "{{±||0.20}}" in result

    def test_format_error_number_without_errors(self):
        """Test de formatage sans erreurs."""
        value = ValueWithUncertainty(value=4.5, error_positive=None, error_negative=None)
        result = FieldFormatter._format_error_number(value)
        assert result == "4.50"

    def test_format_error_number_none_value(self):
        """Test de formatage avec valeur None."""
        result = FieldFormatter._format_error_number(None)
        assert result == ""

    def test_format_error_number_value_none(self):
        """Test de formatage avec value.value = None."""
        value = ValueWithUncertainty(value=None)
        result = FieldFormatter._format_error_number(value)
        assert result == ""

    def test_format_discovery_facility_mapped(self):
        """Test de formatage du lieu de découverte avec mapping."""
        # Note: Ce test dépend du contenu de WIKIPEDIA_DISC_FACILITY_MAP
        result = FieldFormatter._format_discovery_facility("Kepler")
        assert isinstance(result, str)

    def test_format_discovery_facility_unmapped(self):
        """Test de formatage du lieu de découverte sans mapping."""
        result = FieldFormatter._format_discovery_facility("Unknown Facility")
        assert result == "Unknown Facility"

    def test_format_discovery_method_mapped(self):
        """Test de formatage de la méthode de découverte avec mapping."""
        # Note: Ce test dépend du contenu de WIKIPEDIA_DISC_METHOD_MAP
        result = FieldFormatter._format_discovery_method("transit")
        assert isinstance(result, str)

    def test_format_discovery_method_unmapped(self):
        """Test de formatage de la méthode de découverte sans mapping."""
        result = FieldFormatter._format_discovery_method("Unknown Method")
        assert result == "Unknown Method"

    def test_format_designations_hd(self):
        """Test de formatage des désignations HD."""
        result = FieldFormatter._format_designations("HD 209458")
        assert "{{HD|209458}}" in result

    def test_format_designations_hip(self):
        """Test de formatage des désignations HIP."""
        result = FieldFormatter._format_designations("HIP 108859")
        assert "{{HIP|108859}}" in result

    def test_format_designations_koi(self):
        """Test de formatage des désignations KOI."""
        result = FieldFormatter._format_designations("KOI 87")
        assert "{{StarKOI|87}}" in result

    def test_format_designations_kic(self):
        """Test de formatage des désignations KIC."""
        result = FieldFormatter._format_designations("KIC 11804465")
        assert "{{StarKIC|11804465}}" in result

    def test_format_designations_tic(self):
        """Test de formatage des désignations TIC."""
        result = FieldFormatter._format_designations("TIC 307210830")
        assert "{{StarTIC|307210830}}" in result

    def test_format_designations_2mass_with_plus(self):
        """Test de formatage des désignations 2MASS avec +."""
        result = FieldFormatter._format_designations("2MASS J19285196+4824465")
        assert "{{Star2MASS|19285196|+4824465}}" in result

    def test_format_designations_2mass_with_minus(self):
        """Test de formatage des désignations 2MASS avec -."""
        result = FieldFormatter._format_designations("2MASS J19285196-4824465")
        assert "{{Star2MASS|19285196|-4824465}}" in result

    def test_format_designations_unknown(self):
        """Test de formatage des désignations inconnues."""
        result = FieldFormatter._format_designations("Unknown Designation")
        assert result == "Unknown Designation"

    def test_format_designations_list(self):
        """Test de formatage d'une liste de désignations."""
        result = FieldFormatter._format_designations(["HD 209458", "HIP 108859"])
        assert "{{HD|209458}}" in result
        assert "{{HIP|108859}}" in result
        assert ", " in result

    def test_format_age_with_value(self):
        """Test de formatage de l'âge."""
        value = ValueWithUncertainty(value=4.5)
        result = FieldFormatter.format_age(value)
        assert "4.5" in result
        assert "×10<sup>9</sup>" in result

    def test_format_age_none(self):
        """Test de formatage de l'âge avec None."""
        result = FieldFormatter.format_age(None)
        assert result == ""

    def test_format_age_value_none(self):
        """Test de formatage de l'âge avec value.value = None."""
        value = ValueWithUncertainty(value=None)
        result = FieldFormatter.format_age(value)
        assert result == ""

    def test_process_field_with_string_value(self, formatter):
        """Test de traitement d'un champ avec valeur string."""
        mapping = FieldMapping(source_attribute="test", infobox_field="test_field")
        result = formatter.process_field("test value", mapping, [])
        assert "test_field" in result
        assert "test value" in result

    def test_process_field_with_value_with_uncertainty(self, formatter):
        """Test de traitement d'un champ avec ValueWithUncertainty."""
        mapping = FieldMapping(source_attribute="pl_mass", infobox_field="mass")
        value = ValueWithUncertainty(value=1.5, error_positive=0.1)
        result = formatter.process_field(value, mapping, [])
        assert "mass" in result
        assert "1.50" in result

    def test_process_field_with_empty_value(self, formatter):
        """Test de traitement d'un champ avec valeur vide."""
        mapping = FieldMapping(source_attribute="test", infobox_field="test_field")
        result = formatter.process_field("", mapping, [])
        assert result == ""

    def test_process_field_with_none_value(self, formatter):
        """Test de traitement d'un champ avec valeur None."""
        mapping = FieldMapping(source_attribute="test", infobox_field="test_field")
        result = formatter.process_field(None, mapping, [])
        assert result == ""

    def test_process_field_with_reference(self, formatter):
        """Test de traitement d'un champ avec référence."""
        mapping = FieldMapping(source_attribute="pl_mass", infobox_field="mass")
        value = ValueWithUncertainty(value=1.5)
        result = formatter.process_field(value, mapping, ["mass"], wiki_reference="<ref>Test</ref>")
        assert "mass" in result
        assert "mass notes" in result
        assert "<ref>Test</ref>" in result

    def test_process_field_with_reference_not_in_notes_fields(self, formatter):
        """Test de traitement d'un champ avec référence mais pas dans notes_fields."""
        mapping = FieldMapping(source_attribute="other", infobox_field="other_field")
        result = formatter.process_field("value", mapping, ["mass"], wiki_reference="<ref>Test</ref>")
        assert "other_field" in result
        assert "other_field notes" not in result

    def test_format_field_value_with_location(self, formatter):
        """Test de formatage de valeur avec champ location."""
        result = formatter._format_field_value("Kepler", InfoboxField.LOCATION)
        assert isinstance(result, str)

    def test_format_field_value_with_method(self, formatter):
        """Test de formatage de valeur avec champ method."""
        result = formatter._format_field_value("transit", InfoboxField.METHOD)
        assert isinstance(result, str)

    def test_format_field_value_with_constellation(self, formatter):
        """Test de formatage de valeur avec champ constellation."""
        result = formatter._format_field_value("Cygnus", InfoboxField.CONSTELLATION)
        assert "[[Cygnus (constellation)|Cygnus]]" in result

    def test_format_field_value_with_designations(self, formatter):
        """Test de formatage de valeur avec champ designations."""
        result = formatter._format_field_value("HD 209458", InfoboxField.DESIGNATIONS)
        assert "{{HD|209458}}" in result
