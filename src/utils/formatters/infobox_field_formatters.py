# src/utils/formatters/infobox_field_formatters.py
from typing import Any, Optional

from src.constants.field_mappings import DISCOVERY_FACILITY_MAPPING, METHOD_NAME_MAPPING
from src.models.reference import DataPoint
from src.utils.validators import infobox_validators
from src.models.infobox_fields import FieldMapping


class FieldFormatter:
    """Formatters pour différents types de champs"""

    def _format_field(
        self, datapoint: DataPoint, mapping: FieldMapping, default_mapping: dict
    ) -> str:
        """Formats a standard field with its value and unit."""
        value, unit = self._extract_field_value(datapoint)
        if not value:
            return ""

        unit_to_use = self._get_unit_to_use(unit, mapping, default_mapping)

        formatted_value = FieldFormatter._apply_special_formatting(
            mapping.infobox_field, value
        )
        return FieldFormatter._format_field_with_unit(
            mapping.infobox_field, formatted_value, unit_to_use
        )

    @staticmethod
    def _apply_special_formatting(infobox_field: str, value: Any) -> str:
        """Applique le formatage spécial selon le type de champ"""
        if infobox_field == "lieu":
            return FieldFormatter._format_discovery_facility(value)
        elif infobox_field == "méthode":
            return FieldFormatter._format_discovery_method(value)
        elif infobox_field == "âge":
            return FieldFormatter._format_age(value)
        elif infobox_field == "désignations":
            return FieldFormatter._format_designations(value)
        elif infobox_field == "carte UAI":
            return FieldFormatter._format_carte_uai(value)
        elif infobox_field == "constellation":
            return FieldFormatter._format_constellation(value)
        return value

    @staticmethod
    def _format_discovery_facility(value: Any) -> str:
        """Formate le lieu de découverte"""
        mapped = DISCOVERY_FACILITY_MAPPING.get(value)
        return f"[[{mapped}]]" if mapped else str(value)

    @staticmethod
    def _format_discovery_method(value: Any) -> str:
        """Formate la méthode de découverte"""
        method_key = str(value).strip().lower()
        mapped = METHOD_NAME_MAPPING.get(method_key)
        return f"[[{mapped['article']}|{mapped['display']}]]" if mapped else str(value)

    @staticmethod
    def _format_age(value: Any) -> str:
        """Formate l'âge avec notation scientifique"""
        return f"{value}×10<sup>9</sup>"

    @staticmethod
    def _format_designations(value: Any) -> str:
        """Formate les désignations en liste"""
        if isinstance(value, list):
            return ", ".join(
                FieldFormatter._format_designation_with_template(str(v))
                for v in value
                if str(v).strip()
            )
        return FieldFormatter._format_designation_with_template(str(value).strip())

    @staticmethod
    def _format_field_with_unit(
        infobox_field: str, value: str, unit: Optional[str]
    ) -> str:
        """Formate le champ avec son unité si présente"""
        output = f" | {infobox_field} = {value}"
        if unit:
            output += f"\n | {infobox_field} unité = {unit}"
        return output

    def _extract_field_value(
        self, datapoint: DataPoint
    ) -> tuple[Optional[Any], Optional[str]]:
        """
        Returns a tuple (value, unit) from the DataPoint.
        If the DataPoint has no value or it's invalid, returns (None, None).
        """
        # We assume DataPoint has .value and .unit attributes
        try:
            raw_value = datapoint.value
            raw_unit = getattr(datapoint, "unit", None)
        except AttributeError:
            return None, None

        # If the raw_value is None or empty, treat as invalid
        if raw_value is None or (
            isinstance(raw_value, str) and raw_value.strip() == ""
        ):
            return None, None

        return raw_value, raw_unit

    @staticmethod
    def _format_designation_with_template(designation: str) -> str:
        """Formate une désignation avec le modèle Wikipédia approprié si possible."""
        d = designation.strip()
        if d.lower().startswith("hd "):
            return f"{{{{HD|{d.split(' ')[1]}}}}}"
        if d.lower().startswith("hip "):
            return f"{{{{HIP|{d.split(' ')[1]}}}}}"
        if d.lower().startswith("koi "):
            return f"{{{{StarKOI|{d.split(' ')[1]}}}}}"
        if d.lower().startswith("kic "):
            return f"{{{{StarKIC|{d.split(' ')[1]}}}}}"
        if d.lower().startswith("tic "):
            return f"{{{{StarTIC|{d.split(' ')[1]}}}}}"
        if d.lower().startswith("2mass j"):
            core = d[7:].strip()
            if "+" in core or "-" in core:
                for sep in ["+", "-"]:
                    if sep in core:
                        parts = core.split(sep)
                        if len(parts) == 2:
                            return f"{{{{Star2MASS|{parts[0]}|{sep}{parts[1]}}}}}"
        # Ajoute d'autres modèles si besoin
        return d

    def format_numeric_no_trailing_zeros(value):
        try:
            fval = float(value)
            return f"{fval:.5f}".rstrip("0").rstrip(".")
        except Exception:
            return str(value)

    def process_field(
        self,
        datapoint: DataPoint | None,
        mapping: FieldMapping,
        default_mapping: dict,
        notes_fields: list[str],
        obj: Any,
    ) -> str:
        """
        Traite un champ complet avec sa valeur, unité et notes.
        """
        if mapping.condition and not mapping.condition(obj):
            return ""

        if not datapoint or not datapoint.value:
            return ""

        value_part = self._format_field(datapoint, mapping, default_mapping)
        if not value_part:
            return ""

        return self._add_notes_if_needed(value_part, datapoint, mapping, notes_fields)

    @staticmethod
    def _format_constellation(value: str) -> str:
        """Formate le champ constellation."""
        return f"[[{value} (constellation)|{value}]]"

    @staticmethod
    def _format_carte_uai(value: str) -> str:
        """Formate le champ carte UAI."""
        return value

    def _get_unit_to_use(
        self, unit: Optional[str], mapping: FieldMapping, default_mapping: dict
    ) -> Optional[str]:
        """Détermine l'unité à utiliser pour le champ."""
        if mapping.unit_override:
            return mapping.unit_override

        if not unit:
            return None

        return (
            unit
            if infobox_validators.is_needed_infobox_unit(
                mapping.infobox_field, unit, default_mapping
            )
            else None
        )

    def _add_notes_if_needed(
        self,
        value_part: str,
        datapoint: DataPoint,
        mapping: FieldMapping,
        notes_fields: list[str],
    ) -> str:
        """Ajoute les notes au champ si nécessaire."""
        parts = [value_part]
        if datapoint.reference and infobox_validators.is_valid_infobox_note(
            mapping.infobox_field, notes_fields
        ):
            notes_ref = FieldFormatter._extract_notes(datapoint)
            if notes_ref:
                parts.append(f"| {mapping.infobox_field} notes = {notes_ref}")

        return "\n".join(parts)

    @staticmethod
    def _extract_notes(datapoint: DataPoint) -> Optional[str]:
        """Extrait les notes d'un DataPoint."""
        ref = datapoint.reference
        if not ref:
            return None

        try:
            full_ref = ref.to_wiki_ref()
            if not full_ref:
                return None
            return full_ref
        except Exception:
            return None
